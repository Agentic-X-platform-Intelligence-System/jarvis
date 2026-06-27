"""Legacy core.audio shim — re-exports from aura.audio."""

from aura.audio import (
    AudioRecorder,
    AudioRecorderError,
    drain_queue,
    record_seconds_blocking,
    save_wav_float32_mono,
)

__all__ = [
    "AudioRecorder",
    "AudioRecorderError",
    "drain_queue",
    "record_seconds_blocking",
    "save_wav_float32_mono",
]
