"""LoginData - represents login test data with expected results."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LoginData:
    """
    Represents login test data with expected validation results.

    Equivalent to Java record:
        public record LoginData(String username, String password, String expectedError) {}

    Attributes:
        username: The login username
        password: The login password
        expected_error: The expected error message if login fails
    """
    username: str
    password: str
    expected_error: str

