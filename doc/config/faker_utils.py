"""
Faker utilities for generating random test data.

Equivalent to Java FakerUtils class.
Generates random emails, passwords, names, usernames, etc.
"""

import os
import random
import uuid
from typing import Final

from faker import Faker


class FakerUtils:
    """Utility class for generating random test data using Faker library."""

    # Get faker seed from environment or use default
    _FAKER_SEED: Final[int] = int(os.getenv("FAKER_SEED", "42"))

    # Initialize Faker with seed for reproducible results
    _FAKER: Final[Faker] = Faker()
    Faker.seed(_FAKER_SEED)
    random.seed(_FAKER_SEED)

    @staticmethod
    def resolve_token(token: str | None) -> str:
        """
        Resolve a Faker token to a random value.

        Supported tokens:
            - email, random_email
            - password, random_password
            - name, random_name
            - username, random_username, invalid_username
            - invalid_password, wrong_password

        Args:
            token: The token string to resolve (case-insensitive)

        Returns:
            The resolved random value or the original token if not recognized
        """
        if token is None:
            return ""

        normalized = token.strip().lower()

        match normalized:
            case "email" | "random_email":
                return FakerUtils.generate_random_email()
            case "password" | "random_password":
                return FakerUtils.generate_random_password()
            case "name" | "random_name":
                return FakerUtils.generate_random_name()
            case "username" | "random_username" | "invalid_username":
                return FakerUtils.generate_random_username()
            case "invalid_password" | "wrong_password":
                return FakerUtils.generate_invalid_password_for_sauce_demo()
            case _:
                return token

    @staticmethod
    def generate_random_number(length: int = 10) -> int:
        """
        Generate a random number.

        Args:
            length: Number of digits (default 10)

        Returns:
            Random integer
        """
        return FakerUtils._FAKER.generator.random.randint(
            10 ** (length - 1),
            10 ** length - 1
        )

    @staticmethod
    def generate_random_email() -> str:
        """
        Generate a random email address.

        Returns:
            Random email address
        """
        return FakerUtils._FAKER.email()

    @staticmethod
    def generate_random_password(min_length: int = 8, max_length: int = 14) -> str:
        """
        Generate a random password.

        Args:
            min_length: Minimum password length (default 8)
            max_length: Maximum password length (default 14)

        Returns:
            Random password with letters, numbers and symbols
        """
        return FakerUtils._FAKER.password(
            length=random.randint(min_length, max_length),
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )

    @staticmethod
    def generate_random_name() -> str:
        """
        Generate a random full name.

        Returns:
            Random full name
        """
        return FakerUtils._FAKER.name()

    @staticmethod
    def generate_random_username(prefix: str = "user_") -> str:
        """
        Generate a random username.

        Args:
            prefix: Username prefix (default "user_")

        Returns:
            Random username in format: user_<8-char-uuid>
        """
        uid = uuid.uuid4().hex.replace("-", "")[:8]
        return f"{prefix}{uid}"

    @staticmethod
    def generate_invalid_password_for_sauce_demo(prefix: str = "wrong_") -> str:
        """
        Generate an invalid password for Sauce Demo (deliberately wrong).

        Args:
            prefix: Password prefix (default "wrong_")

        Returns:
            Invalid password in format: wrong_<8-char-uuid>
        """
        uid = uuid.uuid4().hex.replace("-", "")[:8]
        return f"{prefix}{uid}"

