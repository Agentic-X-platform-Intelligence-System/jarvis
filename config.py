"""Central configuration and constants for JARVIS."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (directory containing this file)
_PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(_PROJECT_ROOT / ".env")

# --- Paths ---
DATA_DIR: Path = _PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH: Path = DATA_DIR / "jarvis_interactions.db"
AUDIO_TMP_DIR: Path = DATA_DIR / "audio_tmp"
AUDIO_TMP_DIR.mkdir(parents=True, exist_ok=True)

# --- Audio I/O ---
SAMPLE_RATE: int = int(os.getenv("JARVIS_SAMPLE_RATE", "16000"))
RECORD_SECONDS_DEFAULT: float = float(os.getenv("JARVIS_RECORD_SECONDS", "5.0"))
RECORD_CHANNELS: int = 1
RECORD_DTYPE: str = "float32"

# --- Wake word (Porcupine) ---
PORCUPINE_ACCESS_KEY: str | None = os.getenv("PORCUPINE_ACCESS_KEY")
# Optional path to custom .ppn file from Picovoice Console (for "Hey JARVIS" custom model)
PORCUPINE_KEYWORD_PATH: str | None = os.getenv("PORCUPINE_KEYWORD_PATH")
# Built-in keyword if no custom path (e.g. "jarvis" is a Picovoice built-in keyword)
PORCUPINE_BUILTIN_KEYWORD: str = os.getenv("PORCUPINE_BUILTIN_KEYWORD", "jarvis").strip()

# --- STT (faster-whisper) ---
WHISPER_MODEL_SIZE: str = os.getenv("WHISPER_MODEL_SIZE", "base")
WHISPER_DEVICE: str = os.getenv("WHISPER_DEVICE", "auto")
WHISPER_COMPUTE_TYPE: str = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

# --- LLM (Anthropic) ---
ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
MAX_CONVERSATION_TURNS: int = int(os.getenv("MAX_CONVERSATION_TURNS", "10"))

SYSTEM_PROMPT: str = os.getenv(
    "JARVIS_SYSTEM_PROMPT",
    "You are JARVIS, a sharp and concise personal AI assistant. "
    "Keep responses under 3 sentences unless asked for detail. "
    "You have access to tools for weather, web search, system control, and time.",
)

# --- TTS (Coqui optional; Edge TTS default on unsupported Python / fresh installs) ---
# JARVIS_TTS_BACKEND: auto | coqui | edge
JARVIS_TTS_BACKEND: str = os.getenv("JARVIS_TTS_BACKEND", "auto").strip().lower()
TTS_MODEL_NAME: str = os.getenv(
    "TTS_MODEL_NAME",
    "tts_models/en/ljspeech/tacotron2-DDC",
)
EDGE_TTS_VOICE: str = os.getenv("EDGE_TTS_VOICE", "en-US-GuyNeural").strip()

# --- Skills / external APIs ---
OPENWEATHER_API_KEY: str | None = os.getenv("OPENWEATHER_API_KEY")
SERPER_API_KEY: str | None = os.getenv("SERPER_API_KEY")

# --- Timeouts (seconds) ---
API_TIMEOUT_SECONDS: float = float(os.getenv("API_TIMEOUT_SECONDS", "120"))
RECORD_QUEUE_TIMEOUT: float = float(os.getenv("RECORD_QUEUE_TIMEOUT", "0.5"))
