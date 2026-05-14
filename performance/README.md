# Performance Module (Python)

This package is the Python conversion of legacy Java classes under `performance/`.

## Converted Java -> Python

- `ClickTimingContext.java` -> `click_timing_context.py`
- `ClickTimingEntry.java` -> `click_timing_entry.py`
- `NavigationTimingCollector.java` -> `navigation_timing_collector.py`
- `NavigationTimingEntry.java` -> `navigation_timing_entry.py`
- `PerformanceInterceptor.java` -> `performance_interceptor.py`
- `PerformanceNavigationContext.java` -> `performance_navigation_context.py`

## Quick Usage

```python
from performance import ClickTimingContext, PerformanceInterceptor

ClickTimingContext.begin_scenario("my-scenario")
PerformanceInterceptor.measure_navigation("open-home", lambda: driver.get("https://example.com"), driver)
print(ClickTimingContext.to_json())
```

## Smoke Test

Run the lightweight harness:

```powershell
cd C:\Users\benaz\Desktop\behave-selenium-framework
.\.venv\Scripts\python.exe run_performance_conversion_smoke.py
```

