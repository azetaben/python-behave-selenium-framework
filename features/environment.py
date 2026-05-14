"""Behave environment hooks and lifecycle configuration."""

import os
import re
import json
import uuid
from datetime import datetime
from pathlib import Path

import allure
from behave.model_core import Status

from config.config import settings
from config.integration import attach_config_to_context
from core.driver import WebDriverFactory
from pages.page_manager import PageManager
from performance.click_timing_context import ClickTimingContext
from performance.performance_navigation_context import PerformanceNavigationContext
from utils.logger import get_logger

logger = get_logger(__name__)

# Behave configuration
os.environ.setdefault('BEHAVE_DEBUG_ON_ERROR', 'true')

# Characters not allowed in Windows directory/file names
_INVALID_PATH_CHARS = re.compile(r'[<>:"/\\|?*,]')
_DEFAULT_RETENTION_DAYS = 14


def _safe_name(name: str) -> str:
    """Return a filesystem-safe version of a scenario/file name."""
    name = _INVALID_PATH_CHARS.sub('', name)   # remove forbidden chars
    name = name.replace(' ', '_')               # spaces -> underscores
    name = re.sub(r'_+', '_', name)             # collapse consecutive underscores
    return name.strip('_')


def _delete_passed_screenshots(base_dir: Path) -> None:
    """Remove legacy success screenshots so the folder keeps only relevant artifacts."""
    for screenshot in base_dir.rglob("*_PASSED.png"):
        try:
            screenshot.unlink(missing_ok=True)
        except OSError as e:
            logger.debug("Could not remove success screenshot '%s': %s", screenshot, e)


def _artifact_retention_days() -> int:
    """Resolve retention days from env var with safe fallback."""
    raw_days = os.getenv("ARTIFACT_RETENTION_DAYS", str(_DEFAULT_RETENTION_DAYS))
    try:
        days = int(raw_days)
        return days if days >= 1 else _DEFAULT_RETENTION_DAYS
    except ValueError:
        return _DEFAULT_RETENTION_DAYS


def _purge_old_artifacts(base_dir: Path, max_age_days: int, patterns: tuple[str, ...]) -> int:
    """Delete old artifacts matching glob patterns and return deleted count."""
    if not base_dir.exists():
        return 0

    threshold_ts = datetime.now().timestamp() - (max_age_days * 86400)
    deleted = 0
    seen: set[Path] = set()

    for pattern in patterns:
        for artifact in base_dir.rglob(pattern):
            if artifact in seen or not artifact.is_file():
                continue
            seen.add(artifact)
            try:
                if artifact.stat().st_mtime < threshold_ts:
                    artifact.unlink(missing_ok=True)
                    deleted += 1
            except OSError as e:
                logger.debug("Failed deleting old artifact '%s': %s", artifact, e)

    for folder in sorted(base_dir.rglob("*"), reverse=True):
        if folder.is_dir():
            try:
                folder.rmdir()
            except OSError:
                pass

    return deleted


def _write_run_metadata(reports_dir: Path, metadata: dict) -> Path:
    """Persist per-run metadata JSON and return the run-specific metadata path."""
    run_id = metadata["run_id"]
    run_metadata_path = reports_dir / f"run_metadata_{run_id}.json"
    latest_metadata_path = reports_dir / "run_metadata_latest.json"

    payload = json.dumps(metadata, indent=2)
    run_metadata_path.write_text(payload, encoding="utf-8")
    latest_metadata_path.write_text(payload, encoding="utf-8")
    return run_metadata_path


