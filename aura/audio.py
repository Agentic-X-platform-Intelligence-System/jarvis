"""Microphone capture utilities using sounddevice + numpy (thread/queue friendly)."""

from __future__ import annotations

import logging
import queue
import threading
import time
import uuid
from pathlib import Path
from typing import Callable, Optional

import numpy as np
import sounddevice as sd

from config import (
    AUDIO_TMP_DIR,
    RECORD_CHANNELS,
    RECORD_DTYPE,
    RECORD_QUEUE_TIMEOUT,
    SAMPLE_RATE,
)

logger = logging.getLogger(__name__)


class AudioRecorderError(RuntimeError):
    """Raised when microphone recording cannot be completed."""


def _dtype_np() -> np.dtype:
    mapping = {"float32": np.float32, "int16": np.int16, "int32": np.int32}
    return np.dtype(mapping.get(RECORD_DTYPE, np.float32))


def record_seconds_blocking(
    seconds: float,
    samplerate: int = SAMPLE_RATE,
    channels: int = RECORD_CHANNELS,
) -> np.ndarray:
    """
    Record a fixed duration from the default input device.
    Blocks until recording is complete.
    """
    if seconds <= 0:
        raise ValueError("seconds must be positive")
    frames = int(max(1, round(seconds * samplerate)))
    try:
        audio = sd.rec(
            frames,
            samplerate=samplerate,
            channels=channels,
            dtype=RECORD_DTYPE,
            blocking=True,
        )
    except OSError as exc:
        raise AudioRecorderError(f"Microphone unavailable: {exc}") from exc
    except sd.PortAudioError as exc:
        raise AudioRecorderError(f"PortAudio error during recording: {exc}") from exc

    if audio is None:
        raise AudioRecorderError("sounddevice returned no buffer")

    return np.squeeze(np.asarray(audio))


def save_wav_float32_mono(path: Path, audio: np.ndarray, samplerate: int = SAMPLE_RATE) -> None:
    """Write mono float32 WAV via scipy if available, else raw numpy + simple WAV header."""
    path.parent.mkdir(parents=True, exist_ok=True)
    audio = np.asarray(audio, dtype=np.float32).reshape(-1)
    try:
        from scipy.io import wavfile

        # scipy expects float in [-1, 1] for float WAV
        wavfile.write(str(path), samplerate, audio)
        return
    except Exception:
        pass

    # Minimal PCM16 WAV fallback
    pcm = np.clip(audio, -1.0, 1.0)
    pcm16 = (pcm * 32767.0).astype(np.int16)
    _write_wav_pcm16_mono(path, pcm16, samplerate)


def _write_wav_pcm16_mono(path: Path, pcm16: np.ndarray, samplerate: int) -> None:
    import wave

    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(pcm16.tobytes())


class AudioRecorder:
    """
    Non-blocking recorder: spawns a thread to capture audio and delivers results via a queue.
    """

    def __init__(
        self,
        samplerate: int = SAMPLE_RATE,
        channels: int = RECORD_CHANNELS,
        result_queue: Optional[queue.Queue[np.ndarray]] = None,
        on_error: Optional[Callable[[BaseException], None]] = None,
    ) -> None:
        self.samplerate = samplerate
        self.channels = channels
        self._result_queue: queue.Queue[np.ndarray] = result_queue or queue.Queue(maxsize=4)
        self._on_error = on_error
        self._thread: Optional[threading.Thread] = None

    @property
    def results(self) -> queue.Queue[np.ndarray]:
        return self._result_queue

    def record_async(self, seconds: float) -> None:
        """Start a background recording; result is pushed to ``results`` queue when done."""

        def worker() -> None:
            try:
                buf = record_seconds_blocking(
                    seconds,
                    samplerate=self.samplerate,
                    channels=self.channels,
                )
                self._result_queue.put(buf)
            except BaseException as exc:
                logger.exception("Async recording failed")
                if self._on_error:
                    self._on_error(exc)

        t = threading.Thread(target=worker, name="AudioRecorder", daemon=True)
        self._thread = t
        t.start()

    def wait_result(self, timeout: Optional[float] = None) -> np.ndarray:
        """Block until a recording finishes (use after ``record_async``)."""
        return self._result_queue.get(timeout=timeout)

    def record_to_tempfile(self, seconds: float) -> Path:
        """Convenience: record blocking and write a WAV under ``AUDIO_TMP_DIR``."""
        audio = record_seconds_blocking(
            seconds,
            samplerate=self.samplerate,
            channels=self.channels,
        )
        name = f"capture_{int(time.time())}_{uuid.uuid4().hex[:8]}.wav"
        path = AUDIO_TMP_DIR / name
        save_wav_float32_mono(path, audio, samplerate=self.samplerate)
        return path


def drain_queue(q: queue.Queue, timeout: float = RECORD_QUEUE_TIMEOUT) -> None:
    """Drop pending items (e.g. stale recordings) without blocking indefinitely."""
    while True:
        try:
            q.get_nowait()
        except queue.Empty:
            return
        except Exception:
            return
