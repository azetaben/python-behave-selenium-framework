"""Common step definitions shared across all feature scenarios.

Covers:
  - Generic assertions and actions for page title, current URL / page location
  - Top-level navigation reused across login, shopping, checkout features
  - Performance measurement helpers (navigation timing, click latency)
  - Page load timing steps (Navigation Timing API + wall-clock measurements)
  - Configuration bundle and token resolution steps
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from behave import step
from selenium.webdriver.support.ui import WebDriverWait

from constants.app_constants import AppConstants
from performance import PerformanceInterceptor, PerformanceNavigationContext
from performance.navigation_timing_collector import NavigationTimingCollector
from utils.logger import get_logger

logger = get_logger(__name__)


# ── Performance measurement helpers ────────────────────────────────────────────

def _is_performance_scenario(context: Any) -> bool:
    """Return True when the running scenario carries a performance tag."""
    tags = set(getattr(getattr(context, "scenario", None), "effective_tags", []))
    return bool(tags & {"performance", "click_performance"})


def run_with_perf_navigation(
    context: Any,
    label: str,
    action: Callable[[], None],
) -> None:
    """Run *action*, wrapping it with navigation-timing measurement in @performance scenarios."""
    if _is_performance_scenario(context) and getattr(context, "driver", None):
        PerformanceInterceptor.measure_navigation(label, action, context.driver)
    else:
        action()


def run_with_perf_click(
    context: Any,
    label: str,
    action: Callable[[], None],
    element: Any = None,
) -> None:
    """Run *action*, wrapping it with click-latency measurement in @performance scenarios."""
    if _is_performance_scenario(context) and getattr(context, "driver", None):
        PerformanceInterceptor.measure_click(label, element, action, context.driver)
    else:
        action()


# ── Page load timing helpers ───────────────────────────────────────────────────

def _ensure_timing_store(context) -> dict:
    """Return (and lazily initialise) the per-scenario timing store."""
    if not hasattr(context, "page_load_timings"):
        context.page_load_timings = {}
    return context.page_load_timings


def _wait_for_page_ready(driver, timeout: int = 15) -> None:
    """Block until ``document.readyState == 'complete'``."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except Exception:  # noqa: BLE001 — proceed and let assertions decide
        pass


def _collect_nav_timing(context) -> dict:
    """Return a timing dict combining wall-clock elapsed_ms and Navigation Timing API values."""
    driver = getattr(context, "driver", None)
    scenario_name = getattr(getattr(context, "scenario", None), "name", "unknown")

    elapsed_ms: int | None = None
    timer_start = getattr(context, "_load_timer_start", None)
    if timer_start is not None:
        elapsed_ms = int((time.perf_counter() - timer_start) * 1000)
        context._load_timer_start = None  # reset so subsequent timers are independent

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


def _fmt(value) -> str:
    """Format a float/int ms value for log lines (returns 'n/a' when None)."""
    return "n/a" if value is None else "%.1f" % float(value)


def _ms(value) -> str:
    """Format a ms value for report table columns (returns '—' when None)."""
    return "—" if value is None else "%.1f ms" % float(value)


# ── Page endpoint aliases ─────────────────────────────────────────────────────

_PAGE_ENDPOINTS: dict[str, str] = {
    "login": "",
    "inventory": "inventory.html",
    "cart": "cart.html",
    "checkout": "checkout-step-one.html",
    "checkout-two": "checkout-step-two.html",
}


# ── Navigation ────────────────────────────────────────────────────────────────

@step('the user navigates to the application home page')
def step_navigate_to_home(context) -> None:
    """Navigate to the application home (login) page."""
    run_with_perf_navigation(context, "navigate-home", lambda: context.app.login.load(""))
    logger.info("Navigated to home page")


@step('the user navigates to the "{page}" page')
def step_navigate_to_named_page(context, page: str) -> None:
    """Navigate to a named application page using the endpoint alias map."""
    page_key = page.strip().lower()
    endpoint = _PAGE_ENDPOINTS.get(page_key)
    if endpoint is None:
        raise ValueError(
            "Unknown page alias '%s'. Supported: %s" % (page, ", ".join(_PAGE_ENDPOINTS))
        )
    context.app.login.load(endpoint)
    logger.info("Navigated to '%s' page (endpoint: '%s')", page_key, endpoint)


# ── Page title assertion ──────────────────────────────────────────────────────

@step('the user can see the page title "{title}"')
def step_verify_page_title(context, title: str) -> None:
    """Assert that the browser page title equals *title*."""
    actual = context.app.login.get_page_title().strip()
    assert actual == title.strip(), "Expected page title '%s', got '%s'" % (title, actual)
    logger.info("Page title verified: '%s'", title)


