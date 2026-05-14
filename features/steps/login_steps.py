"""Step definitions for login / authentication, login page UI verification,
and data-driven login scenarios."""

from __future__ import annotations

from behave import step

from config.config import settings
from constants import SauceDemoConstants
from features.steps.common_steps import run_with_perf_navigation
from utils.logger import get_logger
from utils.testdata_loader import TestDataLoader

logger = get_logger(__name__)
CONSTANTS = SauceDemoConstants.from_config()


# ── Private helpers ───────────────────────────────────────────────────────────

def _normalize_heading(value: str) -> str:
    """Lowercase, strip whitespace, and remove a trailing colon."""
    return value.strip().lower().rstrip(":")


def _table_first_column_values(context) -> list[str]:
    return [row.cells[0].strip() for row in context.table]


# ── Session setup ─────────────────────────────────────────────────────────────

@step('the user has successfully logged in')
def step_user_logged_in(context) -> None:
    """Log in with the configured test credentials and land on the inventory page."""
    context.app.login.load("")
    run_with_perf_navigation(
        context,
        "login-settings-user",
        lambda: context.app.login.login(settings.test_username, settings.test_password),
    )
    assert context.app.inventory.get_product_count() > 0, "Login failed — inventory page not reached"
    logger.info("User successfully logged in")



# ── Login page UI verification ────────────────────────────────────────────────

@step('the logo should present and visible')
def step_verify_logo_visible(context) -> None:
    """Assert that the login page logo is displayed."""
    assert context.app.login.is_logo_displayed(), "Login logo is not visible"
    logger.info("Login logo is visible")


@step('the user can see the following input fields:')
def step_verify_input_fields(context) -> None:
    """Assert that each listed field name (column: field_name) is visible."""
    field_locators = {
        "username": context.app.login.USERNAME,
        "password": context.app.login.PASSWORD,
    }
    for row in context.table:
        field_name = row["field_name"].strip().lower()
        locator = field_locators.get(field_name)
        assert locator is not None, "Unsupported input field: '%s'" % field_name
        assert context.app.login.is_element_visible(locator, timeout=3), \
            "Input field not visible: '%s'" % field_name
    logger.info("All listed input fields are visible")


@step('the user can see the "{button_text}" button is enabled and visible')
def step_verify_login_button_enabled_visible(context, button_text: str) -> None:
    """Assert the Login submit button is visible and enabled."""
    assert button_text.strip().lower() == "login", \
        "Unsupported button text: '%s' — only 'Login' is supported here" % button_text
    assert context.app.login.is_element_visible(context.app.login.LOGIN_BUTTON, timeout=3), \
        "Login button is not visible"
    button = context.app.login.find_element(context.app.login.LOGIN_BUTTON, timeout=3)
    assert button.is_enabled(), "Login button is disabled"
    logger.info("Login button is visible and enabled")


@step('the login page should contain "{heading}":')
def step_verify_login_page_lists(context, heading: str) -> None:
    """Assert the credential hint block matches the expected heading and table values."""
    normalized_heading = _normalize_heading(heading)
    raw_values = _table_first_column_values(context)

    if normalized_heading == _normalize_heading(context.app.login.ACCEPTED_USERNAMES_TEXT):
        assert context.app.login.is_accepted_usernames_hint_displayed(), \
            "Accepted usernames hint block is not visible"
        expected = [
            v for v in raw_values
            if _normalize_heading(v) not in {"accepted usernames", normalized_heading}
        ]
        actual = context.app.login.get_accepted_usernames()
        assert actual == expected, (
            "Accepted usernames mismatch.\n  Expected: %s\n  Got     : %s" % (expected, actual)
        )
        logger.info("Accepted usernames verified: %s", actual)
        return

    if normalized_heading == _normalize_heading(context.app.login.SHARED_PASSWORD_TEXT):
        assert context.app.login.is_password_hint_displayed(), \
            "Password hint block is not visible"
        candidates = [
            v for v in raw_values
            if _normalize_heading(v) not in {"password for all users", normalized_heading}
        ]
        expected = candidates[0] if candidates else ""
        actual = context.app.login.get_shared_password()
        assert actual == expected, (
            "Shared password mismatch. Expected '%s', got '%s'" % (expected, actual)
        )
        logger.info("Shared password verified")
        return

    raise AssertionError("Unsupported login page heading: '%s'" % heading)


@step('the user logged in as {username}')
def step_login_as_listed_user(context, username: str) -> None:
    """Log in using the credential extracted from the page's accepted-usernames hint."""
    context.app.login.login_with_accepted_username(username.strip())
    logger.info("Logged in as '%s' via page credential hints", username.strip())


# ── Individual field / button visibility ─────────────────────────────────────

@step('the username field should be visible')
def step_check_username_field_visible(context) -> None:
    """Verify the username input field is visible."""
    assert context.app.login.is_element_visible(context.app.login.USERNAME), \
        "Username field is not visible"
    logger.info("Username field is visible")


