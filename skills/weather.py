"""OpenWeatherMap current weather skill."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from config import OPENWEATHER_API_KEY

logger = logging.getLogger(__name__)


class WeatherSkill:
    """Fetch current weather for a city using OpenWeatherMap One Call / weather API."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def run(self, params: dict[str, Any]) -> dict[str, Any]:
        city = str(params.get("city", "")).strip()
        units = str(params.get("units", "metric")).strip() or "metric"
        if not city:
            return {"ok": False, "error": "Missing required parameter: city"}

        if not OPENWEATHER_API_KEY:
            return {
                "ok": False,
                "error": "OPENWEATHER_API_KEY is not set in the environment (.env).",
            }

        query = urllib.parse.urlencode(
            {
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": units,
            }
        )
        url = f"{self.BASE_URL}?{query}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "JARVIS/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            body = ""
            try:
                body = exc.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            logger.warning("OpenWeather HTTP error: %s %s", exc.code, body)
            return {"ok": False, "error": f"Weather API HTTP {exc.code}", "details": body}
        except urllib.error.URLError as exc:
            logger.warning("OpenWeather network error: %s", exc)
            return {"ok": False, "error": f"Network error calling weather API: {exc.reason}"}
        except TimeoutError as exc:
            return {"ok": False, "error": f"Weather API timed out: {exc}"}

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            return {"ok": False, "error": f"Invalid JSON from weather API: {exc}"}

        if str(data.get("cod", "200")) not in ("200", 200):
            return {"ok": False, "error": data.get("message", "Unknown weather API error")}

        main = data.get("main") or {}
        wind = data.get("wind") or {}
        weather0 = (data.get("weather") or [{}])[0]

        summary = {
            "ok": True,
            "city": data.get("name"),
            "country": (data.get("sys") or {}).get("country"),
            "description": weather0.get("description"),
            "temp": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "wind_speed": wind.get("speed"),
            "units": units,
        }
        return summary
