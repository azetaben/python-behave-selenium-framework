"""Thread-local context for navigation timing entries and JSON export."""

from __future__ import annotations

import json
import logging
import re
import threading
import time
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from performance.navigation_timing_collector import NavigationTimingCollector
from performance.navigation_timing_entry import NavigationTimingEntry

logger = logging.getLogger(__name__)


class _State:
    def __init__(self) -> None:
        self.entries: list[NavigationTimingEntry] = []
        self.scenario_name: str | None = None
        self.last_recorded_url: str | None = None


class PerformanceNavigationContext:
    _state = threading.local()

    @classmethod
    def _get_state(cls) -> _State:
        state = getattr(cls._state, "value", None)
        if state is None:
            state = _State()
            cls._state.value = state
        return state

    @classmethod
    def begin_scenario(cls, scenario_name: str) -> None:
        state = cls._get_state()
        state.scenario_name = scenario_name
        state.last_recorded_url = None
        state.entries.clear()

    @classmethod
    def record_if_url_changed(
        cls,
        driver: WebDriver | None,
        scenario_name: str,
        trigger: str,
    ) -> None:
        if driver is None:
            return

        try:
            current_url = driver.current_url
        except Exception:
            return

        if not current_url:
            return

        state = cls._get_state()
        if current_url == state.last_recorded_url:
            return

        entry = NavigationTimingCollector.collect(driver, scenario_name, trigger)
        if entry is None:
            state.last_recorded_url = current_url
            return

        if entry.url and entry.url == state.last_recorded_url:
            return

        state.entries.append(entry)
        state.last_recorded_url = entry.url or current_url
        logger.info(
            "[PERF] navigation recorded: url=%s, ttfbMs=%s, loadEventMs=%s",
            state.last_recorded_url,
            entry.ttfb_ms,
            entry.load_event_ms,
        )

    @classmethod
    def get_entries_snapshot(cls) -> list[NavigationTimingEntry]:
        return list(cls._get_state().entries)

    @classmethod
    def flush_to_file(cls, output_dir: Path) -> Path | None:
        state = cls._get_state()
        if not state.entries:
            return None

        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            safe_name = cls._safe_file_name(state.scenario_name or "scenario")
            timestamp = str(int(time.time() * 1000))
            out_path = output_dir / f"{timestamp}_{safe_name}_navtimings.json"
            payload = [entry.to_dict() for entry in state.entries]
            out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return out_path
        except Exception as exc:
            logger.warning("Failed to write navigation timing metrics: %s", str(exc))
            return None

    @classmethod
    def to_json(cls) -> str:
        try:
            payload = [entry.to_dict() for entry in cls.get_entries_snapshot()]
            return json.dumps(payload, indent=2)
        except Exception:
            return "[]"

    @classmethod
    def clear(cls) -> None:
        if hasattr(cls._state, "value"):
            del cls._state.value

    @staticmethod
    def _safe_file_name(value: str) -> str:
        return re.sub(r"[^a-zA-Z0-9._-]+", "_", value)