@step('the password field should be visible')
def step_check_password_field_visible(context) -> None:
    """Verify the password input field is visible."""
    assert context.app.login.is_element_visible(context.app.login.PASSWORD), \
        "Password field is not visible"
    logger.info("Password field is visible")


@step('the login button should be visible')
def step_check_login_button_visible(context) -> None:
    """Verify the login submit button is visible."""
    assert context.app.login.is_element_visible(context.app.login.LOGIN_BUTTON), \
        "Login button is not visible"
    logger.info("Login button is visible")


# ── Error assertions ──────────────────────────────────────────────────────────

@step('an error message should be displayed')
def step_check_error_displayed(context) -> None:
    """Verify that a login error message is visible."""
    assert context.app.login.is_error_displayed(), "Error message not displayed"
    logger.info("Error message is displayed")


@step('the error message should contain "{text}"')
def step_check_error_text(context, text: str) -> None:
    """Verify that the displayed error message contains *text* (case-insensitive)."""
    error_msg = context.app.login.get_error_message().lower()
    assert text.lower() in error_msg, (
        "Error message does not contain '%s': %s" % (text, error_msg)
    )
    logger.info("Error message contains '%s'", text)


@step('the login error should match constant "{constant_name}"')
def step_check_error_text_from_constant(context, constant_name: str) -> None:
    """Assert that the displayed login error exactly matches a *SauceDemoConstants* value."""
    expected = getattr(CONSTANTS, constant_name, None)
    assert expected is not None, "Unknown SauceDemoConstants key: %s" % constant_name
    actual = context.app.login.get_error_message().strip()
    assert actual == expected, "Expected exact error '%s', got '%s'" % (expected, actual)
    logger.info("Error matched constant '%s'", constant_name)


# ── Login actions ─────────────────────────────────────────────────────────────

@step('the user logs in with username ref "{username_ref}" and password ref "{password_ref}"')
def step_login_with_references(context, username_ref: str, password_ref: str) -> None:
    """Log in using flexible value refs: EMPTY, constants, config tokens, or literals."""

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
        "login-%s" % username_ref,
        lambda: context.app.login.login(username, password),
    )
    logger.info("Logged in with refs username='%s' password='%s'", username_ref, password_ref)


# ── Data-driven helpers ───────────────────────────────────────────────────────

def _require_test_data(context) -> list:
    """Raise if test data has not been loaded yet."""
    if not hasattr(context, "test_data"):
        raise RuntimeError(
            "Test data not loaded. Call 'I load login test data from …' first."
        )
    return context.test_data


def _find_test_case(context, test_case_id: str):
    """Return the test-case row matching *test_case_id*, or raise AssertionError."""
    for row in _require_test_data(context):
        if row.test_case_id == test_case_id:
            return row
    raise AssertionError("Test case '%s' not found in loaded test data" % test_case_id)


# ── Data loading ──────────────────────────────────────────────────────────────

@step('I load login test data from "{data_file}"')
@step('I load up login test data from "{data_file}"')
def step_load_test_data(context, data_file: str) -> None:
    """Auto-detect format (csv / json / xlsx) from the file extension and load into context."""
    file_path = TestDataLoader.get_test_data_path(data_file)
    context.test_data = TestDataLoader.load_login_data(file_path)
    logger.info("Loaded %d test case(s) from '%s'", len(context.test_data), data_file)


@step('I load login test data from excel "{excel_file}" sheet "{sheet_name}"')
def step_load_excel_test_data(context, excel_file: str, sheet_name: str) -> None:
    """Load login test data from a specific sheet in an Excel workbook."""
    file_path = TestDataLoader.get_test_data_path(excel_file)
    context.test_data = TestDataLoader.load_login_excel(file_path, sheet_name)
    logger.info(
        "Loaded %d test case(s) from '%s' (sheet: %s)",
        len(context.test_data), excel_file, sheet_name,
    )


# ── Filtering ─────────────────────────────────────────────────────────────────

@step('I filter test data for successful logins')
def step_filter_success_cases(context) -> None:
    """Keep only rows whose expected_result is SUCCESS."""
    context.test_data = [
        row for row in _require_test_data(context)
        if row.expected_result.upper() == "SUCCESS"
    ]
    logger.info("Filtered to %d successful test case(s)", len(context.test_data))


@step('I filter test data for failed logins')
def step_filter_failure_cases(context) -> None:
    """Keep only rows whose expected_result is FAILURE."""
    context.test_data = [
        row for row in _require_test_data(context)
        if row.expected_result.upper() == "FAILURE"
    ]
    logger.info("Filtered to %d failed test case(s)", len(context.test_data))


# ── Execution ─────────────────────────────────────────────────────────────────

@step('I have {count:d} login test cases loaded')
def step_verify_test_data_count(context, count: int) -> None:
    """Assert that exactly *count* test cases are loaded."""
    actual = len(_require_test_data(context))
    assert actual == count, "Expected %d test case(s) but got %d" % (count, actual)
    logger.info("Verified %d test case(s) loaded", count)


