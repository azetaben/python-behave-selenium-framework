"""Faker utilities for generating random test data."""

import os
import random
import uuid
from typing import Final

from faker import Faker


class FakerUtils:
    """Utility class for generating random test data using Faker library."""

    _FAKER_SEED: Final[int] = int(os.getenv("FAKER_SEED", "42"))
    _FAKER: Final[Faker] = Faker()
    Faker.seed(_FAKER_SEED)
    random.seed(_FAKER_SEED)

    @staticmethod
    def resolve_token(token: str | None) -> str:
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
        return FakerUtils._FAKER.generator.random.randint(10 ** (length - 1), 10 ** length - 1)

    @staticmethod
    def generate_random_email() -> str:
        return FakerUtils._FAKER.email()

    @staticmethod
    def generate_random_password(min_length: int = 8, max_length: int = 14) -> str:
        return FakerUtils._FAKER.password(
            length=random.randint(min_length, max_length),
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

    @staticmethod
    def generate_random_name() -> str:
        return FakerUtils._FAKER.name()

    @staticmethod
    def generate_random_username(prefix: str = "user_") -> str:
        uid = uuid.uuid4().hex.replace("-", "")[:8]
        return f"{prefix}{uid}"

    @staticmethod
    def generate_invalid_password_for_sauce_demo(prefix: str = "wrong_") -> str:
        uid = uuid.uuid4().hex.replace("-", "")[:8]
        return f"{prefix}{uid}"
