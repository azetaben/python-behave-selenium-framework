"""Step definitions for hamburger menu / toggle sidebar interactions.

Covers:
- Opening/closing the sidebar
- Clicking sidebar menu items by text
- Verifying menu items visibility and presence
- Waiting for sidebar state changes
"""

from __future__ import annotations

from behave import step

from utils.logger import get_logger

logger = get_logger(__name__)


# ── Sidebar visibility & state ────────────────────────────────────────────────

@step('the user tap on the toggle menu button')
def step_tap_toggle_menu_button(context) -> None:
    """Tap the hamburger toggle button to open the sidebar."""
    context.app.toggle.click_toggle_menu_button()
    logger.info("Tapped toggle menu button")

@step('the hamburger menu should be visible')
def step_verify_sidebar_visible(context) -> None:
    """Verify that the sidebar menu is visible."""
    assert context.app.toggle.is_sidebar_visible(), "Sidebar is not visible"
    logger.info("Sidebar menu is visible")


@step('the hamburger menu should not be visible')
def step_verify_sidebar_not_visible(context) -> None:
    """Verify that the sidebar menu is not visible."""
    assert not context.app.toggle.is_sidebar_visible(), "Sidebar is visible but should not be"
    logger.info("Sidebar menu is not visible")


@step('the hamburger menu should be displayed')
def step_verify_sidebar_displayed(context) -> None:
    """Verify that the sidebar menu is displayed."""
    assert context.app.toggle.is_sidebar_displayed(), "Sidebar is not displayed"
    logger.info("Sidebar menu is displayed")


@step('I wait for the hamburger menu to appear')
def step_wait_for_sidebar_visible(context) -> None:
    """Wait for the sidebar menu to become visible."""
    assert context.app.toggle.wait_for_sidebar_visible(), "Sidebar did not appear"
    logger.info("Sidebar menu appeared")


@step('I wait for the hamburger menu to disappear')
def step_wait_for_sidebar_invisible(context) -> None:
    """Wait for the sidebar menu to become invisible."""
    assert context.app.toggle.wait_for_sidebar_invisible(), "Sidebar did not disappear"
    logger.info("Sidebar menu disappeared")


# ── Menu item verification ────────────────────────────────────────────────────

@step('the "{item}" menu item should be visible')
def step_verify_menu_item_visible(context, item: str) -> None:
    """Verify that a menu item is visible by its text label."""
    assert context.app.toggle.is_menu_item_visible(item), \
        "Menu item '%s' is not visible" % item
    logger.info("Menu item '%s' is visible", item)


@step('the "{item}" menu item should be present')
def step_verify_menu_item_present(context, item: str) -> None:
    """Verify that a menu item exists in the DOM by its text label."""
    assert context.app.toggle.is_menu_item_present(item), \
        "Menu item '%s' is not present" % item
    logger.info("Menu item '%s' is present", item)


@step('the "{item}" menu item should be enabled')
def step_verify_menu_item_enabled(context, item: str) -> None:
    """Verify that a menu item is enabled/clickable."""
    assert context.app.toggle.is_menu_item_enabled(item), \
        "Menu item '%s' is not enabled" % item
    logger.info("Menu item '%s' is enabled", item)


@step('all menu items should be visible')
def step_verify_all_menu_items_visible(context) -> None:
    """Verify that all menu items are visible."""
    assert context.app.toggle.verify_all_menu_items_visible(), \
        "Not all menu items are visible"
    logger.info("All menu items are visible")


@step('the user can see "<menu>" link')
def step_verify_menu_links_from_table(context) -> None:
    """Verify each menu link listed in the step table is visible."""
    expected_items = [row.cells[0].strip().strip('"') for row in context.table]
    for item in expected_items:
        assert context.app.toggle.is_menu_item_visible(item), "Menu link '%s' is not visible" % item
    logger.info("Verified menu links from table: %s", expected_items)


@step('all menu items should be present')
def step_verify_all_menu_items_present(context) -> None:
    """Verify that all menu items exist in the DOM."""
    assert context.app.toggle.verify_all_menu_items_present(), \
        "Not all menu items are present"
    logger.info("All menu items are present")


@step('the close menu button should be visible')
def step_verify_close_button_visible(context) -> None:
    """Verify that the close menu button is visible."""
    assert context.app.toggle.verify_close_button_visible(), \
        "Close button is not visible"
    logger.info("Close menu button is visible")


# ── Click menu items ──────────────────────────────────────────────────────────

@step('the user clicks on the "{item}" menu link')
def step_user_clicks_menu_link(context, item: str) -> None:
    """Click a sidebar menu link using the exact scenario phrasing."""
    context.app.toggle.click_menu_item(item)
    logger.info("Clicked menu link: '%s'", item)

@step('I click the "{item}" menu item')
def step_click_menu_item_by_text(context, item: str) -> None:
    """Click a menu item by its text label (case-insensitive)."""
    context.app.toggle.click_menu_item(item)
    logger.info("Clicked menu item: '%s'", item)


@step('I click "All Items" in the menu')
def step_click_all_items(context) -> None:
    """Click the 'All Items' menu link."""
    context.app.toggle.click_all_items()
    logger.info("Clicked 'All Items' menu link")


@step('I click "About" in the menu')
def step_click_about(context) -> None:
    """Click the 'About' menu link."""
    context.app.toggle.click_about()
    logger.info("Clicked 'About' menu link")


@step('I click "Logout" in the menu')
def step_click_logout(context) -> None:
    """Click the 'Logout' menu link."""
    context.app.toggle.click_logout()
    logger.info("Clicked 'Logout' menu link")


@step('I click "Reset App State" in the menu')
def step_click_reset_app_state(context) -> None:
    """Click the 'Reset App State' menu link."""
    context.app.toggle.click_reset_app_state()
    logger.info("Clicked 'Reset App State' menu link")


@step('I close the hamburger menu')
def step_close_menu(context) -> None:
    """Click the close menu button (X icon)."""
    context.app.toggle.click_close_menu()
    logger.info("Closed hamburger menu")


# ── Menu content verification ─────────────────────────────────────────────────

@step('the menu should contain {count:d} item')
@step('the menu should contain {count:d} items')
def step_verify_menu_item_count(context, count: int) -> None:
    """Verify the menu contains exactly *count* items."""
    actual = context.app.toggle.get_all_menu_items_count()
    assert actual == count, "Expected %d menu item(s), got %d" % (count, actual)
    logger.info("Menu contains %d item(s)", count)


@step('the menu should contain the following items:')
def step_verify_menu_contains_items(context) -> None:
    """Verify that the menu contains all items listed in the data table (column: item)."""
    expected = [row["item"].strip() for row in context.table]
    actual = context.app.toggle.get_all_menu_items_text()

    missing = [item for item in expected if item not in actual]
    assert not missing, "Menu missing items: %s" % missing
    logger.info("Menu contains all expected items: %s", expected)


# ── Session logout ────────────────────────────────────────────────────────────

@step('I log out via the menu')
def step_logout_via_menu(context) -> None:
    """Open the sidebar and click Logout."""
    context.app.toggle.wait_for_sidebar_visible()
    context.app.toggle.click_logout()
    logger.info("Logged out via sidebar menu")


@step('I reset the app state via the menu')
def step_reset_app_state_via_menu(context) -> None:
    """Open the sidebar and click Reset App State."""
    context.app.toggle.wait_for_sidebar_visible()
    context.app.toggle.click_reset_app_state()
    logger.info("Reset app state via sidebar menu")