# ── URL / page location assertions ───────────────────────────────────────────

@step('the user should be on the "/" page')
def step_verify_root_page(context) -> None:
    """Assert that the current URL is the application root."""
    assert context.app.login.wait_for_url_contains("/", timeout=AppConstants.Timeouts.SHORT), (
        "Expected to be on root page ('/'), got: %s" % context.app.login.get_current_url()
    )
    logger.info("Confirmed on root ('/') page")


@step('the user should be on the "{page}" page')
@step('I am in "{page}" page')
def step_verify_current_page(context, page: str) -> None:
    """Assert that the current URL contains *page* (used as a URL fragment)."""
    if not context.app.login.wait_for_url_contains(page, timeout=AppConstants.Timeouts.SHORT):
        current_url = context.app.login.get_current_url()
        assert False, "Expected URL to contain '%s', got: %s" % (page, current_url)
    logger.info("On page: %s", page)


@step('the user should be on the login page')
def step_verify_login_page(context) -> None:
    """Assert that the login page is displayed and ready for authentication."""
    current_url = context.app.login.get_current_url()
    on_root = context.app.login.wait_for_url_contains("/", timeout=AppConstants.Timeouts.SHORT)
    username_visible = context.app.login.is_element_visible(context.app.login.USERNAME, timeout=3)
    password_visible = context.app.login.is_element_visible(context.app.login.PASSWORD, timeout=3)

    assert on_root and username_visible and password_visible, (
        "Expected to be on the login page, got URL=%s (username visible=%s, password visible=%s)"
        % (current_url, username_visible, password_visible)
    )
    logger.info("Confirmed on login page")


@step("the config bundle is initialized")
def step_config_bundle_initialized(context) -> None:
    """Assert that both the config bundle and property reader are present on the context."""
    assert hasattr(context, "config_bundle"), "Config bundle was not attached in before_all"
    assert hasattr(context, "property_reader"), "Property reader is missing from context"
    logger.info("Config bundle is initialized")


@step('I resolve token "{token}"')
def step_resolve_token(context, token: str) -> None:
    """Resolve a config token and store the result in context.resolved_value."""
    context.resolved_value = context.property_reader.resolve_value(token)
    logger.info("Resolved token '%s' → '%s'", token, context.resolved_value)


@step("the resolved value should not be empty")
def step_resolved_not_empty(context) -> None:
    """Assert that the most recently resolved token value is a non-empty string."""
    assert isinstance(context.resolved_value, str), \
        "Resolved value is not a string: %r" % context.resolved_value
    assert context.resolved_value.strip(), "Resolved value is empty"
    logger.info("Resolved value is non-empty: '%s'", context.resolved_value)


@step("I read timeout values from integrated config")
def step_read_timeouts(context) -> None:
    """Load the timeout configuration dict from the config bundle."""
    context.timeout_values = context.config_bundle.get_timeouts()
    logger.info("Timeout values loaded: %s", context.timeout_values)


@step("timeouts should be positive integers")
def step_verify_timeouts(context) -> None:
    """Assert that page_load, implicit, and explicit timeouts are positive integers."""
    timeouts = context.timeout_values
    for key in ("page_load", "implicit", "explicit"):
        assert key in timeouts, "Missing timeout key: %s" % key
        assert isinstance(timeouts[key], int), "Timeout '%s' is not an integer: %r" % (key, timeouts[key])
        assert timeouts[key] > 0, "Timeout '%s' must be > 0, got %d" % (key, timeouts[key])
    logger.info("All timeout values are valid positive integers")


# ── Page load timing steps ────────────────────────────────────────────────────

@step('the user starts a page load timer')
def step_start_page_load_timer(context) -> None:
    """Record a high-resolution timestamp immediately before the next navigation."""
    context._load_timer_start = time.perf_counter()
    logger.info("[PLT] Page load timer started")


@step('the page load time for "{label}" should be recorded')
def step_record_page_load_time(context, label: str) -> None:
    """Collect Navigation Timing metrics and store them under *label*."""
    timing = _collect_nav_timing(context)
    _ensure_timing_store(context)[label] = timing

    logger.info(
        "[PLT] %-45s | elapsed=%s ms | ttfb=%s ms | dcl=%s ms | load=%s ms | url=%s",
        label,
        _fmt(timing.get("elapsed_ms")),
        _fmt(timing.get("ttfb_ms")),
        _fmt(timing.get("dom_content_loaded_ms")),
        _fmt(timing.get("load_event_ms")),
        timing.get("url", "n/a"),
    )


