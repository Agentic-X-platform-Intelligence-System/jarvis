"""Skill registry: Anthropic tool definitions + execution router."""

from __future__ import annotations

import json
import logging
from typing import Any

from .datetime_skill import DateTimeSkill
from .system import SystemSkill
from .weather import WeatherSkill
from .web_search import WebSearchSkill

logger = logging.getLogger(__name__)


def anthropic_tool_definitions() -> list[dict[str, Any]]:
    """Return Claude ``tools`` definitions (name/description/input_schema)."""
    return [
        {
            "name": "get_weather",
            "description": "Get current weather for a city using OpenWeatherMap.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, optionally with country code"},
                    "units": {
                        "type": "string",
                        "description": "Units: metric or imperial",
                        "enum": ["metric", "imperial"],
                    },
                },
                "required": ["city"],
            },
        },
        {
            "name": "web_search",
            "description": "Search the web for fresh information. Uses Serper if configured, otherwise DuckDuckGo.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {
                        "type": "integer",
                        "description": "Max results to return (1-10)",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        },
        {
            "name": "system_control",
            "description": "Control local system: open an application, set master volume (Windows), or read/write clipboard.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["open_application", "set_volume", "clipboard_set", "clipboard_get"],
                    },
                    "target": {
                        "type": "string",
                        "description": "For open_application: executable name, path, or macOS app name",
                    },
                    "level": {
                        "type": "integer",
                        "description": "For set_volume: 0-100 master volume (Windows; requires pycaw)",
                    },
                    "text": {"type": "string", "description": "For clipboard_set: text to copy"},
                },
                "required": ["action"],
            },
        },
        {
            "name": "get_datetime",
            "description": "Get the current local (or specified timezone) date/time.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA timezone like America/New_York; omit for local",
                    },
                    "format": {
                        "type": "string",
                        "description": "iso | date | time",
                        "enum": ["iso", "date", "time"],
                    },
                },
                "required": [],
            },
        },
    ]


class SkillRouter:
    """Maps Claude tool names to skill classes."""

    def __init__(self) -> None:
        self._registry: dict[str, Any] = {
            "get_weather": WeatherSkill(),
            "web_search": WebSearchSkill(),
            "system_control": SystemSkill(),
            "get_datetime": DateTimeSkill(),
        }

    def run(self, tool_name: str, tool_input: dict[str, Any]) -> str:
        skill = self._registry.get(tool_name)
        if skill is None:
            return json.dumps({"ok": False, "error": f"Unknown tool: {tool_name}"})
        try:
            result = skill.run(tool_input)
        except Exception as exc:
            logger.exception("Skill %s crashed", tool_name)
            return json.dumps({"ok": False, "error": f"Skill error: {exc}"})
        return json.dumps(result, ensure_ascii=False)


__all__ = ["SkillRouter", "anthropic_tool_definitions"]
