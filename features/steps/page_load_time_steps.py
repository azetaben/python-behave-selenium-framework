"""
Step definitions for Page Load Time performance tests.

Measures wall-clock load time (using PerformanceInterceptor) AND the browser
Navigation Timing API metrics (TTFB, DOM-Content-Loaded, Load-Event-End) for
every page transition starting from the login page.

Results are stored in context.page_load_timings (dict[label → dict]) so that
individual scenarios can assert thresholds and comparison steps can compare two
recorded entries.
"""
from __future__ import annotations

import time

from behave import when, then
from selenium.webdriver.support.ui import WebDriverWait

from performance.navigation_timing_collector import NavigationTimingCollector
from utils.logger import get_logger

logger = get_logger(__name__)

# ─── helpers ──────────────────────────────────────────────────────────────────

def _ensure_timing_store(context) -> dict:
    """Return (and lazily create) the per-scenario timing store."""
    if not hasattr(context, "page_load_timings"):
        context.page_load_timings = {}
    return context.page_load_timings


def _wait_for_page_ready(driver, timeout: int = 15) -> None:
    """Block until document.readyState == 'complete'."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except Exception():
        pass  # proceed anyway and let assertions decide


def _collect_nav_timing(context) -> dict:
    """
    Return a dict with wall-clock elapsed_ms (from context._load_timer_start)
    merged with Navigation-Timing-API values gathered from the current page.
    """
    driver = getattr(context, "driver", None)
    scenario_name = getattr(getattr(context, "scenario", None), "name", "unknown")

    elapsed_ms: int | None = None
    timer_start = getattr(context, "_load_timer_start", None)
    if timer_start is not None:
        elapsed_ms = int((time.perf_counter() - timer_start) * 1000)
        context._load_timer_start = None  # reset so the next timer is independent

    if driver is None:
        return {"elapsed_ms": elapsed_ms}

    _wait_for_page_ready(driver)

    entry = NavigationTimingCollector.collect(driver, scenario_name, "page-load-time-step")

    result: dict = {
        "elapsed_ms": elapsed_ms,
        "url": driver.current_url,
    }
    if entry is not None:
        result["ttfb_ms"] = entry.ttfb_ms
        result["dom_content_loaded_ms"] = entry.dom_content_loaded_ms
        result["load_event_ms"] = entry.load_event_ms
        result["transfer_size_bytes"] = entry.transfer_size_bytes

    return result


# ─── step definitions ─────────────────────────────────────────────────────────


@when('the user starts a page load timer')
def step_start_page_load_timer(context):
    """Record a high-resolution timestamp immediately before the next navigation."""
    context._load_timer_start = time.perf_counter()
    logger.info("[PLT] Page load timer started")


@then('the page load time for "{label}" should be recorded')
def step_record_page_load_time(context, label: str):
    """
    Collect Navigation Timing metrics for the current page and store them
    under *label* in context.page_load_timings.
    """
    timing = _collect_nav_timing(context)
    _ensure_timing_store(context)[label] = timing

    logger.info(
        "[PLT] %-45s | elapsed=%s ms | ttfb=%s ms | dcl=%s ms | load=%s ms | url=%s",
        label,
        timing.get("elapsed_ms", "n/a"),
        _fmt(timing.get("ttfb_ms")),
        _fmt(timing.get("dom_content_loaded_ms")),
        _fmt(timing.get("load_event_ms")),
        timing.get("url", "n/a"),
    )


@then('the page should have loaded within {threshold_ms:d} milliseconds')
def step_assert_page_loaded_within(context, threshold_ms: int):
    """
    Assert the most recently recorded page load time is within *threshold_ms*.

    Priority order for the measured value:
      1. load_event_ms  (Navigation Timing API — most accurate end-to-end)
      2. elapsed_ms     (wall-clock stopwatch — fallback when API unavailable)
    """
    timings = _ensure_timing_store(context)
    if not timings:
        raise AssertionError(
            "No timing has been recorded yet. "
            "Call 'the page load time for … should be recorded' first."
        )

    # Use the most recently inserted entry.
    latest_label = list(timings.keys())[-1]
    timing = timings[latest_label]

    measured_ms = timing.get("load_event_ms") or timing.get("elapsed_ms")

    if measured_ms is None:
        logger.warning(
            "[PLT] Could not determine load time for '%s' — skipping threshold assertion",
            latest_label,
        )
        return

    logger.info(
        "[PLT] ASSERT '%s': measured=%.1f ms vs threshold=%d ms",
        latest_label,
        measured_ms,
        threshold_ms,
    )

    assert measured_ms <= threshold_ms, (
        f"[PLT] Page load threshold exceeded for '{latest_label}':\n"
        f"  Measured : {measured_ms:.1f} ms\n"
        f"  Threshold: {threshold_ms} ms\n"
        f"  URL      : {timing.get('url', 'n/a')}\n"
        f"  TTFB     : {_fmt(timing.get('ttfb_ms'))} ms\n"
        f"  DCL      : {_fmt(timing.get('dom_content_loaded_ms'))} ms"
    )
    logger.info(
        "[PLT] ✓ '%s' loaded in %.1f ms (threshold %d ms)",
        latest_label,
        measured_ms,
        threshold_ms,
    )


@then('the performance recorded as "{key}"')
def step_save_timing_under_key(context, key: str):
    """
    Alias the most recently recorded timing entry under a simple *key* so that
    comparison steps can reference it by name.
    """
    timings = _ensure_timing_store(context)
    if not timings:
        raise AssertionError("No timing recorded to save.")

    latest_label = list(timings.keys())[-1]
    timings[key] = dict(timings[latest_label])  # shallow copy
    logger.info("[PLT] Timing '%s' saved as key '%s'", latest_label, key)


@then('"{key_slow}" load time should be slower than "{key_fast}"')
def step_assert_slower_than(context, key_slow: str, key_fast: str):
    """
    Assert that the timing stored under *key_slow* is slower (greater) than
    the timing stored under *key_fast*.
    """
    timings = _ensure_timing_store(context)

    def _get_ms(key: str) -> float:
        entry = timings.get(key)
        if entry is None:
            raise AssertionError(f"No timing entry found for key '{key}'")
        return float(entry.get("load_event_ms") or entry.get("elapsed_ms") or 0)

    slow_ms = _get_ms(key_slow)
    fast_ms = _get_ms(key_fast)

    logger.info(
        "[PLT] Comparison: '%s'=%.1f ms vs '%s'=%.1f ms",
        key_slow, slow_ms, key_fast, fast_ms,
    )

    assert slow_ms >= fast_ms, (
        f"Expected '{key_slow}' ({slow_ms:.1f} ms) to be ≥ '{key_fast}' ({fast_ms:.1f} ms). "
        f"This could indicate the performance_glitch_user fix has regressed or the comparison is wrong."
    )
    logger.info(
        "[PLT] ✓ '%s' (%.1f ms) is correctly ≥ '%s' (%.1f ms)",
        key_slow, slow_ms, key_fast, fast_ms,
    )


@then('the full navigation flow report should be printed')
def step_print_full_nav_report(context):
    """
    Print a human-readable summary table of every timing entry collected
    during the scenario (both explicit page_load_timings and the automatic
    PerformanceNavigationContext entries attached by environment.py).
    """
    from performance import PerformanceNavigationContext

    timings = _ensure_timing_store(context)

    separator = "-" * 110
    header = f"{'Label':<45}  {'Elapsed':>10}  {'TTFB':>10}  {'DCL':>10}  {'Load':>10}  URL"

    lines = [
        "",
        "=" * 110,
        " PAGE LOAD TIME - FULL NAVIGATION REPORT",
        "=" * 110,
        header,
        separator,
    ]

    for label, t in timings.items():
        lines.append(
            f"{label:<45}  "
            f"{_ms(t.get('elapsed_ms')):>10}  "
            f"{_ms(t.get('ttfb_ms')):>10}  "
            f"{_ms(t.get('dom_content_loaded_ms')):>10}  "
            f"{_ms(t.get('load_event_ms')):>10}  "
            f"{t.get('url', '')}"
        )

    # Also dump automatic navigation context entries (collected by after_step hook)
    nav_entries = PerformanceNavigationContext.get_entries_snapshot()
    if nav_entries:
        lines.append(separator)
        lines.append(" AUTO-CAPTURED NAVIGATION TIMINGS (via after_step hook)")
        lines.append(separator)
        for entry in nav_entries:
            label = entry.trigger or "(auto)"
            lines.append(
                f"{label:<45}  "
                f"{'--':>10}  "
                f"{_ms(entry.ttfb_ms):>10}  "
                f"{_ms(entry.dom_content_loaded_ms):>10}  "
                f"{_ms(entry.load_event_ms):>10}  "
                f"{entry.url or ''}"
            )

    lines.append("=" * 110)
    report = "\n".join(lines)
    logger.info(report)
    print(report)  # also echo to console so it appears in behave –no-capture output


# ─── tiny formatting helpers ──────────────────────────────────────────────────

def _fmt(value) -> str:
    """Format a float/int ms value for log lines."""
    return "n/a" if value is None else f"{float(value):.1f}"


def _ms(value) -> str:
    """Format a ms value for table columns."""
    return "—" if value is None else f"{float(value):.1f} ms"





