"""Helpers to wrap step actions with optional performance interception."""

from __future__ import annotations

from collections.abc import Callable

from performance import PerformanceInterceptor


def _is_performance_scenario(context) -> bool:
    tags = set(getattr(getattr(context, "scenario", None), "effective_tags", []))
    return "performance" in tags or "click_performance" in tags


def run_with_perf_navigation(context, label: str, action: Callable[[], None]) -> None:
    """Measure a step action when running @performance scenarios, else run normally."""
    if _is_performance_scenario(context) and hasattr(context, "driver") and context.driver:
        PerformanceInterceptor.measure_navigation(label, action, context.driver)
        return
    action()


def run_with_perf_click(
    context,
    label: str,
    action: Callable[[], None],
    element=None,
) -> None:
    """Measure click latency (including non-navigation actions) in performance scenarios."""
    if _is_performance_scenario(context) and hasattr(context, "driver") and context.driver:
        PerformanceInterceptor.measure_click(label, element, action, context.driver)
        return
    action()
