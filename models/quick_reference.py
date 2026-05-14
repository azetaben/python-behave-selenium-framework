"""Quick reference for the models package.

This module provides compact usage snippets and helper constants that can be
imported in step files or scripts while keeping naming conventions consistent.
"""

from __future__ import annotations

from models.external_login_data_row import ExternalLoginDataRow
from models.field_input_model import FieldInputModel
from models.login_data import LoginData
from models.login_model import LoginModel, PredefinedUsers


MODEL_FIELD_MAP: dict[str, tuple[str, ...]] = {
    "LoginModel": ("username", "password"),
    "LoginData": ("username", "password", "expected_error"),
    "FieldInputModel": ("field_input_data",),
    "ExternalLoginDataRow": (
        "test_case_id",
        "username",
        "password",
        "expected_result",
        "expected_message",
    ),
}


def quick_login_model() -> LoginModel:
    """Return a standard credential model for smoke checks/examples."""
    return PredefinedUsers.STANDARD_USER


def quick_negative_case() -> LoginData:
    """Return a simple negative login-data sample."""
    return LoginData(
        username="locked_out_user",
        password="secret_sauce",
        expected_error="Epic sadface: Sorry, this user has been locked out.",
    )


def quick_checkout_form() -> FieldInputModel:
    """Return a minimal checkout payload sample."""
    return FieldInputModel(
        field_input_data={
            "first_name": "Jane",
            "last_name": "Doe",
            "postal_code": "10001",
        }
    )


def quick_external_row() -> ExternalLoginDataRow:
    """Return one external test-data row sample."""
    return ExternalLoginDataRow(
        test_case_id="SMOKE_001",
        username="standard_user",
        password="secret_sauce",
        expected_result="SUCCESS",
        expected_message="",
    )


__all__ = [
    "MODEL_FIELD_MAP",
    "quick_login_model",
    "quick_negative_case",
    "quick_checkout_form",
    "quick_external_row",
]


if __name__ == "__main__":
    print("Model fields:", MODEL_FIELD_MAP["LoginModel"])
    print("Smoke user:", quick_login_model().username)

