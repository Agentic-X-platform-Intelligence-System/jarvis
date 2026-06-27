"""Smoke tests for monorepo package layout and legacy shims."""

from __future__ import annotations


def test_stem_config_imports() -> None:
    from stem.config.settings import CLAUDE_MODEL, SAMPLE_RATE, get_settings

    assert SAMPLE_RATE == 16000
    assert get_settings().claude_model == CLAUDE_MODEL


def test_stem_tools_imports() -> None:
    from stem.tools import SkillRouter, anthropic_tool_definitions

    tools = anthropic_tool_definitions()
    assert len(tools) >= 4
    result = SkillRouter().run("unknown_tool", {})
    assert "Unknown tool" in result


def test_stem_agent_imports() -> None:
    from stem.agent.brain import BrainError, JarvisBrain

    assert BrainError.__name__ == "BrainError"
    assert JarvisBrain.__name__ == "JarvisBrain"


def test_aura_imports() -> None:
    from aura import JarvisTTS, WhisperSTT, WakeWordListener

    assert WhisperSTT.__name__ == "WhisperSTT"
    assert JarvisTTS.__name__ == "JarvisTTS"
    assert WakeWordListener.__name__ == "WakeWordListener"


def test_legacy_shims() -> None:
    from config import CLAUDE_MODEL
    from core.brain import JarvisBrain
    from core.stt import WhisperSTT
    from memory import ConversationHistory
    from skills import SkillRouter

    assert CLAUDE_MODEL
    assert JarvisBrain.__name__ == "JarvisBrain"
    assert WhisperSTT.__name__ == "WhisperSTT"
    assert ConversationHistory.__name__ == "ConversationHistory"
    assert SkillRouter.__name__ == "SkillRouter"


def test_voice_entry_imports() -> None:
    from apps.voice.main import main

    assert callable(main)
