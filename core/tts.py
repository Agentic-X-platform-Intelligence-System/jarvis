"""Text-to-speech: Coqui TTS when available, otherwise Edge TTS (works on Python 3.13+)."""

from __future__ import annotations

import asyncio
import logging
import os
import re
import subprocess
import tempfile
import threading
from typing import Literal, Optional

import numpy as np
import sounddevice as sd

from config import EDGE_TTS_VOICE, JARVIS_TTS_BACKEND, TTS_MODEL_NAME

logger = logging.getLogger(__name__)


class TTSError(RuntimeError):
    """Raised when speech synthesis or playback fails."""


_WS_RE = re.compile(r"\s+")


def _strip_ssml_tags(text: str) -> str:
    """Remove obvious SSML tags if the model is not SSML-capable."""
    text = re.sub(r"<[^>]+>", "", text)
    return _WS_RE.sub(" ", text).strip()


BackendName = Literal["coqui", "edge"]


def _decode_mp3_to_float_mono_ffmpeg(mp3_path: str, target_sr: int = 24_000) -> tuple[np.ndarray, int]:
    """Decode MP3 to mono float32 PCM using the ffmpeg binary shipped with ``imageio-ffmpeg``."""
    try:
        import imageio_ffmpeg as ioff
    except ImportError as exc:
        raise TTSError("imageio-ffmpeg is required for Edge TTS audio decoding") from exc

    ffmpeg_exe = ioff.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe,
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        mp3_path,
        "-f",
        "f32le",
        "-ac",
        "1",
        "-ar",
        str(int(target_sr)),
        "-",
    ]
    try:
        raw = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        raise TTSError(f"ffmpeg failed to decode synthesized speech ({exc.returncode})") from exc
    except OSError as exc:
        raise TTSError(f"Could not execute ffmpeg ({ffmpeg_exe}): {exc}") from exc

    audio = np.frombuffer(raw, dtype=np.float32).copy()
    peak = float(np.max(np.abs(audio))) if audio.size else 0.0
    if peak > 1.0:
        audio = (audio / peak).astype(np.float32)
    return audio, int(target_sr)


