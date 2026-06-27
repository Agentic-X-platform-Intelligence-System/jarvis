"""Porcupine wake word listener (background thread + event flag)."""

from __future__ import annotations

import logging
import threading
import time
from typing import Callable, Optional

import numpy as np
import sounddevice as sd

from config import PORCUPINE_ACCESS_KEY, PORCUPINE_BUILTIN_KEYWORD, PORCUPINE_KEYWORD_PATH

logger = logging.getLogger(__name__)


class WakeWordError(RuntimeError):
    """Raised when Porcupine cannot be initialized."""


class WakeWordListener:
    """
    Listens for a wake word in a daemon thread and sets ``wake_event`` when detected.

    Audio is captured via non-blocking ``sounddevice.RawInputStream`` callbacks.
    """

    def __init__(
        self,
        access_key: Optional[str] = PORCUPINE_ACCESS_KEY,
        builtin_keyword: str = PORCUPINE_BUILTIN_KEYWORD,
        keyword_path: Optional[str] = PORCUPINE_KEYWORD_PATH,
        on_detection: Optional[Callable[[], None]] = None,
    ) -> None:
        self.access_key = access_key
        self.builtin_keyword = builtin_keyword.strip().lower()
        self.keyword_path = keyword_path
        self.on_detection = on_detection

        self.wake_event = threading.Event()
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._porcupine = None
        self._disabled_reason: Optional[str] = None  # None == configured OK / running

    @property
    def enabled(self) -> bool:
        return self._disabled_reason is None

    @property
    def disabled_reason(self) -> Optional[str]:
        return self._disabled_reason

    def configure(self) -> None:
        """
        Validate configuration early (without starting audio).

        Picovoice requires an access key. Either a built-in keyword or a ``.ppn`` path must be used.
        """
        if not self.access_key:
            self._disabled_reason = "Missing PORCUPINE_ACCESS_KEY (.env)"
            return

        if not self.keyword_path and not self.builtin_keyword:
            self._disabled_reason = "Missing Porcupine keyword configuration"
            return

        self._disabled_reason = None

    def start(self) -> None:
        self.configure()
        if self._disabled_reason:
            logger.warning("Wake word disabled: %s", self._disabled_reason)
            return

        if self._thread and self._thread.is_alive():
            return

        self._stop.clear()
        self.wake_event.clear()

        self._thread = threading.Thread(target=self._run, name="WakeWordListener", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self._thread = None
        self._destroy_porcupine()

    def clear_detection(self) -> None:
        self.wake_event.clear()

    def _destroy_porcupine(self) -> None:
        p = self._porcupine
        self._porcupine = None
        if p is not None:
            try:
                p.delete()
            except Exception:
                logger.exception("Failed to delete Porcupine instance")

    def _run(self) -> None:
        try:
            import pvporcupine
        except ImportError:
            logger.exception("pvporcupine is not installed")
            self._disabled_reason = "pvporcupine is not installed"
            return

        try:
            if self.keyword_path:
                self._porcupine = pvporcupine.create(
                    access_key=self.access_key,
                    keyword_paths=[self.keyword_path],
                )
            else:
                self._porcupine = pvporcupine.create(
                    access_key=self.access_key,
                    keywords=[self.builtin_keyword],
                )
        except Exception as exc:
            logger.exception("Failed to create Porcupine")
            self._disabled_reason = f"Porcupine init failed: {exc}"
            return

        assert self._porcupine is not None
        frame_len = int(self._porcupine.frame_length)
        sample_rate = int(self._porcupine.sample_rate)

        logger.info(
            "Wake word listening: sample_rate=%s frame_length=%s keyword=%s",
            sample_rate,
            frame_len,
            self.keyword_path or self.builtin_keyword,
        )

        def callback(indata, frames, _time, status) -> None:  # type: ignore[no-untyped-def]
            if status:
                logger.warning("Wake word audio status: %s", status)
            if self._stop.is_set() or self._porcupine is None:
                return
            try:
                pcm = np.frombuffer(indata, dtype=np.int16)
                if pcm.size != frame_len:
                    return
                keyword_index = self._porcupine.process(pcm)
                if keyword_index >= 0:
                    logger.info("Wake word detected (index=%s)", keyword_index)
                    self.wake_event.set()
                    if self.on_detection:
                        try:
                            self.on_detection()
                        except Exception:
                            logger.exception("on_detection callback failed")
            except Exception:
                logger.exception("Wake word audio callback failed")

        stream = None
        try:
            stream = sd.RawInputStream(
                samplerate=sample_rate,
                blocksize=frame_len,
                dtype="int16",
                channels=1,
                callback=callback,
            )
            stream.start()
            while not self._stop.is_set():
                time.sleep(0.05)
        except OSError as exc:
            logger.error("Microphone error in wake listener: %s", exc)
            self._disabled_reason = f"Wake listener mic error: {exc}"
        except sd.PortAudioError as exc:
            logger.error("PortAudio error in wake listener: %s", exc)
            self._disabled_reason = f"Wake listener PortAudio error: {exc}"
        finally:
            if stream is not None:
                try:
                    stream.stop()
                    stream.close()
                except Exception:
                    logger.exception("Failed to close wake word audio stream")
            self._destroy_porcupine()
