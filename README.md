# Selenium WebDriver with Python Behave (BDD) Framework

An enterprise-grade test automation framework built with Selenium WebDriver 4, Python 3.10+, and Behave BDD — following the Gherkin language syntax and Page Object Model pattern.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Writing Features](#writing-features)
- [Writing Steps](#writing-steps)
- [Page Objects](#page-objects)
- [Exception Handling](#exception-handling)
- [Reports](#reports)

---

## Features

### Core

- **BDD with Gherkin**: Feature files written in plain English syntax
- **Cross-Browser Support**: Chrome, Firefox, Edge, Safari, Selenium Grid
- **Page Object Model**: BasePage with 60+ helper methods
- **Pydantic Settings**: Type-safe, environment-based configuration
- **Structured Logging**: Per-module loggers with configurable level
- **Screenshots on Failure**: Automatic screenshot capture
- **Allure Reports**: Beautiful test reports with Behave integration

### Browser Options

- Headless mode, incognito/private, GPU disable
- Custom user-agent, proxy server, mobile device emulation
- Configurable download directory, page-load strategy
- SSL/certificate error bypass, notification/popup suppression

---

## Project Structure

```
behave-selenium-framework/
│
├── config/
│   └── config.py                   # Pydantic settings
│
├── core/
│   ├── driver.py                   # WebDriver factory
│   └── base_page.py                # BasePage with 60+ methods
│
├── exceptions/
│   ├── custom.py                   # Exception hierarchy
│   ├── handlers.py                 # Decorators and helpers
│   └── __init__.py
│
├── features/
│   ├── environment.py              # Behave hooks (before/after)
│   ├── *.feature                   # Feature files (Gherkin)
│   └── steps/
│       ├── *_steps.py              # Step definitions
│
├── pages/
│   ├── page_objects.py             # All page classes
│   └── PageManager.py              # Page object manager
│
├── utils/
│   └── logger.py                   # Logging utility
│
├── logs/                           # Test execution logs
├── reports/                        # Test reports & screenshots
│
├── .env.example                    # Configuration template
├── requirements.txt                # Python dependencies
├── setup.py                        # Package metadata
└── README.md
```

---

## Installation

**Requirements**: Python 3.10+, pip, Git

```bash
# 1. Clone repository
git clone <repository-url>
cd behave-selenium-framework

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings
```

---

## Configuration

All settings are loaded from `.env` file using Pydantic.

### Example .env

```env
# Browser
BROWSER=chrome
HEADLESS=false
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080

# Application
BASE_URL=https://www.saucedemo.com
ENVIRONMENT=dev
EXPLICIT_WAIT=15

# Test Data
TEST_USERNAME=standard_user
TEST_PASSWORD=secret_sauce

# Reporting
SCREENSHOT_ON_FAILURE=true
REPORT_PATH=reports
```

---

## Config Integration Example

You can run the new Python config integration sample without opening a browser.

```powershell
python run_config_integration_example.py
```

Run the matching Behave feature (tagged `@config_only`) to validate token resolution and timeout wiring:

```powershell
behave features/config-integration/config_integration.feature
```

Login example using resolved config tokens:

```powershell
python run_login_config_example.py
python -u run_login_constants_example.py
behave features/config-integration/config_login_with_tokens.feature
```

See `doc/config/README.md` for details.

---

## Running Tests

```bash
# All scenarios
behave

# Specific feature file
behave features/login-application.feature

# By tag (smoke tests)
behave --tags=@smoke

# By tag (e2e tests)
behave --tags=@e2e

# Multiple tags
behave --tags=@smoke --tags=@regression

# With allure reporting
behave --tags=@smoke --format allure_behave.formatter:AllureFormatter --outfile=reports/allure

# Verbose output
behave -v

# Dry run (parse without executing)
behave --dry-run

# Single scenario
behave features/login-application.feature:10  # Line 10 of file
```

---

## Writing Features

Feature files use Gherkin syntax:

```gherkin
Feature: Login Functionality
  As a user
  I want to log into the application
  So that I can access features

  Background:
    Given the user navigates to the home page

  @smoke @regression
  Scenario: Successful login
    When the user logs in with "user" and "pass"
    Then the user should see the dashboard

  @regression
  Scenario: Failed login
    When the user logs in with "invalid" and "pass"
    Then an error message should be displayed
```

### Tags

- `@smoke` - Critical path tests
- `@regression` - Full test suite
- `@e2e` - End-to-end user journeys
- `@functional` - Feature-level tests
- `@slow` - Tests taking > 60 seconds

---

## Writing Steps

Step definitions implement the Gherkin scenarios:

```python
from behave import given, when, then
from utils.logger import get_logger

logger = get_logger(__name__)

@given('the user navigates to the home page')
def step_navigate_home(context):
    """Navigate to home page."""
    context.app.login.load("")
    logger.info("Navigated to home")

@when('the user logs in with "{username}" and "{password}"')
def step_login(context, username, password):
    """Log in with credentials."""
    context.app.login.login(username, password)
    logger.info(f"Logged in as {username}")

@then('the user should see the dashboard')
def step_verify_dashboard(context):
    """Verify dashboard is displayed."""
    assert context.app.inventory.get_product_count() > 0
    logger.info("Dashboard verified")
```

### Context Object

- `context.driver` - WebDriver instance
- `context.app` - PageManager with all page objects
- `context.scenario` - Current scenario metadata
- `context.table` - Data table from Gherkin

---

## Page Objects

### Creating a Page Object

```python
from selenium.webdriver.common.by import By
from core.base_page import BasePage

class ProductPage(BasePage):
    """Product details page."""
    
    TITLE = (By.CLASS_NAME, "product-title")
    ADD_TO_CART = (By.ID, "add-to-cart")
    PRICE = (By.CLASS_NAME, "price")
    
    def get_title(self) -> str:
        return self.get_text(self.TITLE)
    
    def add_to_cart(self) -> None:
        self.click(self.ADD_TO_CART)
```

### Using PageManager

```python
@then('the user adds product to cart')
def step_add_product(context):
    context.app.product.add_to_cart()  # Access page via manager
    context.app.nav.go_to_cart()       # Cross-navigate between pages
```

### BasePage Methods

**Navigation**
- `load(endpoint)` - Navigate to URL
- `navigate_to(url)` - Navigate to absolute URL
- `get_current_url()` - Get current page URL
- `refresh()` - Refresh page
- `go_back()` - Browser back button

**Element Finding**
- `find_element(locator)` - Find single element
- `find_elements(locator)` - Find multiple elements
- `element_exists(locator)` - Check if element exists

**Interaction**
- `click(locator)` - Click element
- `type_text(locator, text)` - Type text in field
- `get_text(locator)` - Get element text
- `check(locator)` - Check checkbox
- `select_dropdown_by_value(locator, value)` - Select dropdown

**Keyboard**
- `press_enter(locator)` - Press Enter key
- `press_escape(locator)` - Press Escape key
- `send_keyboard_shortcut(*keys)` - Send Ctrl+A, etc.

**Mouse**
- `hover(locator)` - Hover over element
- `drag_and_drop(source, target)` - Drag and drop
- `double_click(locator)` - Double-click element

**Scrolling**
- `scroll_to_element(locator)` - Scroll to element
- `scroll_by(x, y)` - Scroll by offset
- `scroll_to_top()` - Scroll to top
- `scroll_to_bottom()` - Scroll to bottom

**Storage**
- `get_local_storage(key)` - Read localStorage
- `set_local_storage(key, value)` - Write localStorage
- `clear_local_storage()` - Clear all localStorage

**Screenshots**
- `take_screenshot(file_path)` - Full page screenshot
- `take_element_screenshot(locator, file_path)` - Element screenshot

---

## Exception Handling

### Custom Exception Hierarchy

```
FrameworkError
├── BrowserInitError
├── ElementNotFoundError
├── ElementNotInteractableError
├── StaleElementError
├── NavigationError
└── PageLoadError
```

### Using Safe Helpers

```python
from exceptions import safe_int, safe_str, safe_bool, suppress

# Safe value extraction
count = safe_int(lambda: int(page.get_text(locator)))  # Returns 0 on failure
text = safe_str(lambda: page.get_text(locator))        # Returns "" on failure

# Suppress exceptions
from selenium.common.exceptions import TimeoutException
with suppress(TimeoutException):
    page.wait_for_element(locator)
```

### Retry on Stale Element

```python
from exceptions import retry_on_stale

@retry_on_stale(max_retries=3)
def my_method(self):
    # Method will retry if StaleElementReferenceException is raised
    ...
```

---

## Reports

### Allure Reports

```bash
# Generate Allure report
behave --format allure_behave.formatter:AllureFormatter --outfile=reports/allure

# View report
allure serve reports/allure
```

### Screenshots

Screenshots are automatically saved on test failure to `reports/screenshots/`:

```
reports/
├── screenshots/
│   ├── Login_Functionality/
│   │   ├── Successful_login_FAILED.png
│   │   └── Failed_login_PASSED.png
│   └── Shopping_Cart/
│       └── Add_product_FAILED.png
└── allure/
    └── (allure report data)
```

### Logging

Test logs are saved to `logs/` directory:

```
logs/
└── test_2026-05-09.log
```

---

## Behave Hooks

The `features/environment.py` file contains hooks for test setup and teardown:

```python
def before_all(context):
    """Run once before all scenarios."""
    # Setup test environment
    pass

def before_scenario(context, scenario):
    """Run before each scenario."""
    # Initialize browser and page objects
    context.driver = WebDriverFactory.create_driver()
    context.app = PageManager(context.driver)

def after_scenario(context, scenario):
    """Run after each scenario."""
    # Take screenshot on failure
    # Close browser
    pass
```

---

## Best Practices

### Feature Writing

1. **Use descriptive titles** - Clearly state what is being tested
2. **Include Background** - Set up common preconditions
3. **Use data tables** - For parameterized tests
4. **One scenario per behavior** - Keep scenarios focused
5. **Use tags** - Organize and filter tests

### Step Writing

1. **One action per step** - Avoid compound steps
2. **Use Given-When-Then** - Follow BDD structure
3. **Make steps reusable** - Avoid scenario-specific language
4. **Log important actions** - For debugging failures
5. **Use parameterization** - For data-driven tests

### Page Objects

1. **Locators as constants** - Define once, use many times
2. **One method per action** - `login()`, `click_checkout()`, etc.
3. **Return page objects** - For method chaining
4. **Keep pages focused** - One page per application page
5. **Use meaningful names** - `SUBMIT_BUTTON`, not `BUTTON_1`

---

## Troubleshooting

### WebDriver fails to start

```bash
pip install --upgrade webdriver-manager
# Check logs for detailed error message
```

### Stale element errors

Framework automatically retries 3 times. If errors persist, increase retries:

```python
@retry_on_stale(max_retries=5)
def my_method(self): ...
```

### Tests timing out

Increase explicit wait in `.env`:

```env
EXPLICIT_WAIT=30
```

### Screenshot issues

Ensure `reports/screenshots/` directory is writable and disk space is available.

---

## Framework Comparison

| Feature | Pytest | Behave |
|---------|--------|--------|
| **Syntax** | Python | Gherkin (English) |
| **Business readability** | Low | High |
| **Setup** | Fixtures | Hooks |
| **Assertions** | `assert` | Step assertions |
| **Reporting** | pytest-html | Allure |
| **Best for** | Technical teams | Cross-functional teams |

---

## Additional Resources

- [Selenium 4 Documentation](https://selenium.dev/documentation/)
- [Behave Documentation](https://behave.readthedocs.io/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Allure Behave](https://allurereport.org/docs/behave/)

---

**Framework Version**: 1.0.0  
**Python**: 3.10+  
**Selenium**: 4.x  
**Behave**: 1.2.x  
**Last Updated**: May 2026  
**Maintained By**: QA Automation Team
