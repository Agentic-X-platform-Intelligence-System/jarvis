"""Rolling conversation history and SQLite interaction logging."""

from __future__ import annotations

import sqlite3
import threading
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import DB_PATH, MAX_CONVERSATION_TURNS


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ConversationHistory:
    """Stores Anthropic-style message dicts with a rolling cap on conversational turns."""

    max_turns: int = MAX_CONVERSATION_TURNS
    messages: deque[dict[str, Any]] = field(default_factory=lambda: deque(maxlen=400))

    def add_user_message(self, content: str | list[dict[str, Any]]) -> None:
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str | list[dict[str, Any]]) -> None:
        self.messages.append({"role": "assistant", "content": content})

    def snapshot(self) -> list[dict[str, Any]]:
        """Return a shallow copy suitable for passing to the API."""
        return list(self.messages)

    def trim_to_turn_budget(self) -> None:
        """
        Approximate trim: keep trailing messages so we do not exceed max_turns
        user-visible exchanges. Counts 'user' messages that are plain text (not only tool_result).
        """
        msgs = list(self.messages)
        user_turns = 0
        cut = 0
        for i in range(len(msgs) - 1, -1, -1):
            m = msgs[i]
            if m.get("role") != "user":
                continue
            content = m.get("content")
            if isinstance(content, str) and content.strip():
                user_turns += 1
            elif isinstance(content, list):
                has_non_tool = any(
                    isinstance(b, dict) and b.get("type") not in (None, "tool_result")
                    for b in content
                )
                if has_non_tool or any(
                    isinstance(b, dict) and b.get("type") == "text" for b in content
                ):
                    user_turns += 1
            if user_turns >= self.max_turns:
                cut = i
                break
        if cut > 0:
            self.messages.clear()
            self.messages.extend(msgs[cut:])


class InteractionLogger:
    """Thread-safe SQLite logger for user input and final assistant responses."""

    def __init__(self, db_path: Path = DB_PATH) -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    jarvis_response TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def log(self, user_input: str, jarvis_response: str) -> None:
        ts = _utc_now_iso()
        with self._lock:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    "INSERT INTO interactions (timestamp, user_input, jarvis_response) VALUES (?, ?, ?)",
                    (ts, user_input, jarvis_response),
                )
                conn.commit()
