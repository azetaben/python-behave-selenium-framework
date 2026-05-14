"""Step definitions for shopping cart feature."""
from behave import given, when, then, step

from doc.config.config import settings
from constants.AppConstants import AppConstants
from exceptions import safe_int
from features.steps.performance_step_helpers import run_with_perf_click, run_with_perf_navigation
from utils.logger import get_logger


logger = get_logger(__name__)


@given('the user has successfully logged in')
def step_user_logged_in(context):
    context.app.login.load("")
    run_with_perf_navigation(
        context,
        "login-settings-user",
        lambda: context.app.login.login(settings.test_username, settings.test_password),
    )
    assert context.app.inventory.get_product_count() > 0, "Login failed"
    logger.info("User successfully logged in")


@given('the user has added products to the cart')
def step_add_products_to_cart(context):
    context.app.inventory.add_product_to_cart(0)
    context.app.inventory.add_product_to_cart(1)
    logger.info("Products added to cart")


@when('the user adds the first product to the cart')
def step_add_first_product(context):
    run_with_perf_click(context, "add-first-product", lambda: context.app.inventory.add_product_to_cart(0))
    logger.info("Added first product to cart")


@when('the user adds the second product to the cart')
def step_add_second_product(context):
    run_with_perf_click(context, "add-second-product", lambda: context.app.inventory.add_product_to_cart(1))
    logger.info("Added second product to cart")


@when('the user adds the third product to the cart')
def step_add_third_product(context):
    run_with_perf_click(context, "add-third-product", lambda: context.app.inventory.add_product_to_cart(2))
    logger.info("Added third product to cart")


@when('the user navigates to the shopping cart')
def step_go_to_cart(context):
    run_with_perf_navigation(context, "go-to-cart", lambda: context.app.nav.go_to_cart())
    logger.info("Navigated to shopping cart")


def _assert_cart_count(context, count):
    context.app.nav.go_to_cart()

    # Stabilize on expected UI state through page-object waits.
    if count == 0:
        context.app.cart.wait_for_element_invisibility(
            context.app.cart.CART_ITEMS,
            timeout=AppConstants.Timeouts.MEDIUM,
        )
    else:
        context.app.cart.wait_for_element_count(
            context.app.cart.CART_ITEMS,
            count,
            timeout=AppConstants.Timeouts.MEDIUM,
        )

    actual = context.app.cart.get_cart_items_count()
    assert actual == count, f"Expected {count} items, got {actual}"
    logger.info(f"Cart contains {count} item(s)")


@then('the cart should contain {count:d} item')
def step_verify_cart_item_count(context, count):
    _assert_cart_count(context, count)


@then('the cart should contain {count:d} items')
def step_verify_cart_items_count(context, count):
    _assert_cart_count(context, count)


@then('the cart badge should display "{count}"')
def step_verify_cart_badge(context, count):
    badge_count = safe_int(lambda: int(context.app.inventory.get_text(context.app.inventory.CART_BADGE)))
    assert badge_count == int(count), f"Expected badge '{count}', got '{badge_count}'"
    logger.info(f"Cart badge displays '{count}'")


@when('the user removes the first item from the cart')
def step_remove_first_item(context):
    run_with_perf_click(context, "remove-first-cart-item", lambda: context.app.cart.remove_item_from_cart(0))
    logger.info("Removed first item from cart")


@then('the cart should be empty')
def step_verify_cart_empty(context):
    cart_count = context.app.cart.get_cart_items_count()
    assert cart_count == 0, f"Expected empty cart, but it contains {cart_count} items"
    logger.info("Cart is empty")


@when('the user clicks on the first product')
def step_click_first_product(context):
    run_with_perf_click(
        context,
        "click-first-product",
        lambda: context.app.inventory.click(context.app.inventory.PRODUCT_NAME),
    )
    logger.info("Clicked on first product")


@when('the user clicks on the product named "{name}"')
def step_click_product_by_name(context, name):
    run_with_perf_click(context, f"click-product-by-name-{name}", lambda: context.app.inventory.click_product_by_name(name))
    logger.info(f"Clicked on product: {name}")


@then('the product details page should be displayed')
def step_verify_product_details_page(context):
    current_url = context.app.inventory.get_current_url()
    assert (
        AppConstants.Pages.INVENTORY_URL_FRACTION not in current_url
        or AppConstants.Pages.PRODUCT_DETAIL_URL_FRACTION in current_url
    ), \
        "Product details page not displayed"
    logger.info("Product details page is displayed")


@when('the user navigates back to the inventory')
def step_navigate_back_to_inventory(context):
    run_with_perf_click(context, "back-to-inventory", lambda: context.app.inventory.go_back())
    logger.info("Navigated back to inventory")


@then('the cart badge should still show {count:d} item')
def step_verify_cart_badge_persists(context, count):
    badge_count = safe_int(lambda: int(context.app.inventory.get_text(context.app.inventory.CART_BADGE)))
    assert badge_count == count, f"Expected badge '{count}', got '{badge_count}'"
    logger.info(f"Cart badge still shows {count} item")


# ── New steps: page URL verification ─────────────────────────────────────────

@step('the user should be on the "{page}" page')
@step('I am in "{page}" page')
def step_verify_current_page(context, page):
    if not context.app.nav.wait_for_url_contains(page, timeout=AppConstants.Timeouts.SHORT):
        current_url = context.app.nav.get_current_url()
        assert False, f"Expected URL to contain '{page}', got: {current_url}"
    logger.info(f"On page: {page}")


# ── New steps: add product by name (inventory page) ──────────────────────────

