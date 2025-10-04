import uuid
from datetime import datetime
from src.schemes.base import BaseScheme


class UserListScheme(BaseScheme):
    id: uuid.UUID
    username: str
    first_name: str
    last_name: str


class KeycloakUserScheme(UserListScheme):
    email: str


class UserScheme(KeycloakUserScheme):
    lvl1_solved: bool
    lvl2_solved: bool
    lvl3_solved: bool
    last_login: datetime
    created_at: datetime


class UserFriendsScheme(UserListScheme):
    last_login: datetime
