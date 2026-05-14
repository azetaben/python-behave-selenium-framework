"""Step definitions for the Inventory (products list) and Product Detail pages.

Covers:
- Inventory page state assertions
- Adding products to the cart from the inventory list
- Clicking / navigating into product detail pages
- Product detail page assertions and back-navigation
"""

from __future__ import annotations

import time

from behave import step

from features.steps.common_steps import run_with_perf_click
from utils.logger import get_logger

logger = get_logger(__name__)


# ── Inventory page state ──────────────────────────────────────────────────────

@step('the user should be on the inventory page')
def step_check_inventory_page(context) -> None:
    """Verify that the user landed on the inventory page."""
    assert context.app.inventory.get_product_count() > 0, "No products found on inventory page"
    logger.info("User is on inventory page")


@step('the product inventory should be displayed')
def step_check_products_displayed(context) -> None:
    """Verify that at least one product is displayed."""
    product_count = context.app.inventory.get_product_count()
    assert product_count > 0, "No products displayed"
    logger.info("Products displayed: %d", product_count)


# ── Adding products to the cart ───────────────────────────────────────────────

@step('the user has added products to the cart')
def step_add_products_to_cart(context) -> None:
    """Add the first two products to the cart (index 0 and 1)."""
    context.app.inventory.add_product_to_cart(0)
    context.app.inventory.add_product_to_cart(1)
    logger.info("Products added to cart (indices 0, 1)")


@step('the user adds the first product to the cart')
def step_add_first_product(context) -> None:
    run_with_perf_click(context, "add-first-product", lambda: context.app.inventory.add_product_to_cart(0))
    logger.info("Added first product to cart")


@step('the user adds the second product to the cart')
def step_add_second_product(context) -> None:
    run_with_perf_click(context, "add-second-product", lambda: context.app.inventory.add_product_to_cart(1))
    logger.info("Added second product to cart")


@step('the user adds the third product to the cart')
def step_add_third_product(context) -> None:
    run_with_perf_click(context, "add-third-product", lambda: context.app.inventory.add_product_to_cart(2))
    logger.info("Added third product to cart")


@step('the user add a product item "{name}" to the cart')
@step('the user add "{name}" to the cart:')
def step_add_product_by_name(context, name: str) -> None:
    """Add a named product from the inventory list page."""
    run_with_perf_click(
        context,
        "add-product-by-name-%s" % name,
        lambda: context.app.inventory.add_product_by_name(name),
    )
    logger.info("Added '%s' to cart from inventory", name)


@step('the user adds the following products to the cart:')
def step_add_multiple_products_from_table(context) -> None:
    """Add multiple products from a data table (column: product_name)."""
    for row in context.table:
        product_name = row["product_name"].strip()
        run_with_perf_click(
            context,
            "add-product-from-table-%s" % product_name,
            lambda p=product_name: context.app.inventory.add_product_by_name(p),
        )
        logger.info("Added '%s' to cart from table", product_name)
        # Allow React state + DOM to stabilise between additions.
        time.sleep(0.75)


# ── Inventory – product navigation ───────────────────────────────────────────

@step('the user clicks on the first product')
def step_click_first_product(context) -> None:
    run_with_perf_click(
        context,
        "click-first-product",
        lambda: context.app.inventory.click(context.app.inventory.PRODUCT_NAME),
    )
    logger.info("Clicked on first product")


@step('the user clicks on the product named "{name}"')
def step_click_product_by_name(context, name: str) -> None:
    run_with_perf_click(
        context,
        "click-product-by-name-%s" % name,
        lambda: context.app.inventory.click_product_by_name(name),
    )
    logger.info("Clicked on product: %s", name)


@step('the user navigates back to the inventory')
def step_navigate_back_to_inventory(context) -> None:
    run_with_perf_click(context, "back-to-inventory", lambda: context.app.inventory.go_back())
    logger.info("Navigated back to inventory")


# ── Product detail page ───────────────────────────────────────────────────────

@step('the product details page should be displayed')
def step_verify_product_details_page(context) -> None:
    from constants.app_constants import AppConstants
    current_url = context.app.inventory.get_current_url()
    assert (
        AppConstants.Pages.INVENTORY_URL_FRACTION not in current_url
        or AppConstants.Pages.PRODUCT_DETAIL_URL_FRACTION in current_url
    ), "Product details page not displayed"
    logger.info("Product details page is displayed")


@step('the user should see product details for "{name}"')
def step_verify_product_details_visible(context, name: str) -> None:
    assert context.app.product_detail.is_product_visible(), \
        "Product details not visible for '%s'" % name
    logger.info("Product details visible for '%s'", name)


@step('the user verify that the product name is "{name}"')
def step_verify_product_name_on_detail(context, name: str) -> None:
    actual = context.app.product_detail.get_product_name().strip()
    assert actual == name.strip(), "Expected product name '%s', got '%s'" % (name, actual)
    logger.info("Product name verified: '%s'", name)


@step('the user can see "{text}" button')
def step_verify_button_visible(context, text: str) -> None:
    assert context.app.product_detail.is_back_button_visible(), \
        "'%s' button not visible" % text
    logger.info("'%s' button is visible", text)


@step('the user clicks on the "Back to products" button')
def step_click_back_to_products(context) -> None:
    run_with_perf_click(
        context,
        "click-back-to-products",
        lambda: context.app.product_detail.go_back_to_products(),
    )
    logger.info("Clicked 'Back to products'")


@step('the user add the product "{name}" to the cart')
def step_add_product_from_detail(context, name: str) -> None:
    """Add the currently displayed product from the detail page to the cart."""
    run_with_perf_click(
        context,
        "add-product-from-detail-%s" % name,
        lambda: context.app.product_detail.add_to_cart(),
    )
    logger.info("Added '%s' to cart from product detail page", name)


@step('the user can see remove button for "{name}"')
def step_verify_remove_button_visible(context, name: str) -> None:
    from constants.app_constants import AppConstants
    if AppConstants.Pages.PRODUCT_DETAIL_URL_FRACTION in context.app.product_detail.get_current_url():
        visible = context.app.product_detail.is_remove_button_visible()
    else:
        visible = context.app.inventory.is_remove_button_visible_for(name)
    assert visible, "Remove button not visible for '%s'" % name
    logger.info("Remove button visible for '%s'", name)

