"""Browser context, storage, downloads, screenshots, and frame helpers."""

import time
from pathlib import Path
from typing import Optional, TypeAlias

from config.config import settings
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoAlertPresentException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from core.page_contract import PageContract
from utils.logger import get_logger

logger = get_logger(__name__)

Locator: TypeAlias = tuple[str, str]


class PageContextMixin(PageContract):
    """Shared browser context helpers."""

    def _switch_to_alert(self) -> Alert:
        return self.driver.switch_to.alert

    def accept_alert(self) -> str:
        try:
            alert = self._switch_to_alert()
            text = alert.text
            alert.accept()
            logger.debug("Alert accepted: %s", text)
            return text
        except (NoAlertPresentException, WebDriverException) as e:
            logger.error("Failed to accept alert: %s", e)
            raise

    def dismiss_alert(self) -> str:
        try:
            alert = self._switch_to_alert()
            text = alert.text
            alert.dismiss()
            logger.debug("Alert dismissed: %s", text)
            return text
        except (NoAlertPresentException, WebDriverException) as e:
            logger.error("Failed to dismiss alert: %s", e)
            raise

    def type_in_alert(self, text: str) -> None:
        try:
            alert = self._switch_to_alert()
            alert.send_keys(text)
            logger.debug("Typed in alert: %s", text)
        except (NoAlertPresentException, WebDriverException) as e:
            logger.error("Failed to type in alert: %s", e)
            raise

    def get_number_of_windows(self) -> int:
        count = len(self.driver.window_handles)
        logger.debug("Number of windows: %d", count)
        return count

    def switch_to_window(self, window_index: int) -> None:
        try:
            self.driver.switch_to.window(self.driver.window_handles[window_index])
            logger.debug("Switched to window %d", window_index)
        except (WebDriverException, IndexError) as e:
            logger.error("Failed to switch to window %d: %s", window_index, e)
            raise

    def close_current_window(self) -> None:
        self.driver.close()
        logger.debug("Closed current window")

    def switch_to_frame(self, locator: Locator, timeout: Optional[int] = None) -> None:
        element = self._el(locator, timeout=timeout)
        self.driver.switch_to.frame(element)
        logger.debug("Switched to frame: %s", locator)

    def switch_to_frame_by_index(self, index: int) -> None:
        self.driver.switch_to.frame(index)
        logger.debug("Switched to frame by index: %d", index)

    def switch_to_parent_frame(self) -> None:
        self.driver.switch_to.parent_frame()
        logger.debug("Switched to parent frame")

    def switch_to_default_content(self) -> None:
        self.driver.switch_to.default_content()
        logger.debug("Switched to default content")

    def get_local_storage(self, key: str) -> str:
        value = self.driver.execute_script("return localStorage.getItem(arguments[0]);", key)
        logger.debug("Got localStorage['%s'] = %s", key, value)
        return value or ""

    def set_local_storage(self, key: str, value: str) -> None:
        self.driver.execute_script("localStorage.setItem(arguments[0], arguments[1]);", key, value)
        logger.debug("Set localStorage['%s'] = %s", key, value)

    def remove_local_storage(self, key: str) -> None:
        self.driver.execute_script("localStorage.removeItem(arguments[0]);", key)
        logger.debug("Removed localStorage['%s']", key)

    def clear_local_storage(self) -> None:
        self.driver.execute_script("localStorage.clear();")
        logger.debug("Cleared localStorage")

    def get_session_storage(self, key: str) -> str:
        value = self.driver.execute_script("return sessionStorage.getItem(arguments[0]);", key)
        logger.debug("Got sessionStorage['%s'] = %s", key, value)
        return value or ""

    def set_session_storage(self, key: str, value: str) -> None:
        self.driver.execute_script("sessionStorage.setItem(arguments[0], arguments[1]);", key, value)
        logger.debug("Set sessionStorage['%s'] = %s", key, value)

    def clear_session_storage(self) -> None:
        self.driver.execute_script("sessionStorage.clear();")
        logger.debug("Cleared sessionStorage")

    @staticmethod
    def get_file_from_download(file_name: str, timeout: int = 30) -> Optional[Path]:
        download_dir = Path(settings.download_dir)
        end_time = time.time() + timeout
        while time.time() < end_time:
            file_path = download_dir / file_name
            partial_file = file_path.with_suffix(file_path.suffix + ".crdownload")
            if file_path.exists() and not partial_file.exists():
                logger.info("File downloaded: %s", file_path)
                return file_path
            time.sleep(0.5)
        logger.warning("File not found in download directory: %s", file_name)
        return None

    def upload_file(self, locator: Locator, file_path: str) -> None:
        resolved_path = Path(file_path).expanduser().resolve()
        if not resolved_path.exists():
            raise FileNotFoundError(f"Upload file does not exist: {resolved_path}")
        input_element = self._el(locator)
        input_element.send_keys(str(resolved_path))
        logger.debug("Uploaded file: %s", resolved_path)

    def take_screenshot(self, file_path: str) -> Path:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not self.driver.save_screenshot(str(path)):
            raise WebDriverException(f"Failed to save screenshot: {path}")
        logger.info("Screenshot saved: %s", path)
        return path

    def take_element_screenshot(self, locator: Locator, file_path: str) -> Path:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        element = self._el(locator)
        if not element.screenshot(str(path)):
            raise WebDriverException(f"Failed to save element screenshot: {path}")
        logger.info("Element screenshot saved: %s", path)
        return path

    def close_google_password_popup(self) -> bool:
        try:
            WebDriverWait(self.driver, 1).until(ec.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            logger.info("Dismissed JS alert (OK): %s", alert_text)
            return True
        except (TimeoutException, NoAlertPresentException):
            pass

        try:
            time.sleep(0.8)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(0.3)
            logger.info("Sent Enter key to dismiss Chrome password manager overlay (OK button)")
            return True
        except Exception as e:
            logger.debug("ActionChains Enter approach did not apply: %s", e)

        dom_selectors = [
            "[data-id='password-change-dialog']",
            "[aria-label*='Change your password']",
            "[aria-label*='Save password']",
            "[role='dialog']",
            "[role='alertdialog']",
        ]
        ok_button_selectors = [
            "button[jsname='LgbsSe']",
            "button[autofocus]",
            "button.primary",
            "button:last-of-type",
        ]
        for dialog_sel in dom_selectors:
            try:
                dialogs = self.driver.find_elements("css selector", dialog_sel)
                if not dialogs:
                    continue
                dialog_el = dialogs[0]
                for btn_sel in ok_button_selectors:
                    try:
                        ok_btn = dialog_el.find_element("css selector", btn_sel)
                        ok_btn.click()
                        logger.info("Clicked OK in DOM dialog (%s -> %s)", dialog_sel, btn_sel)
                        return True
                    except (
                        NoSuchElementException,
                        ElementNotInteractableException,
                        ElementClickInterceptedException,
                        StaleElementReferenceException,
                        WebDriverException,
                    ):
                        pass
                dialog_el.send_keys(Keys.ESCAPE)
                logger.info("Sent Escape to DOM dialog: %s", dialog_sel)
                return True
            except (
                ElementNotInteractableException,
                ElementClickInterceptedException,
                StaleElementReferenceException,
                WebDriverException,
            ):
                pass

        logger.debug("Google Password Manager dialog not detected — continuing")
        return False


