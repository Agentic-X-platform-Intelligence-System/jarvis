"""Claude (Anthropic) client with tool-use loop and conversation memory."""

from __future__ import annotations

import json
import logging
from typing import Any, Optional

from anthropic import Anthropic
from anthropic import APIStatusError, APITimeoutError, RateLimitError

from config import ANTHROPIC_API_KEY, API_TIMEOUT_SECONDS, CLAUDE_MODEL, SYSTEM_PROMPT
from stem.memory.conversation import ConversationHistory
from stem.tools import SkillRouter, anthropic_tool_definitions

logger = logging.getLogger(__name__)


class BrainError(RuntimeError):
    """Raised when the LLM pipeline cannot produce a response."""


def _extract_text_blocks(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""

    parts: list[str] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "text":
            t = block.get("text")
            if isinstance(t, str) and t.strip():
                parts.append(t.strip())
    return "\n".join(parts).strip()


class JarvisBrain:
    """Claude wrapper: maintains rolling history and executes skills via tool_use."""

    def __init__(
        self,
        router: Optional[SkillRouter] = None,
        history: Optional[ConversationHistory] = None,
        model: str = CLAUDE_MODEL,
        system_prompt: str = SYSTEM_PROMPT,
    ) -> None:
        if not ANTHROPIC_API_KEY:
            raise BrainError("ANTHROPIC_API_KEY is missing (.env)")

        self._client = Anthropic(api_key=ANTHROPIC_API_KEY, timeout=API_TIMEOUT_SECONDS)
        self._model = model
        self._system_prompt = system_prompt
        self._router = router or SkillRouter()
        self._history = history or ConversationHistory()
        self._tools = anthropic_tool_definitions()

    @property
    def history(self) -> ConversationHistory:
        return self._history

    def respond(self, user_text: str, max_tokens: int = 1024) -> str:
        """Run a full model turn (including tool loops) and return assistant text for TTS."""
        user_text = user_text.strip()
        if not user_text:
            raise BrainError("Empty user text")

        self._history.add_user_message(user_text)

        try:
            final_text = self._run_tool_loop(max_tokens=max_tokens)
        except (APITimeoutError, RateLimitError, APIStatusError) as exc:
            # Remove the user message we could not answer to avoid dangling turns
            self._pop_last_user_if_matches(user_text)
            raise BrainError(f"Anthropic API error: {exc}") from exc
        except BrainError:
            self._pop_last_user_if_matches(user_text)
            raise

        # Assistant messages (including tool_use blocks) are already recorded in ``_run_tool_loop``.
        self._history.trim_to_turn_budget()
        return final_text

    def _pop_last_user_if_matches(self, user_text: str) -> None:
        if not self._history.messages:
            return
        last = self._history.messages[-1]
        if last.get("role") == "user":
            c = last.get("content")
            if isinstance(c, str) and c.strip() == user_text.strip():
                self._history.messages.pop()

    def _run_tool_loop(self, max_tokens: int) -> str:
        max_tool_rounds = 8
        final_text_parts: list[str] = []

        last_assistant_blocks: list[dict[str, Any]] = []

        for round_idx in range(max_tool_rounds):
            msg = self._client.messages.create(
                model=self._model,
                max_tokens=max_tokens,
                system=self._system_prompt,
                tools=self._tools,
                messages=self._history.snapshot(),
            )

            stop_reason = msg.stop_reason
            content = msg.content

            tool_uses: list[dict[str, Any]] = []
            text_chunks: list[str] = []
            for block in content:
                b = block.model_dump() if hasattr(block, "model_dump") else dict(block)  # type: ignore[arg-type]
                if b.get("type") == "tool_use":
                    tool_uses.append(b)
                elif b.get("type") == "text":
                    t = b.get("text")
                    if isinstance(t, str) and t.strip():
                        text_chunks.append(t.strip())

            # Persist assistant message exactly as returned (text + tool_use blocks)
            assistant_payload: list[dict[str, Any]] = []
            for block in content:
                b = block.model_dump() if hasattr(block, "model_dump") else dict(block)  # type: ignore[arg-type]
                assistant_payload.append(b)
            self._history.add_assistant_message(assistant_payload)
            last_assistant_blocks = assistant_payload

            if text_chunks:
                final_text_parts.extend(text_chunks)

            if stop_reason == "tool_use" and tool_uses:
                if round_idx >= max_tool_rounds - 1:
                    raise BrainError("Exceeded maximum tool-use rounds without a final answer")
                tool_result_blocks: list[dict[str, Any]] = []
                for tu in tool_uses:
                    tu_id = str(tu.get("id", ""))
                    name = str(tu.get("name", ""))
                    inp = tu.get("input") or {}
                    if not isinstance(inp, dict):
                        inp = {}

                    logger.info("Tool call: %s(%s)", name, json.dumps(inp, ensure_ascii=False)[:500])
                    result_str = self._router.run(name, inp)
                    tool_result_blocks.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": tu_id,
                            "content": result_str,
                        }
                    )

                self._history.add_user_message(tool_result_blocks)
                continue

            break

        text = "\n".join(final_text_parts).strip()
        if not text:
            text = _extract_text_blocks(last_assistant_blocks)
        if not text:
            raise BrainError("Model returned no assistant text")
        return text
