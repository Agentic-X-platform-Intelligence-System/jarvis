"""Web search via Serper (Google) with DuckDuckGo fallback."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from typing import Any

from config import SERPER_API_KEY

logger = logging.getLogger(__name__)


class WebSearchSkill:
    def run(self, params: dict[str, Any]) -> dict[str, Any]:
        query = str(params.get("query", "")).strip()
        max_results = int(params.get("max_results", 5) or 5)
        max_results = max(1, min(max_results, 10))
        if not query:
            return {"ok": False, "error": "Missing required parameter: query"}

        if SERPER_API_KEY:
            serp = self._serper_search(query, max_results)
            if serp.get("ok"):
                return serp
            logger.info("Serper failed (%s); falling back to DuckDuckGo", serp.get("error"))

        ddg = self._duckduckgo_search(query, max_results)
        return ddg

    def _serper_search(self, query: str, max_results: int) -> dict[str, Any]:
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "num": max_results}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "X-API-KEY": SERPER_API_KEY or "",
                "Content-Type": "application/json",
                "User-Agent": "JARVIS/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            try:
                body = exc.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            return {"ok": False, "error": f"Serper HTTP {exc.code}", "details": body}
        except urllib.error.URLError as exc:
            return {"ok": False, "error": f"Serper network error: {exc.reason}"}
        except TimeoutError as exc:
            return {"ok": False, "error": f"Serper timed out: {exc}"}

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            return {"ok": False, "error": f"Invalid JSON from Serper: {exc}"}

        organic = data.get("organic") or []
        results: list[dict[str, Any]] = []
        for item in organic[:max_results]:
            results.append(
                {
                    "title": item.get("title"),
                    "snippet": item.get("snippet"),
                    "link": item.get("link"),
                }
            )
        return {"ok": True, "engine": "serper", "query": query, "results": results}

    def _duckduckgo_search(self, query: str, max_results: int) -> dict[str, Any]:
        try:
            from duckduckgo_search import DDGS  # type: ignore
        except ImportError as exc:
            return {
                "ok": False,
                "error": "duckduckgo-search is not installed, and Serper is unavailable.",
                "hint": str(exc),
            }

        results: list[dict[str, Any]] = []
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append(
                        {
                            "title": r.get("title"),
                            "snippet": r.get("body"),
                            "link": r.get("href"),
                        }
                    )
        except Exception as exc:
            logger.exception("DuckDuckGo search failed")
            return {"ok": False, "error": f"DuckDuckGo search failed: {exc}"}

        return {"ok": True, "engine": "duckduckgo", "query": query, "results": results}
