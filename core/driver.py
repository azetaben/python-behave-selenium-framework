"""
WebDriver factory using match/case pattern for driver creation.

Supports Chrome, Firefox, Edge, Safari, and Selenium Grid.
"""
import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.options import Options as SafariOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config.config import settings, BrowserType
from exceptions.custom import BrowserInitError, UnsupportedBrowserError

logger = logging.getLogger(__name__)


class WebDriverFactory:
    """Factory for creating WebDriver instances."""

    @staticmethod
    def _find_cached_driver_binary(driver_folder: str, binary_name: str) -> Path | None:
        """Return the newest cached driver binary from ~/.wdm if present."""
        cache_root = Path.home() / ".wdm" / "drivers" / driver_folder
        if not cache_root.exists():
            return None

        candidates = [
            path
            for path in cache_root.rglob(binary_name)
            if path.is_file()
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda p: p.stat().st_mtime)

    @staticmethod
    def create_driver() -> webdriver.Remote:
        """
        Create and return a WebDriver instance based on settings.browser.
        
        Returns:
            webdriver.Remote: Configured WebDriver instance
            
        Raises:
            BrowserInitError: If driver initialization fails
            UnsupportedBrowserError: If browser type is not supported
        """
        try:
            match settings.browser:
                case BrowserType.CHROME:
                    return WebDriverFactory._create_chrome_driver()
                case BrowserType.FIREFOX:
                    return WebDriverFactory._create_firefox_driver()
                case BrowserType.EDGE:
                    return WebDriverFactory._create_edge_driver()
                case BrowserType.SAFARI:
                    return WebDriverFactory._create_safari_driver()
                case BrowserType.REMOTE:
                    return WebDriverFactory._create_remote_driver()
                case _:
                    raise UnsupportedBrowserError(
                        f"Unsupported browser: {settings.browser}. "
                        f"Supported: {', '.join(b.value for b in BrowserType)}"
                    )
        except (UnsupportedBrowserError, BrowserInitError):
            raise
        except Exception as e:
            raise BrowserInitError(f"Failed to create WebDriver: {str(e)}") from e
    
    @staticmethod
    def _create_chrome_driver() -> webdriver.Chrome:
        """Create Chrome WebDriver with configured options."""
        options = ChromeOptions()
        
        # Display
        if settings.headless:
            options.add_argument("--headless=new")
        
        options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
        
        # Security & Privacy
        if settings.incognito:
            options.add_argument("--incognito")
        
        if settings.ignore_certificate_errors:
            options.add_argument("--ignore-certificate-errors")
        
        # Performance
        if settings.disable_gpu:
            options.add_argument("--disable-gpu")
        
        if settings.disable_images:
            options.add_argument("--blink-settings=imagesEnabled=false")
        
        if settings.disable_javascript:
            options.add_argument("--disable-javascript")
        
        if settings.disable_extensions:
            options.add_argument("--disable-extensions")
        
        if settings.disable_notifications:
            options.add_argument("--disable-notifications")
        
        # Page load strategy
        options.page_load_strategy = settings.page_load_strategy.value
        
        # User agent
        if settings.user_agent:
            options.add_argument(f"user-agent={settings.user_agent}")
        
        # Proxy
        if settings.proxy_server:
            options.add_argument(f"--proxy-server={settings.proxy_server}")
        
        # Download directory and password manager settings
        prefs = {
            "download.default_directory": str(Path(settings.download_dir).resolve()),
            "profile.default_content_settings.popups": 0,
            # Disable password manager save prompts
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.credential_manager_enabled": False,
            # Disable "password found in data breach / change your password" warning
            "profile.password_manager_leak_detection": False,
            # Disable Safe Browsing enhanced protection password check
            "safebrowsing.enabled": False,
            "safebrowsing_without_cloud_reporting.enabled": False,
            # Disable notification popups
            "profile.default_content_setting_values.notifications": 2,
        }
        options.add_experimental_option("prefs", prefs)
        
        # Suppress password manager, sync and Safe Browsing dialogs at the browser level
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-features=PasswordCheck,SafeBrowsingEnhancedProtection,SafetyTips")
        options.add_argument("--password-store=basic")

        # Mobile emulation
        if settings.mobile_emulation_device:
            options.add_experimental_option(
                "mobileEmulation",
                {"deviceName": settings.mobile_emulation_device}
            )
        
        cached_driver = WebDriverFactory._find_cached_driver_binary("chromedriver", "chromedriver.exe")
        if cached_driver:
            logger.info("Using cached ChromeDriver: %s", cached_driver)
            service = ChromeService(str(cached_driver))
        else:
            service = ChromeService(ChromeDriverManager().install())
        logger.info(f"Chrome WebDriver created | Headless: {settings.headless}")
        return webdriver.Chrome(service=service, options=options)


    
    @staticmethod
    def _create_firefox_driver() -> webdriver.Firefox:
        """Create Firefox WebDriver with configured options."""
        options = FirefoxOptions()
        
        # Display
        if settings.headless:
            options.add_argument("--headless")
        
        # Security & Privacy
        if settings.incognito:
            options.add_argument("-private")
        
        if settings.ignore_certificate_errors:
            options.set_preference("security.insecure_field_warning.contextual.enabled", False)
        
        # Page load strategy
        options.page_load_strategy = settings.page_load_strategy.value
        
        # User agent
        if settings.user_agent:
            options.set_preference("general.useragent.override", settings.user_agent)
        
        # Proxy
        if settings.proxy_server:
            # Parse proxy server for Firefox
            if "://" in settings.proxy_server:
                proxy_url = settings.proxy_server
            else:
                proxy_url = f"http://{settings.proxy_server}"
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.http", proxy_url.split("://")[1].split(":")[0])
            options.set_preference("network.proxy.http_port", int(proxy_url.split(":")[-1]))
        
        # Download directory
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference(
            "browser.download.dir",
            str(Path(settings.download_dir).resolve())
        )
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        logger.info(f"Firefox WebDriver created | Headless: {settings.headless}")
        return driver
    
    @staticmethod
    def _create_edge_driver() -> webdriver.Edge:
        """Create Edge WebDriver with configured options."""
        options = EdgeOptions()
        
        # Display
        if settings.headless:
            options.add_argument("--headless=new")
        
        options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
        
        # Security & Privacy
        if settings.incognito:
            options.add_argument("--inprivate")
        
        if settings.ignore_certificate_errors:
            options.add_argument("--ignore-certificate-errors")
        
        # Performance
        if settings.disable_gpu:
            options.add_argument("--disable-gpu")
        
        if settings.disable_images:
            options.add_argument("--blink-settings=imagesEnabled=false")
        
        # Page load strategy
        options.page_load_strategy = settings.page_load_strategy.value
        
        # User agent
        if settings.user_agent:
            options.add_argument(f"user-agent={settings.user_agent}")
        
        # Proxy
        if settings.proxy_server:
            options.add_argument(f"--proxy-server={settings.proxy_server}")
        
        # Download directory and password manager settings
        prefs = {
            "download.default_directory": str(Path(settings.download_dir).resolve()),
            # Disable password manager and credential save prompts
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.credential_manager_enabled": False,
        }
        options.add_experimental_option("prefs", prefs)
        
        # Additional Edge arguments to suppress password manager
        options.add_argument("--disable-sync")

        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        logger.info(f"Edge WebDriver created | Headless: {settings.headless}")
        return driver
    
    @staticmethod
    def _create_safari_driver() -> webdriver.Safari:
        """Create Safari WebDriver."""
        options = SafariOptions()
        driver = webdriver.Safari(options=options)
        logger.info("Safari WebDriver created")
        return driver
    
    @staticmethod
    def _create_remote_driver() -> webdriver.Remote:
        """Create Remote WebDriver for Selenium Grid."""
        if not settings.remote_url:
            raise BrowserInitError("REMOTE_URL not configured for remote browser")
        
        options = ChromeOptions()
        if settings.headless:
            options.add_argument("--headless=new")
        
        # Disable password manager and credential save prompts
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.credential_manager_enabled": False,
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable-sync")

        driver = webdriver.Remote(
            command_executor=settings.remote_url,
            options=options
        )
        
        logger.info(f"Remote WebDriver created | Grid URL: {settings.remote_url}")
        return driver
    
    @staticmethod
    def quit_driver(driver: webdriver.Remote) -> None:
        """Quit the WebDriver instance."""
        try:
            if driver:
                driver.quit()
                logger.info("WebDriver quit successfully")
        except Exception as e:
            logger.warning(f"Error quitting driver: {str(e)}")
