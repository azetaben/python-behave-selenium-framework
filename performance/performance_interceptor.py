"""Interceptor helpers to measure click and navigation performance."""

from __future__ import annotations

import logging
import time
from typing import Callable

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from performance.click_timing_context import ClickTimingContext
from performance.click_timing_entry import ClickTimingEntry
from performance.navigation_timing_collector import NavigationTimingCollector

logger = logging.getLogger(__name__)


class PerformanceInterceptor:
    @staticmethod
    def measure_click(
        label: str,
        element: WebElement | None,
        action: Callable[[], None],
        driver: WebDriver | None,
    ) -> None:
        d = driver
        url_before = PerformanceInterceptor._safe_get_url(d)
        element_desc = PerformanceInterceptor._safe_element_desc(element)
        start_ns = time.perf_counter_ns()
        try:
            action()
        finally:
            elapsed_ms = (time.perf_counter_ns() - start_ns) // 1_000_000
            PerformanceInterceptor._capture_entry(label, element_desc, url_before, elapsed_ms, d)

    @staticmethod
    def measure_navigation(
        label: str,
        action: Callable[[], None],
        driver: WebDriver | None,
    ) -> None:
        d = driver
        url_before = PerformanceInterceptor._safe_get_url(d)
        start_ns = time.perf_counter_ns()
        try:
            action()
        finally:
            elapsed_ms = (time.perf_counter_ns() - start_ns) // 1_000_000
            PerformanceInterceptor._capture_entry(label, None, url_before, elapsed_ms, d)

    @staticmethod
    def _capture_entry(
        label: str,
        element_desc: str | None,
        url_before: str | None,
        elapsed_ms: int,
        driver: WebDriver | None,
    ) -> None:
        try:
            url_after = PerformanceInterceptor._await_url_change_or_current(driver, url_before, 500)
            nav_occurred = url_before != url_after

            entry = ClickTimingEntry(
                label=label,
                element_description=element_desc,
                url_before=url_before,
                url_after=url_after,
                navigation_occurred=nav_occurred,
                elapsed_ms=elapsed_ms,
                timestamp_epoch_ms=int(time.time() * 1000),
            )

            if nav_occurred:
                nav = NavigationTimingCollector.collect(driver, ClickTimingContext.get_scenario_name(), label)
                if nav is not None:
                    entry.ttfb_ms = nav.ttfb_ms
                    entry.dom_content_loaded_ms = nav.dom_content_loaded_ms
                    entry.load_event_ms = nav.load_event_ms

            ClickTimingContext.record(entry)

            if nav_occurred:
                logger.info(
                    "[PERF] %s | elapsed=%sms | ttfb=%sms | load=%sms | url=%s",
                    label,
                    elapsed_ms,
                    PerformanceInterceptor._fmt(entry.ttfb_ms),
                    PerformanceInterceptor._fmt(entry.load_event_ms),
                    url_after,
                )
            else:
                logger.debug("[PERF] %s | elapsed=%sms (no navigation)", label, elapsed_ms)
        except Exception as exc:
            logger.debug("[PERF] Could not record timing for '%s': %s", label, str(exc))

    @staticmethod
    def _safe_get_url(driver: WebDriver | None) -> str | None:
        try:
            return driver.current_url if driver else None
        except Exception:
            return None

    @staticmethod
    def _safe_element_desc(element: WebElement | None) -> str | None:
        if element is None:
            return None
        try:
            text = element.text
            tag = element.tag_name
            if text and text.strip():
                return f'<{tag}> "{text.strip()}"'
            element_id = element.get_dom_attribute("id") if hasattr(element, "get_dom_attribute") else element.get_attribute("id")
            if element_id and str(element_id).strip():
                return f"<{tag} id={element_id}>"
            return f"<{tag}>"
        except Exception:
            return str(element)

    @staticmethod
    def _fmt(ms: float | None) -> str:
        return "n/a" if ms is None else f"{ms:.1f}"

    @staticmethod
    def _await_url_change_or_current(
        driver: WebDriver | None,
        url_before: str | None,
        timeout_ms: int,
    ) -> str | None:
        deadline = time.time() + (timeout_ms / 1000.0)
        while time.time() < deadline:
            current = PerformanceInterceptor._safe_get_url(driver)
            if current != url_before:
                return current
            time.sleep(0.05)
        return PerformanceInterceptor._safe_get_url(driver)

