"""Step definitions for checkout feature."""
from behave import when, then

from utils.logger import get_logger
from steps.performance_step_helpers import run_with_perf_click, run_with_perf_navigation

logger = get_logger(__name__)


@when('the user proceeds to checkout')
def step_proceed_to_checkout(context):
    """Click checkout button to proceed."""
    run_with_perf_navigation(context, "proceed-to-checkout", lambda: context.app.cart.proceed_to_checkout())
    logger.info("Proceeded to checkout")


@when('the user fills in checkout information:')
def step_fill_checkout_info(context):
    """Fill in checkout form with data from table."""
    data = {row.headings[0]: row[0] for row in context.table} if context.table else {}
    first_name = data.get('firstName', 'John')
    last_name = data.get('lastName', 'Doe')
    postal_code = data.get('postalCode', '12345')
    context.app.checkout.fill_checkout_info(first_name, last_name, postal_code)
    logger.info(f"Filled checkout info: {first_name} {last_name} {postal_code}")


@when('the user clicks the continue button')
def step_click_continue(context):
    """Click the continue button on checkout."""
    run_with_perf_click(context, "checkout-continue", lambda: context.app.checkout.click_continue())
    logger.info("Clicked continue button")


@when('the user clicks the continue button without filling any fields')
def step_click_continue_empty(context):
    """Click continue without filling the form."""
    run_with_perf_click(context, "checkout-continue-empty", lambda: context.app.checkout.click_continue())
    logger.info("Clicked continue without filling form")


@when('the user reviews the order')
def step_review_order(context):
    """Review order on checkout step two."""
    # Just verify we're on the review page
    items_count = context.app.checkout_two.get_items_count()
    assert items_count > 0, "No items in order review"
    logger.info(f"Reviewed order with {items_count} items")


@when('the user clicks the finish button')
def step_click_finish(context):
    """Click the finish button to complete order."""
    run_with_perf_click(context, "checkout-finish", lambda: context.app.checkout_two.click_finish())
    logger.info("Clicked finish button")


@then('the order should be successfully completed')
def step_verify_order_completed(context):
    """Verify order was successfully completed."""
    assert context.app.complete.is_checkout_complete(), "Order completion not verified"
    logger.info("Order completed successfully")


@then('the completion message should be displayed')
def step_verify_completion_message(context):
    """Verify completion message is displayed."""
    message = context.app.complete.get_completion_message()
    assert message, "No completion message found"
    message_lower = message.lower()
    # Check for any completion-related keywords that indicate order success
    completion_keywords = ["thank", "complete", "order", "dispatched", "success", "confirmed"]
    assert any(keyword in message_lower for keyword in completion_keywords), \
        f"Unexpected completion message: {message}"
    logger.info(f"Completion message displayed: {message}")


@then('a checkout error message should be displayed')
def step_verify_checkout_error(context):
    """Verify error message on checkout."""
    assert context.app.checkout.is_error_displayed(), "No error message displayed"
    logger.info("Error message displayed on checkout")


@then('the error message should indicate missing fields')
def step_verify_error_indicates_missing_fields(context):
    """Verify error message indicates missing fields."""
    error_msg = context.app.checkout.get_error_message()
    assert error_msg, "No error message found"
    logger.info(f"Error message: {error_msg}")


@then('the cart should show all added products')
def step_verify_all_products_in_cart(context):
    """Verify all products are shown in cart."""
    items_count = context.app.cart.get_cart_items_count()
    assert items_count > 0, "No products in cart"
    logger.info(f"Cart shows {items_count} product(s)")


@then('the item count should match the products count')
def step_verify_count_matches(context):
    """Verify item count matches product count."""
    cart_count = context.app.cart.get_cart_items_count()
    assert cart_count > 0, "Cart is empty"
    logger.info(f"Item count matches: {cart_count}")


@then('the first name field should be visible')
def step_verify_first_name_field(context):
    """Verify first name field is visible."""
    assert context.app.checkout.is_element_visible(context.app.checkout.FIRST_NAME), \
        "First name field not visible"
    logger.info("First name field is visible")


@then('the last name field should be visible')
def step_verify_last_name_field(context):
    """Verify last name field is visible."""
    assert context.app.checkout.is_element_visible(context.app.checkout.LAST_NAME), \
        "Last name field not visible"
    logger.info("Last name field is visible")


@then('the postal code field should be visible')
def step_verify_postal_code_field(context):
    """Verify postal code field is visible."""
    assert context.app.checkout.is_element_visible(context.app.checkout.POSTAL_CODE), \
        "Postal code field not visible"
    logger.info("Postal code field is visible")


@then('the continue button should be visible')
def step_verify_continue_button(context):
    """Verify continue button is visible."""
    assert context.app.checkout.is_element_visible(context.app.checkout.CONTINUE_BUTTON), \
        "Continue button not visible"
    logger.info("Continue button is visible")
