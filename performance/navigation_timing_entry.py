"""Data model for navigation performance metrics."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class NavigationTimingEntry:
    scenario_name: str | None = None
    trigger: str | None = None
    url: str | None = None
    collected_at_epoch_ms: int = 0
    ttfb_ms: float | None = None
    dom_content_loaded_ms: float | None = None
    load_event_ms: float | None = None
    transfer_size_bytes: int | None = None
    encoded_body_size_bytes: int | None = None
    decoded_body_size_bytes: int | None = None
    raw: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a dict without None values (similar to Jackson NON_NULL)."""
        return {k: v for k, v in asdict(self).items() if v is not None}

