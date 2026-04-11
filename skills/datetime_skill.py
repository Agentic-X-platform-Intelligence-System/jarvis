"""Local time and date queries."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo


class DateTimeSkill:
    def run(self, params: dict[str, Any]) -> dict[str, Any]:
        tz_name = str(params.get("timezone", "") or "").strip()
        fmt = str(params.get("format", "iso") or "iso").strip().lower()

        tz: ZoneInfo | None = None
        if tz_name:
            try:
                tz = ZoneInfo(tz_name)
            except Exception:
                return {"ok": False, "error": f"Unknown timezone: {tz_name}"}

        now = datetime.now(tz) if tz else datetime.now().astimezone()

        if fmt in ("date", "day"):
            text = now.strftime("%Y-%m-%d (%A)")
        elif fmt in ("time",):
            text = now.strftime("%H:%M:%S %Z")
        else:
            text = now.isoformat(timespec="seconds")

        return {
            "ok": True,
            "timezone": str(now.tzinfo) if now.tzinfo else "local",
            "formatted": text,
            "iso": now.isoformat(timespec="seconds"),
        }
