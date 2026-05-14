"""Element interaction helpers for page objects."""

from typing import TypeAlias

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from core.page_contract import PageContract
from exceptions import retry_on_stale
from utils.logger import get_logger

logger = get_logger(__name__)

Locator: TypeAlias = tuple[str, str]


class PageInteractionMixin(PageContract):
    """Shared element interaction operations."""

    @retry_on_stale(max_retries=3)
    def click(self, locator: Locator) -> None:
        element = self._clickable(locator)
        element.click()
        logger.debug("Clicked element: %s", locator)

    def double_click(self, locator: Locator) -> None:
        element = self._clickable(locator)
        ActionChains(self.driver).double_click(element).perform()
        logger.debug("Double-clicked element: %s", locator)

    def right_click(self, locator: Locator) -> None:
        element = self._clickable(locator)
        ActionChains(self.driver).context_click(element).perform()
        logger.debug("Right-clicked element: %s", locator)

    def click_and_hold(self, locator: Locator, duration: float = 2) -> None:
        element = self._clickable(locator)
        actions = ActionChains(self.driver)
        actions.click_and_hold(element).pause(duration).release().perform()
        logger.debug("Click and hold for %ss: %s", duration, locator)

    def js_click(self, locator: Locator) -> None:
        element = self._el(locator)
        self.driver.execute_script("arguments[0].click();", element)
        logger.debug("JS-clicked element: %s", locator)

    @retry_on_stale(max_retries=3)
    def type_text(self, locator: Locator, text: str, clear_first: bool = True) -> None:
        element = self._clickable(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.debug("Typed '%s' into element: %s", text, locator)

    def clear_field(self, locator: Locator) -> None:
        element = self._clickable(locator)
        element.clear()
        logger.debug("Cleared field: %s", locator)

    def js_type(self, locator: Locator, text: str) -> None:
        element = self._el(locator)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, text)
        logger.debug("JS-typed '%s' into element: %s", text, locator)

    def press_key(self, locator: Locator, key: str) -> None:
        element = self._clickable(locator)
        element.send_keys(key)
        logger.debug("Pressed key in element: %s", locator)

    def press_enter(self, locator: Locator) -> None:
        self.press_key(locator, Keys.ENTER)

    def press_escape(self, locator: Locator) -> None:
        self.press_key(locator, Keys.ESCAPE)

    def press_tab(self, locator: Locator) -> None:
        self.press_key(locator, Keys.TAB)

    def send_keyboard_shortcut(self, *keys: str) -> None:
        if not keys:
            return

        if len(keys) == 1:
            ActionChains(self.driver).send_keys(keys[0]).perform()
            logger.debug("Sent keyboard key: %s", keys[0])
            return

        modifiers = keys[:-1]
        trigger_key = keys[-1]
        actions = ActionChains(self.driver)
        for modifier in modifiers:
            actions.key_down(modifier)
        actions.send_keys(trigger_key)
        for modifier in reversed(modifiers):
            actions.key_up(modifier)
        actions.perform()
        logger.debug("Sent keyboard shortcut: %s", "+".join(keys))

    def check(self, locator: Locator) -> None:
        element = self._clickable(locator)
        if not element.is_selected():
            element.click()
            logger.debug("Checked checkbox: %s", locator)
        else:
            logger.debug("Checkbox already checked: %s", locator)

    def uncheck(self, locator: Locator) -> None:
        element = self._clickable(locator)
        if element.is_selected():
            element.click()
            logger.debug("Unchecked checkbox: %s", locator)
        else:
            logger.debug("Checkbox already unchecked: %s", locator)

    def is_checked(self, locator: Locator) -> bool:
        element = self._el(locator)
        is_selected = element.is_selected()
        logger.debug("Checkbox selected: %s | %s", is_selected, locator)
        return is_selected

    def select_dropdown_by_value(self, locator: Locator, value: str) -> None:
        element = self._el(locator)
        Select(element).select_by_value(value)
        logger.debug("Selected dropdown by value '%s': %s", value, locator)

    def select_dropdown_by_visible_text(self, locator: Locator, text: str) -> None:
        element = self._el(locator)
        Select(element).select_by_visible_text(text)
        logger.debug("Selected dropdown by text '%s': %s", text, locator)

    def select_dropdown_by_index(self, locator: Locator, index: int) -> None:
        element = self._el(locator)
        Select(element).select_by_index(index)
        logger.debug("Selected dropdown by index %d: %s", index, locator)

    def get_dropdown_options(self, locator: Locator) -> list[str]:
        element = self._el(locator)
        select = Select(element)
        options = [opt.text for opt in select.options]
        logger.debug("Got %d dropdown options from %s", len(options), locator)
        return options

    def hover(self, locator: Locator) -> None:
        element = self._el(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        logger.debug("Hovered over element: %s", locator)

    def hover_and_click(self, locator: Locator) -> None:
        element = self._clickable(locator)
        ActionChains(self.driver).move_to_element(element).click().perform()
        logger.debug("Hovered and clicked element: %s", locator)

    def hover_with_offset(self, locator: Locator, x_offset: int, y_offset: int) -> None:
        element = self._el(locator)
        ActionChains(self.driver).move_to_element_with_offset(element, x_offset, y_offset).perform()
        logger.debug("Hovered with offset (%d, %d): %s", x_offset, y_offset, locator)

    def drag_and_drop(self, source_locator: Locator, target_locator: Locator) -> None:
        source = self._el(source_locator)
        target = self._el(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()
        logger.debug("Dragged from %s to %s", source_locator, target_locator)

    def drag_by_offset(self, locator: Locator, x_offset: int, y_offset: int) -> None:
        element = self._el(locator)
        ActionChains(self.driver).drag_and_drop_by_offset(element, x_offset, y_offset).perform()
        logger.debug("Dragged by offset (%d, %d): %s", x_offset, y_offset, locator)

    def scroll_to_element(self, locator: Locator) -> None:
        element = self._el(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.debug("Scrolled to element: %s", locator)

    def scroll_to_element_and_click(self, locator: Locator) -> None:
        self.scroll_to_element(locator)
        self.click(locator)

    def scroll_by(self, x: int, y: int) -> None:
        self.driver.execute_script("window.scrollBy(arguments[0], arguments[1]);", x, y)
        logger.debug("Scrolled by (%d, %d)", x, y)

    def scroll_to_top(self) -> None:
        self.driver.execute_script("window.scrollTo(0, 0);")
        logger.debug("Scrolled to top")

    def scroll_to_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logger.debug("Scrolled to bottom")

