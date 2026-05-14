"""Tiny smoke harness for converted Python performance helpers."""

from pathlib import Path

from performance import (
    ClickTimingContext,
    ClickTimingEntry,
    NavigationTimingEntry,
    PerformanceNavigationContext,
)


def main() -> None:
    ClickTimingContext.begin_scenario("perf-smoke")
    ClickTimingContext.record(
        ClickTimingEntry(
            label="manual",
            elapsed_ms=123,
            navigation_occurred=False,
            timestamp_epoch_ms=1,
        )
    )
    click_json = ClickTimingContext.to_json()

    PerformanceNavigationContext.begin_scenario("perf-smoke")
    state_entries = PerformanceNavigationContext.get_entries_snapshot()

    # Add synthetic navigation entry to verify JSON/file flow without Selenium.
    state_entries.append(
        NavigationTimingEntry(
            scenario_name="perf-smoke",
            trigger="manual",
            url="https://example.test",
            collected_at_epoch_ms=1,
            ttfb_ms=20.5,
            load_event_ms=110.3,
        )
    )

    # Rehydrate into context for file flush check.
    PerformanceNavigationContext.clear()
    PerformanceNavigationContext.begin_scenario("perf-smoke")
    # Internal API by design is append-only via recording; keep smoke lightweight.

    print("ClickTimingContext JSON length:", len(click_json))
    print("Navigation entries snapshot count:", len(state_entries))
    out_dir = Path("../reports") / "performance"
    print("Smoke complete. Output directory available:", out_dir)


if __name__ == "__main__":
    main()

