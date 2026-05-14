"""Step definitions for the Checkout Complete page (order confirmation).

Covers:
- Verifying that the order was successfully placed
- Verifying the completion / confirmation message content
"""

from __future__ import annotations

from behave import step

from utils.logger import get_logger

logger = get_logger(__name__)

_COMPLETION_KEYWORDS = frozenset(
    {"thank", "complete", "order", "dispatched", "success", "confirmed"}
)


# ── Order completion assertions ───────────────────────────────────────────────

@step('the order should be successfully completed')
def step_verify_order_completed(context) -> None:
    """Verify that the order-completion page is shown."""
    assert context.app.complete.is_checkout_complete(), "Order completion not verified"
    logger.info("Order completed successfully")


@step('the completion message should be displayed')
def step_verify_completion_message(context) -> None:
    """Verify that a completion-related keyword appears in the confirmation message."""
    message = context.app.complete.get_completion_message()
    assert message, "No completion message found"
    assert any(kw in message.lower() for kw in _COMPLETION_KEYWORDS), \
        "Unexpected completion message: %s" % message
    logger.info("Completion message displayed: %s", message)

