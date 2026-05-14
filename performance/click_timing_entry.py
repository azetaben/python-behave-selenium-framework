"""Data model for click and navigation timing entries."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class ClickTimingEntry:
    label: str | None = None
    element_description: str | None = None
    url_before: str | None = None
    url_after: str | None = None
    navigation_occurred: bool = False
    elapsed_ms: int = 0
    timestamp_epoch_ms: int = 0
    ttfb_ms: float | None = None
    dom_content_loaded_ms: float | None = None
    load_event_ms: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a dict without None values (similar to Jackson NON_NULL)."""
        return {k: v for k, v in asdict(self).items() if v is not None}

