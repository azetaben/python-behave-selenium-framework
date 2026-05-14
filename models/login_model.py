"""
LoginModel - Login credentials model (Java record equivalent).

Pydantic provides:
- Type safety and validation
- Automatic serialization (to_dict(), model_dump())
- Field defaults and descriptions
- Easy integration with JSON/YAML
"""

from pydantic import BaseModel, Field, field_validator


class LoginModel(BaseModel):
    """
    Login credentials model (Java record equivalent).

    Pydantic provides:
    - Type safety and validation
    - Automatic serialization (to_dict(), model_dump())
    - Field defaults and descriptions
    - Easy integration with JSON/YAML

    Examples:
        >>> # Create from keyword arguments
        >>> model = LoginModel(username="user1", password="pass123")
        >>> model.username
        'user1'

        >>> # Create from dictionary
        >>> data = {"username": "user1", "password": "pass123"}
        >>> model = LoginModel(**data)

        >>> # Serialize
        >>> model.model_dump()
        {'username': 'user1', 'password': 'pass123'}

        >>> # JSON string
        >>> model.model_dump_json()
        '{"username":"user1","password":"pass123"}'

        >>> # Validation
        >>> LoginModel(username="", password="pass")
        ValidationError: username must not be empty
    """

    username: str = Field(
        ...,
        min_length=1,
        description="Login username",
        example="standard_user"
    )
    password: str = Field(
        ...,
        min_length=1,
        description="Login password",
        example="secret_sauce"
    )

    class Config:
        """Pydantic model configuration."""
        frozen = False  # Allow mutation if needed
        json_schema_extra = {
            "examples": [
                {
                    "username": "standard_user",
                    "password": "secret_sauce"
                },
                {
                    "username": "problem_user",
                    "password": "secret_sauce"
                }
            ]
        }

    @field_validator("username", "password", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace from credentials."""
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        """Validate username is not empty."""
        if not v or not v.strip():
            raise ValueError("username must not be empty")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        """Validate password is not empty."""
        if not v or not v.strip():
            raise ValueError("password must not be empty")
        return v

    def __repr__(self) -> str:
        """Return string representation (safe for logging)."""
        return f"LoginModel(username='{self.username}', password='***')"

    def __str__(self) -> str:
        """Return user-friendly string."""
        return f"User: {self.username}"


# ── Predefined Credentials for Testing ────────────────────────────────────

class PredefinedUsers:
    """Collection of predefined test user credentials."""

    STANDARD_USER = LoginModel(
        username="standard_user",
        password="secret_sauce"
    )

    LOCKED_OUT_USER = LoginModel(
        username="locked_out_user",
        password="secret_sauce"
    )

    PROBLEM_USER = LoginModel(
        username="problem_user",
        password="secret_sauce"
    )

    PERFORMANCE_GLITCH_USER = LoginModel(
        username="performance_glitch_user",
        password="secret_sauce"
    )

    @classmethod
    def get_user(cls, user_type: str) -> LoginModel:
        """
        Get a predefined user by type.

        Args:
            user_type: 'standard', 'locked', 'problem', 'glitch'

        Returns:
            LoginModel with credentials

        Examples:
            >>> user = PredefinedUsers.get_user("standard")
            >>> print(user.username)
            standard_user
        """
        mapping = {
            "standard": cls.STANDARD_USER,
            "locked": cls.LOCKED_OUT_USER,
            "problem": cls.PROBLEM_USER,
            "glitch": cls.PERFORMANCE_GLITCH_USER,
        }
        user = mapping.get(user_type.lower())
        if user is None:
            raise ValueError(
                f"Unknown user type: {user_type}. "
                f"Valid options: {', '.join(mapping.keys())}"
            )
        return user

    @classmethod
    def all_users(cls) -> list[LoginModel]:
        """Get all predefined users as a list."""
        return [cls.STANDARD_USER, cls.LOCKED_OUT_USER, cls.PROBLEM_USER, cls.PERFORMANCE_GLITCH_USER]


# ── Example Usage in Feature Tests ────────────────────────────────────────

if __name__ == "__main__":
    # Example 1: Create model directly
    print("Example 1: Direct creation")
    user1 = LoginModel(username="test_user", password="test_pass")
    print(f"  {user1}")
    print(f"  {user1.model_dump()}")
    print()

    # Example 2: Create from dictionary
    print("Example 2: From dictionary")
    data = {"username": "user2", "password": "pass2"}
    user2 = LoginModel(**data)
    print(f"  {user2}")
    print()

    # Example 3: Use predefined users
    print("Example 3: Predefined users")
    standard_user = PredefinedUsers.get_user("standard")
    print(f"  {standard_user}")
    print(f"  Username: {standard_user.username}")
    print()

    # Example 4: Iterate all users
    print("Example 4: All users")
    for user in PredefinedUsers.all_users():
        print(f"  {user.username}")
    print()

    # Example 5: Validation
    print("Example 5: Validation (will raise error)")
    try:
        invalid_user = LoginModel(username="", password="pass")
    except Exception as e:
        print(f"  Validation error caught: {type(e).__name__}")
