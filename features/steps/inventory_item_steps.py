"""Step definitions for inventory item (product detail) page specific assertions and actions."""

from __future__ import annotations

from behave import step

from features.steps.common_steps import run_with_perf_click
from utils.logger import get_logger

logger = get_logger(__name__)


@step('the inventory item page core elements should be visible')
def step_inventory_item_core_visible(context) -> None:
    """Assert that all core inventory-item elements are visible."""
    assert context.app.inventory_item.verify_all_core_elements_visible(), (
        "One or more inventory item core elements are not visible"
    )
    logger.info("Inventory item page core elements are visible")


@step('the inventory item page core elements should be present')
def step_inventory_item_core_present(context) -> None:
    """Assert that all core inventory-item elements are present in DOM."""
    assert context.app.inventory_item.verify_all_core_elements_present(), (
        "One or more inventory item core elements are not present"
    )
    logger.info("Inventory item page core elements are present")


@step('the inventory item element "{element_key}" should be visible')
def step_inventory_item_element_visible(context, element_key: str) -> None:
    """Assert a specific inventory-item element is visible by text key."""
    assert context.app.inventory_item.is_element_visible_by_text(element_key), (
        "Inventory item element '%s' is not visible" % element_key
    )
    logger.info("Inventory item element '%s' is visible", element_key)


@step('the inventory item element "{element_key}" should be present')
def step_inventory_item_element_present(context, element_key: str) -> None:
    """Assert a specific inventory-item element is present by text key."""
    assert context.app.inventory_item.is_element_present_by_text(element_key), (
        "Inventory item element '%s' is not present" % element_key
    )
    logger.info("Inventory item element '%s' is present", element_key)


@step('the inventory item name should be "{name}"')
def step_inventory_item_name(context, name: str) -> None:
    """Assert exact item name text."""
    assert context.app.inventory_item.verify_item_name(name), (
        "Inventory item name does not match '%s'" % name
    )
    logger.info("Inventory item name matched: %s", name)


@step('the inventory item description should contain "{text}"')
def step_inventory_item_description_contains(context, text: str) -> None:
    """Assert item description contains expected text fragment."""
    assert context.app.inventory_item.verify_item_description_contains(text), (
        "Inventory item description does not contain '%s'" % text
    )
    logger.info("Inventory item description contains: %s", text)


@step('the inventory item price should be "{price}"')
def step_inventory_item_price(context, price: str) -> None:
    """Assert exact item price text."""
    assert context.app.inventory_item.verify_item_price(price), (
        "Inventory item price does not match '%s'" % price
    )
    logger.info("Inventory item price matched: %s", price)


@step('the user clicks "{text}" on the inventory item page')
def step_inventory_item_click_by_text(context, text: str) -> None:
    """Click a supported inventory-item control by text key."""
    run_with_perf_click(
        context,
        "inventory-item-click-%s" % text.strip().lower().replace(" ", "-"),
        lambda: context.app.inventory_item.click_by_text(text),
    )
    logger.info("Clicked inventory item control: %s", text)


@step('the user clicks "{text}" button')
def step_inventory_item_click_button_by_text(context, text: str) -> None:
    """Click a button by text key on inventory item page."""
    run_with_perf_click(
        context,
        "inventory-item-click-%s" % text.strip().lower().replace(" ", "-"),
        lambda: context.app.inventory_item.click_by_text(text),
    )
    logger.info("Clicked button: %s", text)


@step('the user clicks add to cart button')
def step_inventory_item_click_add_to_cart_button(context) -> None:
    """Click the Add to cart button using the exact feature phrasing."""
    run_with_perf_click(
        context,
        "inventory-item-add-to-cart",
        lambda: context.app.inventory_item.click_add_to_cart(),
    )
    logger.info("Clicked add to cart button on inventory item page")


@step('the user clicks back to products on the inventory item page')
def step_inventory_item_click_back(context) -> None:
    """Click Back to products button from inventory item page."""
    run_with_perf_click(
        context,
        "inventory-item-back-to-products",
        lambda: context.app.inventory_item.click_back_to_products(),
    )
    logger.info("Clicked back to products on inventory item page")


@step('the user clicks remove on the inventory item page')
def step_inventory_item_click_remove(context) -> None:
    """Click Remove button from inventory item page."""
    run_with_perf_click(
        context,
        "inventory-item-remove",
        lambda: context.app.inventory_item.click_remove(),
    )
    logger.info("Clicked remove on inventory item page")

