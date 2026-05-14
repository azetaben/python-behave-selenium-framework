"""Reusable model usage helpers for Behave step definitions.

This module follows production conventions:
- snake_case filename
- pure helper functions (no nested step decorators)
- typed interfaces suitable for reuse in `features/steps/*.py`
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from models.external_login_data_row import ExternalLoginDataRow
from models.field_input_model import FieldInputModel
from models.login_data import LoginData
from models.login_model import LoginModel


def build_login_credentials(username: str, password: str) -> LoginModel:
    """Create validated login credentials."""
    return LoginModel(username=username, password=password)


def build_checkout_form(first_name: str, last_name: str, postal_code: str) -> FieldInputModel:
    """Create a checkout form payload for page-object field filling."""
    return FieldInputModel(
        field_input_data={
            "first_name": first_name,
            "last_name": last_name,
            "postal_code": postal_code,
        }
    )


def default_login_test_cases() -> list[LoginData]:
    """Return common login scenarios for negative/positive coverage."""
    return [
        LoginData("standard_user", "secret_sauce", ""),
        LoginData("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
        LoginData("", "secret_sauce", "Epic sadface: Username is required"),
        LoginData("user", "", "Epic sadface: Password is required"),
    ]


def load_external_login_data(csv_file_path: str | Path) -> list[ExternalLoginDataRow]:
    """Load CSV rows into typed `ExternalLoginDataRow` objects."""
    path = Path(csv_file_path)
    rows: list[ExternalLoginDataRow] = []
    with path.open("r", encoding="utf-8", newline="") as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            rows.append(
                ExternalLoginDataRow(
                    test_case_id=row["test_case_id"],
                    username=row["username"],
                    password=row["password"],
                    expected_result=row["expected_result"],
                    expected_message=row["expected_message"],
                )
            )
    return rows


def table_rows_to_login_data(rows: Iterable[dict[str, str]]) -> list[LoginData]:
    """Convert Behave table-like dictionaries to `LoginData` objects."""
    return [
        LoginData(
            username=row["username"],
            password=row["password"],
            expected_error=row.get("expected_error", ""),
        )
        for row in rows
    ]


def to_login_pairs(rows: Iterable[LoginData]) -> list[tuple[str, str]]:
    """Extract `(username, password)` pairs for login action loops."""
    return [(row.username, row.password) for row in rows]


__all__ = [
    "build_login_credentials",
    "build_checkout_form",
    "default_login_test_cases",
    "load_external_login_data",
    "table_rows_to_login_data",
    "to_login_pairs",
]


if __name__ == "__main__":
    sample_cases = default_login_test_cases()
    print(f"Loaded {len(sample_cases)} default login test cases")
    credentials = build_login_credentials("standard_user", "secret_sauce")
    print(f"Credential model created for: {credentials.username}")


