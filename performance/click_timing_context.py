"""Thread-local context for click timing entries."""

from __future__ import annotations

import json
import threading
from dataclasses import asdict

from performance.click_timing_entry import ClickTimingEntry


class _State:
    def __init__(self) -> None:
        self.entries: list[ClickTimingEntry] = []
        self.scenario_name: str | None = None


class ClickTimingContext:
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
        state.entries.clear()

    @classmethod
    def record(cls, entry: ClickTimingEntry) -> None:
        cls._get_state().entries.append(entry)

    @classmethod
    def get_scenario_name(cls) -> str | None:
        return cls._get_state().scenario_name

    @classmethod
    def get_entries_snapshot(cls) -> list[ClickTimingEntry]:
        return list(cls._get_state().entries)

    @classmethod
    def to_json(cls) -> str:
        try:
            payload = [
                {k: v for k, v in asdict(entry).items() if v is not None}
                for entry in cls.get_entries_snapshot()
            ]
            return json.dumps(payload, indent=2)
        except Exception:
            return "[]"

    @classmethod
    def clear(cls) -> None:
        if hasattr(cls._state, "value"):
            del cls._state.value