def before_all(context):
    """Initialize test environment before all scenarios."""
    logger.info("=" * 80)
    logger.info("Starting Behave Test Suite | Environment: %s", settings.environment)
    logger.info("=" * 80)

    # Make unified config APIs available in all steps/hooks.
    bundle = attach_config_to_context(context)
    logger.info(
        "Config bundle ready | implicit=%ss explicit=%ss page_load=%ss",
        bundle.get_timeouts()["implicit"],
        bundle.get_timeouts()["explicit"],
        bundle.get_timeouts()["page_load"],
    )

    # Create reports directory
    reports_dir = Path(settings.report_path)
    reports_dir.mkdir(exist_ok=True)
    screenshots_dir = reports_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    videos_dir = reports_dir / "videos"
    performance_dir = reports_dir / "performance"
    videos_dir.mkdir(exist_ok=True)
    performance_dir.mkdir(exist_ok=True)
    _delete_passed_screenshots(screenshots_dir)

    retention_days = _artifact_retention_days()
    deleted_screenshots = _purge_old_artifacts(screenshots_dir, retention_days, ("*.png", "*.jpg", "*.jpeg"))
    deleted_videos = _purge_old_artifacts(videos_dir, retention_days, ("*.mp4", "*.webm", "*.avi"))
    deleted_perf = _purge_old_artifacts(performance_dir, retention_days, ("*.json", "*.csv", "*.txt"))

    context.run_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    context.run_started_at = datetime.now().isoformat()
    context.run_stats = {"passed": 0, "failed": 0, "skipped": 0, "other": 0}
    run_metadata = {
        "run_id": context.run_id,
        "started_at": context.run_started_at,
        "environment": settings.environment,
        "browser": str(settings.browser),
        "base_url": settings.base_url,
        "report_path": str(reports_dir),
        "artifact_retention_days": retention_days,
        "purged_artifacts": {
            "screenshots": deleted_screenshots,
            "videos": deleted_videos,
            "performance": deleted_perf,
        },
    }
    context.run_metadata = run_metadata
    metadata_file = _write_run_metadata(reports_dir, run_metadata)
    logger.info("Run metadata written: %s", metadata_file)

    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)


def before_feature(context, feature):
    """Initialize before each feature file."""
    logger.info("\n%s", "-" * 80)
    logger.info("Feature: %s", feature.name)
    logger.info("%s", "-" * 80)


def before_scenario(context, scenario):
    """Initialize browser and page objects before each scenario."""
    logger.info("\n[Scenario] %s", scenario.name)

    try:
        context.scenario = scenario
        context.scenario_start_time = datetime.now()
        context.scenario_artifact_id = f"{_safe_name(scenario.name)}_{int(datetime.now().timestamp() * 1000)}"
        context.failure_screenshot_taken = False
        tags = set(getattr(scenario, "effective_tags", []))
        context.performance_enabled = "performance" in tags or "click_performance" in tags

        # Allow lightweight config scenarios that do not need Selenium.
        if "config_only" in tags:
            logger.info("Config-only scenario detected, skipping browser initialization")
            return

        # Initialize WebDriver
        context.driver = WebDriverFactory.create_driver()
        context.driver.implicitly_wait(context.config_bundle.get_timeouts()["implicit"])
        logger.info("Browser initialized: %s", settings.browser)

        # Initialize PageManager
        context.app = PageManager(context.driver)
        logger.info("Page Manager initialized")

        # Keep screenshots in a flat folder (no scenario-named subdirectories).
        context.screenshot_dir = Path(settings.report_path) / "screenshots"
        context.screenshot_dir.mkdir(parents=True, exist_ok=True)

        if context.performance_enabled:
            ClickTimingContext.begin_scenario(scenario.name)
            PerformanceNavigationContext.begin_scenario(scenario.name)
            logger.info("Performance instrumentation enabled for scenario")

    except Exception as e:
        logger.error("Failed to initialize browser: %s", e, exc_info=True)
        raise


def after_step(context, step):
    """Capture per-step navigation timings in performance scenarios."""
    try:
        if not getattr(context, "performance_enabled", False):
            return
        if not hasattr(context, "driver") or not context.driver:
            return

        trigger = f"{step.keyword.strip()} {step.name}".strip()
        PerformanceNavigationContext.record_if_url_changed(
            context.driver,
            getattr(context.scenario, "name", "scenario"),
            trigger,
        )
    except Exception as e:
        logger.debug("Performance capture skipped for step '%s': %s", getattr(step, "name", ""), e)


