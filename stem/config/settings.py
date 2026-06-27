"""Central configuration and constants for AXIS / Jarvis."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application settings with AXIS_* and JARVIS_* env var aliases."""

    model_config = SettingsConfigDict(
        env_file=str(_PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    sample_rate: int = Field(
        default=16000,
        validation_alias=AliasChoices("AXIS_SAMPLE_RATE", "JARVIS_SAMPLE_RATE"),
    )
    record_seconds_default: float = Field(
        default=5.0,
        validation_alias=AliasChoices("AXIS_RECORD_SECONDS", "JARVIS_RECORD_SECONDS"),
    )
    record_channels: int = 1
    record_dtype: str = "float32"

    porcupine_access_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("PORCUPINE_ACCESS_KEY",),
    )
    porcupine_keyword_path: str | None = Field(
        default=None,
        validation_alias=AliasChoices("PORCUPINE_KEYWORD_PATH",),
    )
    porcupine_builtin_keyword: str = Field(
        default="jarvis",
        validation_alias=AliasChoices("AXIS_PORCUPINE_BUILTIN_KEYWORD", "PORCUPINE_BUILTIN_KEYWORD", "JARVIS_PORCUPINE_BUILTIN_KEYWORD"),
    )

    whisper_model_size: str = Field(
        default="base",
        validation_alias=AliasChoices("AXIS_WHISPER_MODEL_SIZE", "WHISPER_MODEL_SIZE", "JARVIS_WHISPER_MODEL_SIZE"),
    )
    whisper_device: str = Field(
        default="auto",
        validation_alias=AliasChoices("AXIS_WHISPER_DEVICE", "WHISPER_DEVICE", "JARVIS_WHISPER_DEVICE"),
    )
    whisper_compute_type: str = Field(
        default="int8",
        validation_alias=AliasChoices("AXIS_WHISPER_COMPUTE_TYPE", "WHISPER_COMPUTE_TYPE", "JARVIS_WHISPER_COMPUTE_TYPE"),
    )

    anthropic_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("ANTHROPIC_API_KEY",),
    )
    claude_model: str = Field(
        default="claude-sonnet-4-20250514",
        validation_alias=AliasChoices("AXIS_CLAUDE_MODEL", "CLAUDE_MODEL", "JARVIS_CLAUDE_MODEL"),
    )
    max_conversation_turns: int = Field(
        default=10,
        validation_alias=AliasChoices("AXIS_MAX_CONVERSATION_TURNS", "MAX_CONVERSATION_TURNS", "JARVIS_MAX_CONVERSATION_TURNS"),
    )
    system_prompt: str = Field(
        default=(
            "You are JARVIS, a sharp and concise personal AI assistant. "
            "Keep responses under 3 sentences unless asked for detail. "
            "You have access to tools for weather, web search, system control, and time."
        ),
        validation_alias=AliasChoices("AXIS_SYSTEM_PROMPT", "JARVIS_SYSTEM_PROMPT"),
    )

    tts_backend: str = Field(
        default="auto",
        validation_alias=AliasChoices("AXIS_TTS_BACKEND", "JARVIS_TTS_BACKEND"),
    )
    tts_model_name: str = Field(
        default="tts_models/en/ljspeech/tacotron2-DDC",
        validation_alias=AliasChoices("AXIS_TTS_MODEL_NAME", "TTS_MODEL_NAME", "JARVIS_TTS_MODEL_NAME"),
    )
    edge_tts_voice: str = Field(
        default="en-US-GuyNeural",
        validation_alias=AliasChoices("AXIS_EDGE_TTS_VOICE", "EDGE_TTS_VOICE", "JARVIS_EDGE_TTS_VOICE"),
    )

    openweather_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("OPENWEATHER_API_KEY",),
    )
    serper_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERPER_API_KEY",),
    )

    api_timeout_seconds: float = Field(
        default=120.0,
        validation_alias=AliasChoices("AXIS_API_TIMEOUT_SECONDS", "API_TIMEOUT_SECONDS", "JARVIS_API_TIMEOUT_SECONDS"),
    )
    record_queue_timeout: float = Field(
        default=0.5,
        validation_alias=AliasChoices("AXIS_RECORD_QUEUE_TIMEOUT", "RECORD_QUEUE_TIMEOUT", "JARVIS_RECORD_QUEUE_TIMEOUT"),
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


_settings = get_settings()

PROJECT_ROOT: Path = _PROJECT_ROOT
DATA_DIR: Path = _PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH: Path = DATA_DIR / "jarvis_interactions.db"
AUDIO_TMP_DIR: Path = DATA_DIR / "audio_tmp"
AUDIO_TMP_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE: int = _settings.sample_rate
RECORD_SECONDS_DEFAULT: float = _settings.record_seconds_default
RECORD_CHANNELS: int = _settings.record_channels
RECORD_DTYPE: str = _settings.record_dtype

PORCUPINE_ACCESS_KEY: str | None = _settings.porcupine_access_key
PORCUPINE_KEYWORD_PATH: str | None = _settings.porcupine_keyword_path
PORCUPINE_BUILTIN_KEYWORD: str = _settings.porcupine_builtin_keyword.strip()

WHISPER_MODEL_SIZE: str = _settings.whisper_model_size
WHISPER_DEVICE: str = _settings.whisper_device
WHISPER_COMPUTE_TYPE: str = _settings.whisper_compute_type

ANTHROPIC_API_KEY: str | None = _settings.anthropic_api_key
CLAUDE_MODEL: str = _settings.claude_model
MAX_CONVERSATION_TURNS: int = _settings.max_conversation_turns
SYSTEM_PROMPT: str = _settings.system_prompt

JARVIS_TTS_BACKEND: str = _settings.tts_backend.strip().lower()
TTS_MODEL_NAME: str = _settings.tts_model_name
EDGE_TTS_VOICE: str = _settings.edge_tts_voice.strip()

OPENWEATHER_API_KEY: str | None = _settings.openweather_api_key
SERPER_API_KEY: str | None = _settings.serper_api_key

API_TIMEOUT_SECONDS: float = _settings.api_timeout_seconds
RECORD_QUEUE_TIMEOUT: float = _settings.record_queue_timeout
