"""
Example step definitions demonstrating data-driven login tests with external data.
This file shows how to integrate testdata_loader with Behave scenarios.
"""

from behave import given, when, then

from utils.logger import get_logger
from utils.testdata_loader import TestDataLoader

logger = get_logger(__name__)


# ============================================================================
# EXAMPLE 1: Load data from context
# ============================================================================

@given('I load login test data from "{data_file}"')
def step_load_test_data(context, data_file):
    """Auto-detect format (csv/json/xlsx) from file extension and load into context."""
    file_path = TestDataLoader.get_test_data_path(data_file)
    context.test_data = TestDataLoader.load_login_data(file_path)
    logger.info(f"Loaded {len(context.test_data)} test cases from {data_file}")


@given('I load up login test data from "{data_file}"')
def step_load_up_test_data(context, data_file):
    """Auto-detect format (csv/json/xlsx) from file extension and load into context."""
    file_path = TestDataLoader.get_test_data_path(data_file)
    context.test_data = TestDataLoader.load_login_data(file_path)
    logger.info(f"Loaded {len(context.test_data)} test cases from {data_file}")


@given('I load login test data from excel "{excel_file}" sheet "{sheet_name}"')
def step_load_excel_test_data(context, excel_file, sheet_name):
    """Load login test data from an Excel file using an explicit sheet name."""
    file_path = TestDataLoader.get_test_data_path(excel_file)
    context.test_data = TestDataLoader.load_login_excel(file_path, sheet_name)
    logger.info(f"Loaded {len(context.test_data)} test cases from {excel_file} ({sheet_name})")


# ============================================================================
# EXAMPLE 2: Filter test data by expected result
# ============================================================================

@given('I filter test data for successful logins')
def step_filter_success_cases(context):
    """Filter context.test_data to include only successful login cases."""
    if not hasattr(context, 'test_data'):
        raise RuntimeError("Test data not loaded. Use 'I load login test data from' step first.")

    context.test_data = [
        row for row in context.test_data
        if row.expected_result.upper() == 'SUCCESS'
    ]
    logger.info(f"Filtered to {len(context.test_data)} successful test cases")


@given('I filter test data for failed logins')
def step_filter_failure_cases(context):
    """Filter context.test_data to include only failed login cases."""
    if not hasattr(context, 'test_data'):
        raise RuntimeError("Test data not loaded. Use 'I load login test data from' step first.")

    context.test_data = [
        row for row in context.test_data
        if row.expected_result.upper() == 'FAILURE'
    ]
    logger.info(f"Filtered to {len(context.test_data)} failed test cases")


# ============================================================================
# EXAMPLE 3: Iterate through test data rows
# ============================================================================

@given('I have {count:d} login test cases loaded')
def step_verify_test_data_count(context, count):
    """Verify that expected number of test cases are loaded."""
    if not hasattr(context, 'test_data'):
        raise RuntimeError("Test data not loaded.")

    assert len(context.test_data) == count, \
        f"Expected {count} test cases but got {len(context.test_data)}"
    logger.info(f"Verified {count} test cases loaded")


@when('I execute login test case "{test_case_id}"')
def step_execute_specific_test_case(context, test_case_id):
    """Execute a specific test case by ID."""
    if not hasattr(context, 'test_data'):
        raise RuntimeError("Test data not loaded.")

    # Find the test case
    test_case = None
    for row in context.test_data:
        if row.test_case_id == test_case_id:
            test_case = row
            break

    assert test_case is not None, f"Test case {test_case_id} not found"

    # Store current test case for verification
    context.current_test_case = test_case

    # Execute login
    context.app.login.login(test_case.username, test_case.password)
    logger.info(f"Executed test case: {test_case_id}")


