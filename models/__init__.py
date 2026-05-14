"""
Models package for Sauce Demo application.

Contains data models for login, authentication, and form input.
"""

from .login_model import LoginModel
from .login_data import LoginData
from .field_input_model import FieldInputModel
from .external_login_data_row import ExternalLoginDataRow
from .quick_reference import MODEL_FIELD_MAP, quick_login_model, quick_negative_case

__all__ = [
    "LoginModel",
    "LoginData",
    "FieldInputModel",
    "ExternalLoginDataRow",
    "MODEL_FIELD_MAP",
    "quick_login_model",
    "quick_negative_case",
]

