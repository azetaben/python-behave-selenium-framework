"""Step definitions for login feature."""
from behave import step

from constants import SauceDemoConstants
from utils.logger import get_logger
from steps.performance_step_helpers import run_with_perf_navigation

logger = get_logger(__name__)
CONSTANTS = SauceDemoConstants.from_config()


@step('the user navigates to the application home page')
def step_navigate_to_home(context):
    """Navigate to the application home page."""
    run_with_perf_navigation(context, "navigate-home", lambda: context.app.login.load(""))
    logger.info("Navigated to home page")


@step('the user should be on the inventory page')
def step_check_inventory_page(context):
    """Verify user is on inventory page."""
    assert context.app.inventory.get_product_count() > 0, "No products found on inventory page"
    logger.info("User is on inventory page")


@step('the product inventory should be displayed')
def step_check_products_displayed(context):
    """Verify products are displayed."""
    product_count = context.app.inventory.get_product_count()
    assert product_count > 0, "No products displayed"
    logger.info(f"Products displayed: {product_count}")


@step('an error message should be displayed')
def step_check_error_displayed(context):
    """Verify error message is displayed."""
    assert context.app.login.is_error_displayed(), "Error message not displayed"
    logger.info("Error message is displayed")


@step('the error message should contain "{text}"')
def step_check_error_text(context, text):
    """Verify error message contains specific text."""
    error_msg = context.app.login.get_error_message().lower()
    assert text.lower() in error_msg, f"Error message does not contain '{text}': {error_msg}"
    logger.info(f"Error message contains '{text}'")


@step('the username field should be visible')
def step_check_username_field_visible(context):
    """Verify username field is visible."""
    assert context.app.login.is_element_visible(context.app.login.USERNAME), \
        "Username field is not visible"
    logger.info("Username field is visible")


@step('the password field should be visible')
def step_check_password_field_visible(context):
    """Verify password field is visible."""
    assert context.app.login.is_element_visible(context.app.login.PASSWORD), \
        "Password field is not visible"
    logger.info("Password field is visible")


@step('the login button should be visible')
def step_check_login_button_visible(context):
    """Verify login button is visible."""
    assert context.app.login.is_element_visible(context.app.login.LOGIN_BUTTON), \
        "Login button is not visible"
    logger.info("Login button is visible")


@step('the login error should match constant "{constant_name}"')
def step_check_error_text_from_constant(context, constant_name):
    """Verify login error text matches a named constant from SauceDemoConstants."""
    expected = getattr(CONSTANTS, constant_name, None)
    assert expected is not None, f"Unknown SauceDemoConstants key: {constant_name}"
    actual = context.app.login.get_error_message().strip()
    assert actual == expected, f"Expected exact error '{expected}', got '{actual}'"
    logger.info(f"Error matched constant '{constant_name}'")


@step('the user logs in with username ref "{username_ref}" and password ref "{password_ref}"')
def step_login_with_references(context, username_ref, password_ref):
    """Log in with refs that can be EMPTY, constants, config tokens, or literals."""

    def _resolve(value_ref: str) -> str:
        if value_ref == "EMPTY":
            return ""
        if value_ref.startswith(("faker:", "config:", "user:", "userdata:", "${")):
            return context.property_reader.resolve_value(value_ref)
        if hasattr(CONSTANTS, value_ref):
            return getattr(CONSTANTS, value_ref)
        return value_ref

    username = _resolve(username_ref)
    password = _resolve(password_ref)
    run_with_perf_navigation(
        context,
        f"login-{username_ref}",
        lambda: context.app.login.login(username, password),
    )
    logger.info("Logged in with table-driven references")
