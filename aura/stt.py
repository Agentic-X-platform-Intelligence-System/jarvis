"""faster-whisper based speech-to-text."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import numpy as np

from config import SAMPLE_RATE, WHISPER_COMPUTE_TYPE, WHISPER_DEVICE, WHISPER_MODEL_SIZE

logger = logging.getLogger(__name__)


class STTError(RuntimeError):
    """Raised when transcription fails."""


class WhisperSTT:
    """Lazy-loaded faster-whisper model wrapper."""

    def __init__(
        self,
        model_size: str = WHISPER_MODEL_SIZE,
        device: str = WHISPER_DEVICE,
        compute_type: str = WHISPER_COMPUTE_TYPE,
    ) -> None:
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self._model: Any = None

    def _ensure_model(self) -> None:
        if self._model is not None:
            return
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise STTError("faster-whisper is not installed") from exc

        logger.info(
            "Loading Whisper model=%s device=%s compute_type=%s",
            self.model_size,
            self.device,
            self.compute_type,
        )
        self._model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
        )

    def transcribe_file(
        self,
        audio_path: str | Path,
        language: Optional[str] = None,
        beam_size: int = 5,
    ) -> str:
        """Transcribe a WAV/FLAC/etc. file on disk."""
        self._ensure_model()
        path = Path(audio_path)
        if not path.is_file():
            raise STTError(f"Audio file not found: {path}")

        segments, info = self._model.transcribe(
            str(path),
            language=language,
            beam_size=beam_size,
            vad_filter=True,
        )
        logger.debug("Detected language=%s probability=%s", info.language, info.language_probability)
        parts: list[str] = []
        try:
            for seg in segments:
                parts.append(seg.text.strip())
        except Exception as exc:
            raise STTError(f"Transcription failed while iterating segments: {exc}") from exc

        text = " ".join(p for p in parts if p).strip()
        return text

    def transcribe_array(
        self,
        audio: np.ndarray,
        samplerate: int = SAMPLE_RATE,
        language: Optional[str] = None,
        beam_size: int = 5,
    ) -> str:
        """Transcribe in-memory mono float32/any array audio."""
        self._ensure_model()
        audio = np.asarray(audio, dtype=np.float32).reshape(-1)
        segments, info = self._model.transcribe(
            audio,
            language=language,
            beam_size=beam_size,
            vad_filter=True,
            sample_rate=samplerate,
        )
        logger.debug("Detected language=%s probability=%s", info.language, info.language_probability)
        parts: list[str] = []
        for seg in segments:
            parts.append(seg.text.strip())
        return " ".join(p for p in parts if p).strip()
