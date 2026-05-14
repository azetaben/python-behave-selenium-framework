"""Step definitions for the Checkout Step Two page (order review / overview).

Covers:
- Reviewing the order items before placing
- Clicking the Finish button to submit the order
"""

from __future__ import annotations

from behave import step

from features.steps.common_steps import run_with_perf_click
from utils.logger import get_logger

logger = get_logger(__name__)


# ── Order review ──────────────────────────────────────────────────────────────

@step('the user reviews the order')
def step_review_order(context) -> None:
    """Assert that the order review page is shown with at least one item."""
    items_count = context.app.checkout_two.get_items_count()
    assert items_count > 0, "No items found on the order review page"
    logger.info("Reviewing order with %d item(s)", items_count)


# ── Finish button ─────────────────────────────────────────────────────────────

@step('the user clicks the finish button')
def step_click_finish(context) -> None:
    """Click Finish to place the order."""
    run_with_perf_click(
        context,
        "checkout-finish",
        lambda: context.app.checkout_two.click_finish(),
    )
    logger.info("Clicked finish button")