@when('the user add a product item "{name}" to the cart')
@when('the user add "{name}" to the cart:')
def step_add_product_by_name(context, name):
    run_with_perf_click(context, f"add-product-by-name-{name}", lambda: context.app.inventory.add_product_by_name(name))
    logger.info(f"Added '{name}' to cart from inventory")


# ── New steps: add product by name (detail page) ─────────────────────────────

@when('the user add the product "{name}" to the cart')
def step_add_product_from_detail(context, name):
    run_with_perf_click(context, f"add-product-from-detail-{name}", lambda: context.app.product_detail.add_to_cart())
    logger.info(f"Added '{name}' to cart from product detail page")


# ── New steps: remove button visibility ──────────────────────────────────────

@step('the user can see remove button for "{name}"')
def step_verify_remove_button_visible(context, name):
    if AppConstants.Pages.PRODUCT_DETAIL_URL_FRACTION in context.app.product_detail.get_current_url():
        visible = context.app.product_detail.is_remove_button_visible()
    else:
        visible = context.app.inventory.is_remove_button_visible_for(name)
    assert visible, f"Remove button not visible for '{name}'"
    logger.info(f"Remove button visible for '{name}'")


# ── New steps: cart count assertions ─────────────────────────────────────────

@then('the cart should contain should be greater than 1 item')
def step_cart_count_gt_1(context):
    context.app.nav.go_to_cart()
    count = context.app.cart.get_cart_items_count()
    assert count > 1, f"Expected more than 1 item in cart, got {count}"
    logger.info(f"Cart contains {count} items (> 1)")


# ── New steps: product detail page assertions ─────────────────────────────────

@step('the user should see product details for "{name}"')
def step_verify_product_details_visible(context, name):
    assert context.app.product_detail.is_product_visible(), \
        f"Product details not visible for '{name}'"
    logger.info(f"Product details visible for '{name}'")


@step('the user verify that the product name is "{name}"')
def step_verify_product_name_on_detail(context, name):
    actual = context.app.product_detail.get_product_name().strip()
    assert actual == name.strip(), f"Expected product name '{name}', got '{actual}'"
    logger.info(f"Product name verified: '{name}'")


# ── New steps: cart badge count ───────────────────────────────────────────────

@step('the user add verify that the cart badge shows "{count}"')
def step_add_verify_badge_shows_quoted(context, count):
    count_int = int(count)
    if count_int == 0:
        visible = context.app.nav.is_element_visible(context.app.nav.CART_BADGE, timeout=3)
        assert not visible, "Expected cart badge to be hidden (0 items) but it is visible"
    else:
        actual = safe_int(lambda: int(context.app.nav.get_text(context.app.nav.CART_BADGE)))
        assert actual == count_int, f"Expected badge count '{count_int}', got '{actual}'"
    logger.info(f"Cart badge shows {count_int} as expected")


@step('the user add verify that the cart badge shows {count:d}')
def step_add_verify_badge_shows(context, count):
    if count == 0:
        visible = context.app.nav.is_element_visible(context.app.nav.CART_BADGE, timeout=3)
        assert not visible, "Expected cart badge to be hidden (0 items) but it is visible"
    else:
        actual = safe_int(lambda: int(context.app.nav.get_text(context.app.nav.CART_BADGE)))
        assert actual == count, f"Expected badge count '{count}', got '{actual}'"
    logger.info(f"Cart badge shows {count} as expected")


# ── New steps: Back to products button ───────────────────────────────────────

@step('the user can see "{text}" button')
def step_verify_button_visible(context, text):
    assert context.app.product_detail.is_back_button_visible(), \
        f"'{text}' button not visible"
    logger.info(f"'{text}' button is visible")


@when('the user clicks on the "Back to products" button')
def step_click_back_to_products(context):
    run_with_perf_click(context, "click-back-to-products", lambda: context.app.product_detail.go_back_to_products())
    logger.info("Clicked 'Back to products'")


# ── New steps: cart badge / remove interactions ───────────────────────────────

@when('the user clicks on the cart badge')
def step_click_cart_badge(context):
    run_with_perf_navigation(context, "click-cart-badge", lambda: context.app.nav.go_to_cart())
    logger.info("Clicked cart badge — navigated to cart")


@when('the user clicks on the remove button for "{name}"')
def step_click_remove_for_product(context, name):
    def _remove() -> None:
        if AppConstants.Pages.PRODUCT_DETAIL_URL_FRACTION in context.app.product_detail.get_current_url():
            context.app.product_detail.remove_from_cart()
        else:
            context.app.inventory.remove_product_by_name(name)

    run_with_perf_click(context, f"click-remove-for-{name}", _remove)
    logger.info(f"Clicked remove button for '{name}'")


@when('the user adds the following products to the cart:')
def step_add_multiple_products_from_table(context):
    """Add multiple products to cart from a data table."""
    import time
    for row in context.table:
        product_name = row['product_name'].strip()
        try:
            run_with_perf_click(
                context,
                f"add-product-from-table-{product_name}",
                lambda p=product_name: context.app.inventory.add_product_by_name(p),
            )
            logger.info(f"Added '{product_name}' to cart from table")
        except ValueError as e:
            logger.error(f"Failed to add product '{product_name}': {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error adding product '{product_name}': {str(e)}")
            raise
        # Wait for page to stabilize between additions
        time.sleep(0.75)  # Increased delay for React state updates and DOM stability


@given('I close the google password popup if it is open')
@given('I close the google password manager javascript popup if it is open')
def step_close_google_password_popup_if_open(context):
    """Close Google password manager popup if it appears."""
    was_closed = context.app.login.close_google_password_popup()
    if was_closed:
        logger.info("Google password manager popup closed")
    else:
        logger.info("Google password manager popup not present")
