from typing import Optional, List

from pydantic import BaseModel


class UserAuthScheme(BaseModel):
    id: str
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: List[str] = []
    is_active: bool = True


class AuthUrlScheme(BaseModel):
    auth_url: str


class TokenScheme(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    expires_in: int
    token_type: str


class RefreshTokenScheme(BaseModel):
    refresh_token: str


class UserRoleScheme(BaseModel):
    roles: List[str]