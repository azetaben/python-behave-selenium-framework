"""Step definitions for the Checkout Step One page (customer information form).

Covers:
- Filling in the checkout information form (first name, last name, postal code)
- Clicking the Continue button
- Form field visibility assertions
- Validation error assertions
"""

from __future__ import annotations

from behave import step

from features.steps.common_steps import run_with_perf_click
from utils.logger import get_logger

logger = get_logger(__name__)


# ── Fill in checkout information ──────────────────────────────────────────────

@step('the user fills in checkout information:')
def step_fill_checkout_info(context) -> None:
    """Fill the checkout form from a step data table (firstName, lastName, postalCode)."""
    data = {row.headings[0]: row[0] for row in context.table} if context.table else {}
    first_name = data.get("firstName", "John")
    last_name = data.get("lastName", "Doe")
    postal_code = data.get("postalCode", "12345")
    context.app.checkout.fill_checkout_info(first_name, last_name, postal_code)
    logger.info("Filled checkout info: %s %s %s", first_name, last_name, postal_code)


# ── Continue button ───────────────────────────────────────────────────────────

@step('the user clicks the continue button')
def step_click_continue(context) -> None:
    """Click Continue on the checkout information page."""
    run_with_perf_click(
        context,
        "checkout-continue",
        lambda: context.app.checkout.click_continue(),
    )
    logger.info("Clicked continue button")


@step('the user clicks the continue button without filling any fields')
def step_click_continue_empty(context) -> None:
    """Click Continue without filling the form (triggers validation error)."""
    run_with_perf_click(
        context,
        "checkout-continue-empty",
        lambda: context.app.checkout.click_continue(),
    )
    logger.info("Clicked continue without filling form")


# ── Validation error assertions ───────────────────────────────────────────────

@step('a checkout error message should be displayed')
def step_verify_checkout_error(context) -> None:
    """Verify that an error banner appears on the checkout form."""
    assert context.app.checkout.is_error_displayed(), "No error message displayed on checkout"
    logger.info("Error message displayed on checkout")


@step('the error message should indicate missing fields')
def step_verify_error_indicates_missing_fields(context) -> None:
    """Verify that a validation error message is present."""
    error_msg = context.app.checkout.get_error_message()
    assert error_msg, "No error message found on checkout"
    logger.info("Checkout error message: %s", error_msg)


# ── Form field visibility ─────────────────────────────────────────────────────

@step('the first name field should be visible')
def step_verify_first_name_field(context) -> None:
    assert context.app.checkout.is_element_visible(context.app.checkout.FIRST_NAME), \
        "First name field not visible"
    logger.info("First name field is visible")


@step('the last name field should be visible')
def step_verify_last_name_field(context) -> None:
    assert context.app.checkout.is_element_visible(context.app.checkout.LAST_NAME), \
        "Last name field not visible"
    logger.info("Last name field is visible")


@step('the postal code field should be visible')
def step_verify_postal_code_field(context) -> None:
    assert context.app.checkout.is_element_visible(context.app.checkout.POSTAL_CODE), \
        "Postal code field not visible"
    logger.info("Postal code field is visible")


@step('the continue button should be visible')
def step_verify_continue_button(context) -> None:
    assert context.app.checkout.is_element_visible(context.app.checkout.CONTINUE_BUTTON), \
        "Continue button not visible"
    logger.info("Continue button is visible")