def after_scenario(context, scenario):
    """Cleanup after each scenario."""
    try:
        # Calculate execution time
        if hasattr(context, 'scenario_start_time'):
            execution_time = (datetime.now() - context.scenario_start_time).total_seconds()
            logger.info("[Execution Time] %.2fs", execution_time)

        if hasattr(context, "run_stats"):
            status_name = getattr(scenario.status, "name", "").lower()
            if status_name in context.run_stats:
                context.run_stats[status_name] += 1
            else:
                context.run_stats["other"] += 1

        if getattr(context, "performance_enabled", False):
            try:
                perf_dir = Path(settings.report_path) / "performance"
                perf_dir.mkdir(parents=True, exist_ok=True)
                safe_scenario = _safe_name(scenario.name)

                nav_file = PerformanceNavigationContext.flush_to_file(perf_dir)
                if nav_file:
                    logger.info("Navigation performance metrics saved: %s", nav_file)
                    allure.attach.file(
                        str(nav_file),
                        name=f"nav_timing_{safe_scenario}",
                        attachment_type=allure.attachment_type.JSON,
                    )

                click_json = ClickTimingContext.to_json()
                click_file = perf_dir / f"{int(datetime.now().timestamp() * 1000)}_{safe_scenario}_clicktimings.json"
                click_file.write_text(click_json, encoding="utf-8")
                logger.info("Click performance metrics saved: %s", click_file)
                allure.attach(
                    click_json,
                    name=f"click_timing_{safe_scenario}",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception as e:
                logger.warning("Failed to persist performance artifacts: %s", e)
            finally:
                ClickTimingContext.clear()
                PerformanceNavigationContext.clear()

        # Take one screenshot on failure if enabled and browser was started.
        if (
            scenario.status == Status.failed
            and settings.screenshot_on_failure
            and not getattr(context, "failure_screenshot_taken", False)
        ):
            if hasattr(context, 'driver') and context.driver and hasattr(context, 'screenshot_dir'):
                try:
                    run_id = getattr(context, "run_id", "run")
                    screenshot_path = context.screenshot_dir / f"{run_id}_{context.scenario_artifact_id}_FAILED.png"
                    context.driver.save_screenshot(str(screenshot_path))
                    context.failure_screenshot_taken = True
                    logger.info("Screenshot saved: %s", screenshot_path)
                    allure.attach.file(
                        str(screenshot_path),
                        name="screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except Exception as e:
                    logger.warning("Failed to capture screenshot: %s", e)

        # Intentionally skip success screenshots so reports/screenshots keeps only failures.

        # Close browser
        if hasattr(context, 'driver') and context.driver:
            try:
                context.driver.quit()
                logger.info("Browser closed")
            except Exception as e:
                logger.warning("Error closing browser: %s", e)

        logger.info("[Status] %s\n", scenario.status.name.upper())

    except Exception as e:
        logger.error("Error in after_scenario hook: %s", e, exc_info=True)


def after_feature(context, feature):
    """Cleanup after each feature."""
    logger.info("Feature '%s' completed\n", feature.name)


def after_all(context):
    """Final cleanup after all scenarios."""
    try:
        if hasattr(context, "run_metadata"):
            ended_at = datetime.now().isoformat()
            context.run_metadata["ended_at"] = ended_at
            context.run_metadata["scenario_stats"] = getattr(context, "run_stats", {})
            if hasattr(context, "run_started_at"):
                elapsed = datetime.now() - datetime.fromisoformat(context.run_started_at)
                context.run_metadata["duration_seconds"] = round(elapsed.total_seconds(), 2)

            reports_dir = Path(settings.report_path)
            metadata_file = _write_run_metadata(reports_dir, context.run_metadata)
            logger.info("Run metadata finalized: %s", metadata_file)
    except Exception as e:
        logger.warning("Unable to finalize run metadata: %s", e)

    logger.info("=" * 80)
    logger.info("Test Suite Completed")
    logger.info("=" * 80)


# Behave exception handler
def behave_exception_handler(exception, tb):
    """Custom exception handler for better logging."""
    logger.error("Exception in step: %s", exception, exc_info=(type(exception), exception, tb))
