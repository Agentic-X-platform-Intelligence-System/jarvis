"""Legacy core.tts shim — re-exports from aura.tts."""

from aura.tts import CoquiTTS, JarvisTTS, TTSError

__all__ = ["CoquiTTS", "JarvisTTS", "TTSError"]
