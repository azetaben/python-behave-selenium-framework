#!/usr/bin/env python
"""
Runner script for Page Load Time performance tests.

Usage
-----
  # Run all page-load-time scenarios (headless Chrome by default):
  python run_page_load_time_tests.py

  # Run with a specific browser exposed as an env variable:
  BROWSER=firefox python run_page_load_time_tests.py

  # Run only smoke scenarios:
  python run_page_load_time_tests.py --tags @Smoke

  # Run with verbose output (no output capture, show print statements):
  python run_page_load_time_tests.py --no-capture

  # Dry-run (list scenarios without running them):
  python run_page_load_time_tests.py --dry-run
"""
from __future__ import annotations

import subprocess
import sys
import os
from pathlib import Path

# ── configuration ─────────────────────────────────────────────────────────────

FEATURE_FILE = "../features/performance/page_load_time.feature"
DEFAULT_TAGS = "@page_load_time"

# Allure results go here so they can be served with `allure serve`
ALLURE_RESULTS_DIR = "reports/allure-results/page-load-time"

# ── helpers ───────────────────────────────────────────────────────────────────

def _parse_extra_args(argv: list[str]) -> tuple[list[str], list[str]]:
    """
    Separate our own flags (--tags, --no-capture, --dry-run) from the raw
    behave arguments that are passed straight through.
    """
    tags: list[str] = []
    behave_extra: list[str] = []
    dry_run = False
    no_capture = False
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--tags" and i + 1 < len(argv):
            tags.append(argv[i + 1])
            i += 2
        elif arg.startswith("--tags="):
            tags.append(arg.split("=", 1)[1])
            i += 1
        elif arg == "--dry-run":
            dry_run = True
            i += 1
        elif arg == "--no-capture":
            no_capture = True
            i += 1
        else:
            behave_extra.append(arg)
            i += 1
    extra_flags: list[str] = []
    if dry_run:
        extra_flags.append("--dry-run")
    if no_capture:
        extra_flags.append("--no-capture")
    return tags, extra_flags + behave_extra


def build_behave_command(
    tags: list[str],
    extra_flags: list[str],
    feature_file: str,
) -> list[str]:
    cmd = [sys.executable, "-m", "behave"]

    # Tags
    effective_tags = tags if tags else [DEFAULT_TAGS]
    for tag in effective_tags:
        # Behave expects tags without the leading @
        clean = tag.lstrip("@")
        cmd.extend(["--tags", clean])

    # Always include @performance so the environment.py hooks enable instrumentation
    if "performance" not in " ".join(effective_tags):
        cmd.extend(["--tags", "performance"])

    # Allure formatter
    cmd.extend([
        "--format", "allure_behave.formatter:AllureFormatter",
        "-o", ALLURE_RESULTS_DIR,
        "--format", "pretty",
        "--no-skipped",
    ])

    cmd.extend(extra_flags)
    cmd.append(feature_file)
    return cmd


# ── entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    root = Path(__file__).parent
    os.chdir(root)

    tags, extra_flags = _parse_extra_args(sys.argv[1:])
    cmd = build_behave_command(tags, extra_flags, FEATURE_FILE)

    print("=" * 80)
    print(" PAGE LOAD TIME PERFORMANCE TEST RUNNER")
    print("=" * 80)
    print(f"Feature : {FEATURE_FILE}")
    print(f"Command : {' '.join(cmd)}")
    print(f"Reports : {ALLURE_RESULTS_DIR}")
    print("=" * 80)

    Path(ALLURE_RESULTS_DIR).mkdir(parents=True, exist_ok=True)

    result = subprocess.run(cmd, cwd=str(root))

    print("\n" + "=" * 80)
    if result.returncode == 0:
        print(" ✓  All page-load-time scenarios PASSED")
        print(f"    Allure results  : {ALLURE_RESULTS_DIR}")
        print("    To open report  : allure serve " + ALLURE_RESULTS_DIR)
    else:
        print(f" ✗  Some scenarios FAILED (exit code {result.returncode})")
    print("=" * 80)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())

