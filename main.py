"""
JARVIS orchestrator: wake word → record → STT → Claude (tools) → TTS.

Run from the project root:

    python main.py
    python main.py --no-wake
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

from config import CLAUDE_MODEL, RECORD_SECONDS_DEFAULT
from core.audio import AudioRecorder, AudioRecorderError
from core.brain import BrainError, JarvisBrain
from core.stt import STTError, WhisperSTT
from core.tts import JarvisTTS, TTSError
from core.wake_word import WakeWordListener
from memory.conversation import InteractionLogger


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def _wait_for_wake(listener: WakeWordListener, poll_s: float = 0.05) -> bool:
    """Block until wake event or listener becomes disabled."""
    while True:
        if not listener.enabled:
            return False
        if listener.wake_event.wait(timeout=poll_s):
            return True


def main() -> int:
    parser = argparse.ArgumentParser(description="JARVIS voice assistant (Python)")
    parser.add_argument("--no-wake", action="store_true", help="Manual mode (no Porcupine wake word)")
    parser.add_argument("--once", action="store_true", help="Run a single interaction then exit")
    parser.add_argument("--record-seconds", type=float, default=RECORD_SECONDS_DEFAULT)
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    _setup_logging(args.verbose)
    log = logging.getLogger("jarvis.main")

    interaction_logger = InteractionLogger()

    wake = WakeWordListener()
    wake.configure()

    use_wake = not args.no_wake and wake.enabled
    if not args.no_wake and not wake.enabled:
        log.warning("Wake word unavailable (%s). Falling back to manual mode.", wake.disabled_reason)

    listener = wake
    if use_wake:
        listener.start()

    brain: JarvisBrain | None = None
    try:
        brain = JarvisBrain()
    except BrainError as exc:
        log.error("Brain failed to initialize: %s", exc)
        if use_wake:
            listener.stop()
        return 2

    stt = WhisperSTT()
    tts = JarvisTTS()

    log.info("JARVIS ready. Model=%s", CLAUDE_MODEL)

    try:
        while True:
            if use_wake:
                log.info('Listening for wake word ("%s")…', listener.keyword_path or listener.builtin_keyword)
                ok = _wait_for_wake(listener)
                if not ok:
                    log.error("Wake listener disabled mid-run: %s", listener.disabled_reason)
                    break
                listener.clear_detection()
            else:
                try:
                    input("Press Enter to speak… ")
                except EOFError:
                    break

            try:
                audio_path = AudioRecorder().record_to_tempfile(seconds=float(args.record_seconds))
            except AudioRecorderError as exc:
                log.error("Recording failed: %s", exc)
                if args.once:
                    break
                continue

            try:
                transcript = stt.transcribe_file(audio_path)
            except STTError as exc:
                log.error("STT failed: %s", exc)
                if args.once:
                    break
                continue

            transcript = transcript.strip()
            if not transcript:
                log.warning("Empty transcript; skipping LLM call")
                if args.once:
                    break
                continue

            log.info("You said: %s", transcript)

            try:
                reply = brain.respond(transcript)
            except BrainError as exc:
                log.error("LLM failed: %s", exc)
                if args.once:
                    break
                continue

            log.info("JARVIS: %s", reply)
            interaction_logger.log(transcript, reply)

            try:
                tts.speak(reply, blocking=True)
            except TTSError as exc:
                log.error("TTS failed: %s", exc)

            if args.once:
                break

            # Avoid immediately re-triggering on wake-word audio leaking into mic
            if use_wake:
                time.sleep(0.35)

    except KeyboardInterrupt:
        log.info("Shutdown requested")
    finally:
        if use_wake:
            listener.stop()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
