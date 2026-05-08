from pydantic import BaseModel, EmailStr, Field
from pydantic_settings import SettingsConfigDict


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OkResponse(BaseModel):
    ok: bool


class UserResponse(BaseModel):

    model_config = SettingsConfigDict(from_attributes=True)

    id: str
    email: str
    role: str
    display_name: str | None


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenClaim(BaseModel):
    sid: str = Field(description="Base64 session id")
    uid: str = Field(description="User id")
    iat: int = Field(description="Issued at (Unix timestamp in seconds)")
    lra: int = Field(description="Last refreshed at (Unix timestamp in seconds)")
    iea: int = Field(
        description="Idle expires at -- when can access no longer be refreshed with current token (Unix timestamp in seconds)"
    )
    mea: int = Field(
        description="Max expires at -- when the user MUST login again for access (Unix timestamp in seconds)"
    )


class PublicSessionResponse(BaseModel):
    sessions: list[dict] = Field(
        description="List of public session dictionaries containing the public session id and session info"
    )


class RevocationRequest(BaseModel):
    ids_to_revoke: list[str] = Field(
        description="list of public session ids to revoke immediately"
    )


class RevocationResponse(BaseModel):
    revoked_ids: list[str] = Field(
        description="list of public session ids that were revoked"
    )
