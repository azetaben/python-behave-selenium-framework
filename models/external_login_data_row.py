"""ExternalLoginDataRow - represents login test data row from external sources."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalLoginDataRow:
    """
    Represents a row of login test data from external sources (CSV, JSON, etc.).

    Equivalent to Java record:
        public record ExternalLoginDataRow(
            String testCaseId,
            String username,
            String password,
            String expectedResult,
            String expectedMessage
        ) {}

    Attributes:
        test_case_id: Unique identifier for the test case
        username: The login username
        password: The login password
        expected_result: The expected result of the login attempt (pass/fail)
        expected_message: The expected message from the application
    """
    test_case_id: str
    username: str
    password: str
    expected_result: str
    expected_message: str

