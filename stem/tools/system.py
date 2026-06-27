"""System control: open apps (Windows), master volume, clipboard."""

from __future__ import annotations

import logging
import platform
import shutil
import subprocess
from typing import Any

logger = logging.getLogger(__name__)


class SystemSkill:
    """
    Cross-platform where practical; volume control is best-effort on Windows via pycaw.
    """

    def run(self, params: dict[str, Any]) -> dict[str, Any]:
        action = str(params.get("action", "")).strip().lower()
        if action == "open_application":
            return self._open_application(str(params.get("target", "")).strip())
        if action == "set_volume":
            try:
                level = int(params.get("level", 50))
            except (TypeError, ValueError):
                return {"ok": False, "error": "Invalid level; expected integer 0-100"}
            return self._set_volume(level)
        if action == "clipboard_set":
            return self._clipboard_set(str(params.get("text", "")))
        if action == "clipboard_get":
            return self._clipboard_get()
        return {"ok": False, "error": f"Unknown action: {action}"}

    def _open_application(self, target: str) -> dict[str, Any]:
        if not target:
            return {"ok": False, "error": "Missing target application name or path"}

        system = platform.system().lower()
        try:
            if system == "windows":
                # `start` accepts a window title (here empty) then the command
                subprocess.Popen(
                    ["cmd", "/c", "start", "", target],
                    shell=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    close_fds=True,
                )
            elif system == "darwin":
                subprocess.Popen(["open", "-a", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                exe = shutil.which(target) or target
                subprocess.Popen([exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            return {"ok": True, "opened": target, "os": system}
        except FileNotFoundError as exc:
            return {"ok": False, "error": f"Could not open '{target}': {exc}"}
        except OSError as exc:
            return {"ok": False, "error": f"OS error opening '{target}': {exc}"}

    def _set_volume(self, level: int) -> dict[str, Any]:
        level = max(0, min(100, int(level)))
        system = platform.system().lower()
        if system != "windows":
            return {
                "ok": False,
                "error": "Automatic master volume control is only implemented on Windows (pycaw).",
                "hint": f"Requested level={level}",
            }

        try:
            from ctypes import POINTER, cast

            from comtypes import CLSCTX_ALL  # type: ignore
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # type: ignore
        except Exception as exc:
            logger.info("pycaw/comtypes not available for volume: %s", exc)
            return {
                "ok": False,
                "error": "Volume control requires Windows packages: pycaw and comtypes.",
            }

        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)
            return {"ok": True, "level": level}
        except Exception as exc:
            logger.exception("Failed to set Windows master volume")
            return {"ok": False, "error": f"Failed to set volume: {exc}"}

    def _clipboard_set(self, text: str) -> dict[str, Any]:
        try:
            import pyperclip
        except ImportError:
            return {"ok": False, "error": "pyperclip is not installed"}

        try:
            pyperclip.copy(text)
            return {"ok": True, "clipboard": "set", "length": len(text)}
        except Exception as exc:
            return {"ok": False, "error": f"Clipboard set failed: {exc}"}

    def _clipboard_get(self) -> dict[str, Any]:
        try:
            import pyperclip
        except ImportError:
            return {"ok": False, "error": "pyperclip is not installed"}

        try:
            data = pyperclip.paste()
            return {"ok": True, "clipboard": str(data)}
        except Exception as exc:
            return {"ok": False, "error": f"Clipboard read failed: {exc}"}
