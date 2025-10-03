import uuid
from datetime import datetime

from src.schemes import UserListScheme
from src.schemes.base import BaseScheme


class FriendRequestScheme(BaseScheme):
    id: int
    friend_id: uuid.UUID
    user: UserListScheme
    created_at: datetime