class JarvisTTS:
    """
    Speech synthesis with pluggable backends:

    - ``coqui``: local Coqui ``TTS`` (heavy deps; not available on all Python versions)
    - ``edge``: Microsoft Edge voices via ``edge-tts`` (needs network; works on Python 3.13+)
    - ``auto``: prefer Coqui if importable, else Edge
    """

    def __init__(
        self,
        backend: str = JARVIS_TTS_BACKEND,
        model_name: str = TTS_MODEL_NAME,
        output_sample_rate: Optional[int] = None,
        edge_voice: str = EDGE_TTS_VOICE,
        edge_pcm_sample_rate: int = 24_000,
    ) -> None:
        self._backend_pref = backend.strip().lower()
        self.model_name = model_name
        self._output_sample_rate = output_sample_rate
        self._edge_voice = edge_voice.strip() or EDGE_TTS_VOICE
        self._edge_pcm_sample_rate = int(edge_pcm_sample_rate)

        self._lock = threading.Lock()
        self._resolved: Optional[BackendName] = None
        self._coqui = None

    def _ensure_coqui(self) -> None:
        if self._coqui is not None:
            return
        try:
            import torch
            from TTS.api import TTS
        except ImportError as exc:
            raise TTSError(
                "Coqui TTS is not installed. Install the optional stack (see requirements-coqui.txt) "
                "or set JARVIS_TTS_BACKEND=edge."
            ) from exc

        gpu = torch.cuda.is_available()
        logger.info("Initializing Coqui TTS model=%s gpu=%s", self.model_name, gpu)
        self._coqui = TTS(model_name=self.model_name, progress_bar=False, gpu=gpu)

        if self._output_sample_rate is None:
            sr = getattr(self._coqui, "output_sample_rate", None)
            if sr is None:
                ap = getattr(self._coqui, "ap", None)
                sr = getattr(ap, "sample_rate", None) if ap is not None else None
            self._output_sample_rate = int(sr) if sr else 22050

    def _resolve_backend(self) -> BackendName:
        if self._resolved is not None:
            return self._resolved

        pref = self._backend_pref
        if pref not in ("auto", "coqui", "edge"):
            raise TTSError(f"Invalid JARVIS_TTS_BACKEND={pref!r} (use auto|coqui|edge)")

        if pref == "coqui":
            self._ensure_coqui()
            self._resolved = "coqui"
            return self._resolved

        if pref == "edge":
            self._resolved = "edge"
            logger.info("Using Edge TTS voice=%s", self._edge_voice)
            return self._resolved

        # auto
        try:
            import importlib.util

            if importlib.util.find_spec("TTS") is not None and importlib.util.find_spec("torch") is not None:
                self._ensure_coqui()
                self._resolved = "coqui"
                logger.info("TTS backend selected: coqui (auto)")
                return self._resolved
        except TTSError as exc:
            logger.info("Coqui unavailable on auto (%s); falling back to Edge TTS", exc)
        except Exception as exc:
            logger.info("Coqui import check failed (%s); falling back to Edge TTS", exc)

        self._resolved = "edge"
        logger.info("TTS backend selected: edge (auto)")
        return self._resolved

    def _synthesize_coqui(self, text: str) -> tuple[np.ndarray, int]:
        with self._lock:
            self._ensure_coqui()
            assert self._coqui is not None
            assert self._output_sample_rate is not None
            try:
                wav = self._coqui.tts(text=text)
            except Exception as exc:
                raise TTSError(f"TTS synthesis failed: {exc}") from exc

        audio = np.asarray(wav, dtype=np.float32).reshape(-1)
        peak = float(np.max(np.abs(audio))) if audio.size else 0.0
        if peak > 1.0:
            audio = (audio / peak).astype(np.float32)
        return audio, int(self._output_sample_rate)

    def _synthesize_edge(self, text: str) -> tuple[np.ndarray, int]:
        try:
            import edge_tts
        except ImportError as exc:
            raise TTSError(
                "Edge TTS requires the edge-tts package. Install requirements.txt "
                "or set JARVIS_TTS_BACKEND=coqui with the optional Coqui stack."
            ) from exc

        async def _save_mp3(path: str) -> None:
            com = edge_tts.Communicate(text, self._edge_voice)
            await com.save(path)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            mp3_path = tmp.name

        try:
            asyncio.run(_save_mp3(mp3_path))
            return _decode_mp3_to_float_mono_ffmpeg(mp3_path, target_sr=self._edge_pcm_sample_rate)
        except TTSError:
            raise
        except Exception as exc:
            raise TTSError(f"Edge TTS synthesis failed: {exc}") from exc
        finally:
            try:
                os.remove(mp3_path)
            except OSError:
                pass

    def synthesize(self, text: str) -> tuple[np.ndarray, int]:
        """Return mono float32 audio and sample rate."""
        text = _strip_ssml_tags(text)
        if not text:
            raise TTSError("Empty text for TTS")

        backend = self._resolve_backend()
        if backend == "coqui":
            return self._synthesize_coqui(text)
        return self._synthesize_edge(text)

    def speak(self, text: str, blocking: bool = True) -> None:
        """Synthesize and play audio through the default output device."""
        audio, sr = self.synthesize(text)

        def play() -> None:
            try:
                sd.play(audio, samplerate=sr, blocking=True)
            except OSError as exc:
                raise TTSError(f"Audio output device error: {exc}") from exc
            except sd.PortAudioError as exc:
                raise TTSError(f"PortAudio playback error: {exc}") from exc

        if blocking:
            play()
        else:
            threading.Thread(target=play, name="TTSPlayback", daemon=True).start()


# Backwards-compatible name used in earlier scaffolding
CoquiTTS = JarvisTTS