@step('I execute login test case "{test_case_id}"')
def step_execute_specific_test_case(context, test_case_id: str) -> None:
    """Execute a single test case by its ID and store it for later assertions."""
    test_case = _find_test_case(context, test_case_id)
    context.current_test_case = test_case
    context.app.login.login(test_case.username, test_case.password)
    logger.info("Executed test case '%s'", test_case_id)


@step('I execute all loaded login test cases')
def step_execute_all_test_cases(context) -> None:
    """Run every loaded test case sequentially and collect pass/fail results."""
    context.executed_results = []

    for test_case in _require_test_data(context):
        result: dict = {"test_case_id": test_case.test_case_id, "expected": test_case.expected_result}
        try:
            context.app.login.load("")
            context.app.login.login(test_case.username, test_case.password)

            if test_case.expected_result.upper() == "SUCCESS":
                is_success = context.app.inventory.get_product_count() > 0
            else:
                is_success = context.app.login.is_error_displayed()

            result["success"] = is_success
        except Exception as exc:  # noqa: BLE001
            logger.error("Error executing '%s': %s", test_case.test_case_id, exc)
            result["success"] = False
            result["error"] = str(exc)

        context.executed_results.append(result)
        logger.info(
            "%s: %s",
            test_case.test_case_id,
            "PASS" if result["success"] else "FAIL",
        )


# ── Data-driven assertions ────────────────────────────────────────────────────

@step('the test case should result in "{expected_result}"')
def step_verify_test_result(context, expected_result: str) -> None:
    """Verify the outcome of the most recently executed test case."""
    if not hasattr(context, "current_test_case"):
        raise RuntimeError("No current test case. Call 'I execute login test case' first.")

    expected = expected_result.upper()
    if expected == "SUCCESS":
        assert context.app.inventory.get_product_count() > 0, \
            "Expected successful login but no products found"
    elif expected == "FAILURE":
        assert context.app.login.is_error_displayed(), \
            "Expected failed login but no error displayed"
    else:
        raise ValueError("Unknown expected result: %s" % expected_result)

    logger.info("Test case result verified: %s", expected)


@step('the error message should match the expected message')
def step_verify_expected_error_message(context) -> None:
    """Assert that the displayed error contains the expected_message from the current test case."""
    if not hasattr(context, "current_test_case"):
        raise RuntimeError("No current test case. Call 'I execute login test case' first.")

    test_case = context.current_test_case
    if test_case.expected_message:
        actual_message = context.app.login.get_error_message()
        assert test_case.expected_message.lower() in actual_message.lower(), (
            "Expected '%s' but got '%s'" % (test_case.expected_message, actual_message)
        )
        logger.info("Error message verified: %s", test_case.expected_message)


@step('all test cases should pass')
def step_verify_all_test_cases_pass(context) -> None:
    """Fail if any of the executed test cases did not produce the expected result."""
    if not hasattr(context, "executed_results"):
        raise RuntimeError("No test results to verify.")

    failed = [r for r in context.executed_results if not r["success"]]
    assert not failed, (
        "%d test case(s) failed out of %d:\n%s"
        % (
            len(failed),
            len(context.executed_results),
            "\n".join("  %s" % r["test_case_id"] for r in failed),
        )
    )
    logger.info("All %d test case(s) passed", len(context.executed_results))


@step('I should have {expected_count:d} test cases with expected result "{expected_result}"')
def step_verify_test_case_counts(context, expected_count: int, expected_result: str) -> None:
    """Assert that exactly *expected_count* rows carry the given *expected_result*."""
    matching = [
        row for row in _require_test_data(context)
        if row.expected_result.upper() == expected_result.upper()
    ]
    assert len(matching) == expected_count, (
        "Expected %d case(s) with '%s' but found %d"
        % (expected_count, expected_result, len(matching))
    )
    logger.info("Verified %d test case(s) with '%s'", expected_count, expected_result)


# ── Reporting ─────────────────────────────────────────────────────────────────

@step('I print test data summary')
def step_print_test_data_summary(context) -> None:
    """Print a human-readable summary of all loaded test cases to stdout and the log."""
    test_data = _require_test_data(context)

    success_count = sum(1 for r in test_data if r.expected_result.upper() == "SUCCESS")
    failure_count = len(test_data) - success_count

    lines = [
        "",
        "=" * 80,
        "TEST DATA SUMMARY",
        "=" * 80,
        "Total test cases : %d" % len(test_data),
        "  Expected SUCCESS: %d" % success_count,
        "  Expected FAILURE: %d" % failure_count,
        "",
    ]
    for row in test_data:
        lines.append(
            "  %-20s  %-25s  %s  →  %s"
            % (row.test_case_id, row.username, "*" * len(row.password), row.expected_result)
        )
    lines.append("=" * 80)

    report = "\n".join(lines)
    print(report)
    logger.info(report)

