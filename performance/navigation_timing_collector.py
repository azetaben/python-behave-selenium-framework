"""Collect browser Navigation Timing metrics via Selenium JavaScript execution."""

from __future__ import annotations

import logging
import time
from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from performance.navigation_timing_entry import NavigationTimingEntry

logger = logging.getLogger(__name__)


class NavigationTimingCollector:
    @staticmethod
    def collect(
        driver: WebDriver | None,
        scenario_name: str | None,
        trigger: str | None,
        explicit_wait_seconds: int = 15,
    ) -> NavigationTimingEntry | None:
        if driver is None:
            return None

        NavigationTimingCollector._wait_for_document_complete(driver, explicit_wait_seconds)

        raw = driver.execute_script(
            "try {"
            "  const url = window.location.href;"
            "  const nav = (performance.getEntriesByType('navigation')||[])[0];"
            "  if (!nav) { return { url: url, missing: true }; }"
            "  return {"
            "    url: url,"
            "    type: nav.type,"
            "    startTime: nav.startTime,"
            "    requestStart: nav.requestStart,"
            "    responseStart: nav.responseStart,"
            "    domContentLoadedEventEnd: nav.domContentLoadedEventEnd,"
            "    loadEventEnd: nav.loadEventEnd,"
            "    transferSize: nav.transferSize,"
            "    encodedBodySize: nav.encodedBodySize,"
            "    decodedBodySize: nav.decodedBodySize"
            "  };"
            "} catch (e) { return { error: String(e) }; }"
        )

        safe_raw = raw if isinstance(raw, dict) else {}
        request_start = NavigationTimingCollector._as_float(safe_raw.get("requestStart"))
        response_start = NavigationTimingCollector._as_float(safe_raw.get("responseStart"))
        dcl_end = NavigationTimingCollector._as_float(safe_raw.get("domContentLoadedEventEnd"))
        load_end = NavigationTimingCollector._as_float(safe_raw.get("loadEventEnd"))

        entry = NavigationTimingEntry(
            scenario_name=scenario_name,
            trigger=trigger,
            url=NavigationTimingCollector._as_str(safe_raw.get("url")),
            collected_at_epoch_ms=int(time.time() * 1000),
            transfer_size_bytes=NavigationTimingCollector._as_int(safe_raw.get("transferSize")),
            encoded_body_size_bytes=NavigationTimingCollector._as_int(safe_raw.get("encodedBodySize")),
            decoded_body_size_bytes=NavigationTimingCollector._as_int(safe_raw.get("decodedBodySize")),
            raw=safe_raw,
        )

        if request_start is not None and response_start is not None:
            entry.ttfb_ms = NavigationTimingCollector._clamp_non_negative(response_start - request_start)
        if dcl_end is not None:
            entry.dom_content_loaded_ms = NavigationTimingCollector._clamp_non_negative(dcl_end)
        if load_end is not None:
            entry.load_event_ms = NavigationTimingCollector._clamp_non_negative(load_end)

        return entry

    @staticmethod
    def _wait_for_document_complete(driver: WebDriver, timeout_seconds: int) -> None:
        try:
            WebDriverWait(driver, timeout_seconds).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except Exception as exc:
            logger.debug(
                "Timed out waiting for document.readyState=complete before collecting timings: %s",
                str(exc),
            )

    @staticmethod
    def _clamp_non_negative(value: float | None) -> float | None:
        if value is None:
            return None
        return 0.0 if value < 0 else value

    @staticmethod
    def _as_str(value: Any) -> str | None:
        return None if value is None else str(value)

    @staticmethod
    def _as_float(value: Any) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except Exception:
            return None

    @staticmethod
    def _as_int(value: Any) -> int | None:
        if value is None:
            return None
        try:
            return int(float(value))
        except Exception:
            return None

