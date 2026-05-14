"""Tiny runner showing login-oriented constants' integration."""

from constants import EndPoint, SauceDemoConstants
from doc.config.integration import build_config_bundle


def main() -> None:
    bundle = build_config_bundle()
    c = SauceDemoConstants.from_config()

    valid_username = bundle.resolve("user:STANDARD_USERNAME")
    valid_password = bundle.resolve("user:PASSWORD")
    invalid_username = bundle.resolve("faker:username")
    invalid_password = bundle.resolve("faker:wrong_password")

    print("Login constants integration example")
    print("----------------------------------")
    print(f"Base URL: {c.DEFAULT_BASE_URL}")
    print(f"Login endpoint: {EndPoint.LOGIN.value}")
    print(f"Expected invalid-login error: {c.ERR_WRONG_CREDENTIALS}")
    print()
    print(f"Valid creds: {valid_username} / {'*' * len(valid_password)}")
    print(f"Invalid creds: {invalid_username} / {'*' * len(invalid_password)}")


if __name__ == "__main__":
    main()