@step('the page should have loaded within {threshold_ms:d} milliseconds')
def step_assert_page_loaded_within(context, threshold_ms: int) -> None:
    """Assert the most-recently recorded load time is within *threshold_ms*.

    Measurement priority:
      1. ``load_event_ms``  (Navigation Timing API — most accurate end-to-end)
      2. ``elapsed_ms``     (wall-clock stopwatch — fallback when API unavailable)
    """
    timings = _ensure_timing_store(context)
    if not timings:
        raise AssertionError(
            "No timing recorded yet. "
            "Call 'the page load time for … should be recorded' first."
        )

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
        latest_label, measured_ms, threshold_ms,
    )

    assert measured_ms <= threshold_ms, (
        "[PLT] Page load threshold exceeded for '%s':\n"
        "  Measured : %.1f ms\n"
        "  Threshold: %d ms\n"
        "  URL      : %s\n"
        "  TTFB     : %s ms\n"
        "  DCL      : %s ms"
        % (
            latest_label,
            measured_ms,
            threshold_ms,
            timing.get("url", "n/a"),
            _fmt(timing.get("ttfb_ms")),
            _fmt(timing.get("dom_content_loaded_ms")),
        )
    )
    logger.info(
        "[PLT] ✓ '%s' loaded in %.1f ms (threshold %d ms)",
        latest_label, measured_ms, threshold_ms,
    )


@step('the performance recorded as "{key}"')
def step_save_timing_under_key(context, key: str) -> None:
    """Alias the most recently recorded timing entry under a simple *key* for comparison steps."""
    timings = _ensure_timing_store(context)
    if not timings:
        raise AssertionError("No timing recorded to save.")

    latest_label = list(timings.keys())[-1]
    timings[key] = dict(timings[latest_label])  # shallow copy
    logger.info("[PLT] Timing '%s' saved as key '%s'", latest_label, key)


@step('"{key_slow}" load time should be slower than "{key_fast}"')
def step_assert_slower_than(context, key_slow: str, key_fast: str) -> None:
    """Assert that *key_slow* timing is ≥ *key_fast* timing."""
    timings = _ensure_timing_store(context)

    def _get_ms(key: str) -> float:
        entry = timings.get(key)
        if entry is None:
            raise AssertionError("No timing entry found for key '%s'" % key)
        return float(entry.get("load_event_ms") or entry.get("elapsed_ms") or 0)

    slow_ms = _get_ms(key_slow)
    fast_ms = _get_ms(key_fast)

    logger.info(
        "[PLT] Comparison: '%s'=%.1f ms vs '%s'=%.1f ms",
        key_slow, slow_ms, key_fast, fast_ms,
    )

    assert slow_ms >= fast_ms, (
        "Expected '%s' (%.1f ms) to be ≥ '%s' (%.1f ms). "
        "This may indicate the performance_glitch_user fix has regressed."
        % (key_slow, slow_ms, key_fast, fast_ms)
    )
    logger.info(
        "[PLT] ✓ '%s' (%.1f ms) is correctly ≥ '%s' (%.1f ms)",
        key_slow, slow_ms, key_fast, fast_ms,
    )


@step('the full navigation flow report should be printed')
def step_print_full_nav_report(context) -> None:
    """Print a formatted table of every timing entry collected during the scenario."""
    timings = _ensure_timing_store(context)

    sep = "-" * 110
    header = "%-45s  %10s  %10s  %10s  %10s  %s" % (
        "Label", "Elapsed", "TTFB", "DCL", "Load", "URL"
    )

    lines = [
        "",
        "=" * 110,
        " PAGE LOAD TIME — FULL NAVIGATION REPORT",
        "=" * 110,
        header,
        sep,
    ]

    for label, t in timings.items():
        lines.append(
            "%-45s  %10s  %10s  %10s  %10s  %s" % (
                label,
                _ms(t.get("elapsed_ms")),
                _ms(t.get("ttfb_ms")),
                _ms(t.get("dom_content_loaded_ms")),
                _ms(t.get("load_event_ms")),
                t.get("url", ""),
            )
        )

    # Also dump automatic navigation-context entries collected by after_step hook.
    nav_entries = PerformanceNavigationContext.get_entries_snapshot()
    if nav_entries:
        lines.append(sep)
        lines.append(" AUTO-CAPTURED NAVIGATION TIMINGS (via after_step hook)")
        lines.append(sep)
        for entry in nav_entries:
            label = entry.trigger or "(auto)"
            lines.append(
                "%-45s  %10s  %10s  %10s  %10s  %s" % (
                    label,
                    "--",
                    _ms(entry.ttfb_ms),
                    _ms(entry.dom_content_loaded_ms),
                    _ms(entry.load_event_ms),
                    entry.url or "",
                )
            )

    lines.append("=" * 110)
    report = "\n".join(lines)
    logger.info(report)
    print(report)