@when('I execute all loaded login test cases')
def step_execute_all_test_cases(context):
    """Execute all loaded test cases sequentially."""
    if not hasattr(context, 'test_data'):
        raise RuntimeError("Test data not loaded.")

    context.executed_results = []

    for test_case in context.test_data:
        try:
            context.app.login.load("")  # Clear login page
            context.app.login.login(test_case.username, test_case.password)

            # Check result
            if test_case.expected_result.upper() == 'SUCCESS':
                is_success = context.app.inventory.get_product_count() > 0
            else:
                is_success = context.app.login.is_error_displayed()

            context.executed_results.append({
                'test_case_id': test_case.test_case_id,
                'expected': test_case.expected_result,
                'success': is_success
            })

            logger.info(f"{test_case.test_case_id}: {'PASS' if is_success else 'FAIL'}")

        except Exception as e:
            logger.error(f"Error executing {test_case.test_case_id}: {str(e)}")
            context.executed_results.append({
                'test_case_id': test_case.test_case_id,
                'expected': test_case.expected_result,
                'success': False,
                'error': str(e)
            })


# ============================================================================
# EXAMPLE 4: Verification steps
# ============================================================================

@then('the test case should result in "{expected_result}"')
def step_verify_test_result(context, expected_result):
    """Verify the result of the current test case."""
    if not hasattr(context, 'current_test_case'):
        raise RuntimeError("No current test case. Use 'I execute login test case' first.")


    expected = expected_result.upper()

    if expected == 'SUCCESS':
        assert context.app.inventory.get_product_count() > 0, \
            "Expected successful login but no products found"
    elif expected == 'FAILURE':
        assert context.app.login.is_error_displayed(), \
            "Expected failed login but no error displayed"
    else:
        raise ValueError(f"Unknown expected result: {expected_result}")

    logger.info(f"Test case result verified: {expected}")


@then('the error message should match the expected message')
def step_verify_expected_error_message(context):
    """Verify error message matches the expected message."""
    if not hasattr(context, 'current_test_case'):
        raise RuntimeError("No current test case.")

    test_case = context.current_test_case

    if test_case.expected_message:
        actual_message = context.app.login.get_error_message()
        assert test_case.expected_message.lower() in actual_message.lower(), \
            f"Expected '{test_case.expected_message}' but got '{actual_message}'"

        logger.info(f"Error message verified: {test_case.expected_message}")


@then('all test cases should pass')
def step_verify_all_test_cases_pass(context):
    """Verify all executed test cases passed."""
    if not hasattr(context, 'executed_results'):
        raise RuntimeError("No test results to verify.")

    failed = [r for r in context.executed_results if not r['success']]
    assert len(failed) == 0, \
        f"{len(failed)} test case(s) failed out of {len(context.executed_results)}"

    logger.info(f"All {len(context.executed_results)} test cases passed")


# ============================================================================
# EXAMPLE 5: Helper steps for data summary
# ============================================================================

@then('I should have {expected_count:d} test cases with expected result "{expected_result}"')
def step_verify_test_case_counts(context, expected_count, expected_result):
    """Verify count of test cases for a specific expected result."""
    if not hasattr(context, 'test_data'):
        raise RuntimeError("Test data not loaded.")

    matching = [
        row for row in context.test_data
        if row.expected_result.upper() == expected_result.upper()
    ]

    assert len(matching) == expected_count, \
        f"Expected {expected_count} cases with '{expected_result}' but found {len(matching)}"

    logger.info(f"Verified {expected_count} test cases with '{expected_result}'")


@then('I print test data summary')
def step_print_test_data_summary(context):
    """Print summary of loaded test data."""
    if not hasattr(context, 'test_data'):
        raise RuntimeError("Test data not loaded.")

    print("\n" + "="*80)
    print("TEST DATA SUMMARY")
    print("="*80)

    success_count = len([r for r in context.test_data if r.expected_result.upper() == 'SUCCESS'])
    failure_count = len([r for r in context.test_data if r.expected_result.upper() == 'FAILURE'])

    print(f"Total test cases: {len(context.test_data)}")
    print(f"  - Expected SUCCESS: {success_count}")
    print(f"  - Expected FAILURE: {failure_count}")
    print()

    for row in context.test_data:
        print(f"  {row.test_case_id}: {row.username} / {'*'*len(row.password)} → {row.expected_result}")

    print("="*80 + "\n")
    logger.info("Test data summary printed")
