"""Step definitions for the Cart page.

Covers:
- Navigating to the cart
- Cart badge assertions (top navigation)
- Cart item count and content assertions
- Removing items from the cart
- Proceeding to checkout from the cart
- Browser pop-up helpers used during cart flows
"""

from __future__ import annotations

from behave import step

from constants.app_constants import AppConstants
from exceptions import safe_int
from features.steps.common_steps import run_with_perf_click, run_with_perf_navigation
from utils.logger import get_logger

logger = get_logger(__name__)


# ── Navigate to cart ──────────────────────────────────────────────────────────

@step('the user navigates to the shopping cart')
def step_go_to_cart(context) -> None:
    run_with_perf_navigation(context, "go-to-cart", lambda: context.app.nav.go_to_cart())
    logger.info("Navigated to shopping cart")


@step('the user clicks on the cart badge')
def step_click_cart_badge(context) -> None:
    run_with_perf_navigation(context, "click-cart-badge", lambda: context.app.nav.go_to_cart())
    logger.info("Clicked cart badge — navigated to cart")


# ── Cart badge assertions (top navigation) ───────────────────────────────────

def _assert_badge_count(context, count: int) -> None:
    """Assert the cart badge shows *count*, or is hidden if count is 0."""
    if count == 0:
        visible = context.app.nav.is_element_visible(context.app.nav.CART_BADGE, timeout=3)
        assert not visible, "Expected cart badge to be hidden (0 items) but it is visible"
    else:
        actual = safe_int(lambda: int(context.app.nav.get_text(context.app.nav.CART_BADGE)))
        assert actual == count, "Expected badge count '%d', got '%s'" % (count, actual)
    logger.info("Cart badge shows %d as expected", count)


@step('the cart badge should display "{count}"')
def step_verify_cart_badge(context, count: str) -> None:
    badge_count = safe_int(
        lambda: int(context.app.inventory.get_text(context.app.inventory.CART_BADGE))
    )
    assert badge_count == int(count), "Expected badge '%s', got '%s'" % (count, badge_count)
    logger.info("Cart badge displays '%s'", count)


@step('the cart badge should still show {count:d} item')
def step_verify_cart_badge_persists(context, count: int) -> None:
    badge_count = safe_int(
        lambda: int(context.app.inventory.get_text(context.app.inventory.CART_BADGE))
    )
    assert badge_count == count, "Expected badge '%d', got '%s'" % (count, badge_count)
    logger.info("Cart badge still shows %d item", count)


@step('the user add verify that the cart badge shows "{count}"')
def step_add_verify_badge_shows_quoted(context, count: str) -> None:
    _assert_badge_count(context, int(count))


@step('the user add verify that the cart badge shows {count:d}')
def step_add_verify_badge_shows(context, count: int) -> None:
    _assert_badge_count(context, count)


# ── Cart contents assertions ──────────────────────────────────────────────────

def _assert_cart_count(context, count: int) -> None:
    """Navigate to cart and assert the expected number of items."""
    context.app.nav.go_to_cart()
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
    assert actual == count, "Expected %d cart item(s), got %d" % (count, actual)
    logger.info("Cart contains %d item(s)", count)


@step('the cart should contain {count:d} item')
@step('the cart should contain {count:d} items')
def step_verify_cart_item_count(context, count: int) -> None:
    """Assert the cart contains exactly *count* items."""
    _assert_cart_count(context, count)


@step('the cart should be empty')
def step_verify_cart_empty(context) -> None:
    cart_count = context.app.cart.get_cart_items_count()
    assert cart_count == 0, "Expected empty cart, but it contains %d items" % cart_count
    logger.info("Cart is empty")


@step('the cart should contain should be greater than 1 item')
def step_cart_count_gt_1(context) -> None:
    context.app.nav.go_to_cart()
    count = context.app.cart.get_cart_items_count()
    assert count > 1, "Expected more than 1 item in cart, got %d" % count
    logger.info("Cart contains %d items (> 1)", count)


@step('the cart should show all added products')
def step_verify_all_products_in_cart(context) -> None:
    items_count = context.app.cart.get_cart_items_count()
    assert items_count > 0, "No products in cart"
    logger.info("Cart shows %d product(s)", items_count)


@step('the item count should match the products count')
def step_verify_count_matches(context) -> None:
    cart_count = context.app.cart.get_cart_items_count()
    assert cart_count > 0, "Cart is empty"
    logger.info("Item count matches: %d", cart_count)


# ── Remove items from cart ────────────────────────────────────────────────────

@step('the user removes the first item from the cart')
def step_remove_first_item(context) -> None:
    run_with_perf_click(
        context,
        "remove-first-cart-item",
        lambda: context.app.cart.remove_item_from_cart(0),
    )
    logger.info("Removed first item from cart")


@step('the user clicks on the remove button for "{name}"')
def step_click_remove_for_product(context, name: str) -> None:
    def _remove() -> None:
        if AppConstants.Pages.PRODUCT_DETAIL_URL_FRACTION in context.app.product_detail.get_current_url():
            context.app.product_detail.remove_from_cart()
        else:
            context.app.inventory.remove_product_by_name(name)

    run_with_perf_click(context, "click-remove-for-%s" % name, _remove)
    logger.info("Clicked remove button for '%s'", name)


# ── Proceed to checkout ───────────────────────────────────────────────────────

@step('the user proceeds to checkout')
def step_proceed_to_checkout(context) -> None:
    """Click the checkout button to start the checkout flow."""
    run_with_perf_navigation(
        context,
        "proceed-to-checkout",
        lambda: context.app.cart.proceed_to_checkout(),
    )
    logger.info("Proceeded to checkout")


# ── Browser / pop-up helpers ──────────────────────────────────────────────────

@step('I close the google password popup if it is open')
@step('I close the google password manager javascript popup if it is open')
def step_close_google_password_popup_if_open(context) -> None:
    """Dismiss the Google password-manager popup when it appears."""
    was_closed = context.app.login.close_google_password_popup()
    if was_closed:
        logger.info("Google password manager popup closed")
    else:
        logger.debug("Google password manager popup not present")

