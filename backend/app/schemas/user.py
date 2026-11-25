from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Fields shared by user representations."""

    username: str = Field(
        description="Unique username used to identify the account.",
        examples=["jane_doe"],
    )
    email: EmailStr = Field(
        description="Email address associated with the account.",
        examples=["jane@example.com"],
    )


class UserCreate(UserBase):
    """Request payload for creating a new user account."""

    password: str = Field(
        description="Password for the new account.",
        examples=["A-secure-password123"],
    )


class UserLogin(BaseModel):
    """Request payload for authenticating with a username and password."""

    username: str = Field(
        description="Username associated with the account.",
        examples=["jane_doe"],
    )
    password: str = Field(
        description="Password associated with the account.",
        examples=["A-secure-password123"],
    )


class User(UserBase):
    """Public representation of a user account."""

    id: int = Field(
        description="Database identifier for the user.",
        examples=[42],
    )

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """OAuth2 access token returned after successful authentication."""

    access_token: str = Field(
        description="Bearer token used to authorize protected API requests.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example"],
    )
    token_type: str = Field(
        default="bearer",
        description="Type of authorization token.",
        examples=["bearer"],
    )


class TokenData(BaseModel):
    """Decoded identity data extracted from an access token."""

    username: str | None = Field(
        default=None,
        description="Username stored in the token subject, if available.",
        examples=["jane_doe"],
    )


class ErrorResponse(BaseModel):
    """Standard error payload returned by API endpoints."""

    detail: str = Field(
        description="Human-readable description of the error.",
        examples=["The requested resource was not found"],
    )