import uuid
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import UserModel, FriendRequestModel
from src.schemes import KeycloakUserScheme, UserScheme, FriendRequestScheme, UserListScheme


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user: KeycloakUserScheme):
        db_user = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        self.session.add(db_user)
        await self.session.commit()
        return user.id

    async def check_users_exists(self, *user_ids):
        query = select(func.count(UserModel.id)).filter(UserModel.id.in_(user_ids))
        res = await self.session.execute(query)
        return len(user_ids) == res.scalar()

    async def get_user(self, user_id: uuid.UUID):
        query = select(UserModel).filter(UserModel.id == user_id)
        res = await self.session.execute(query)
        db_user: Optional[UserModel] = res.scalar()
        if db_user is None:
            return None
        return UserScheme.model_validate(db_user)

    async def get_user_by_username(self, username: str):
        query = select(UserModel).filter(UserModel.username == username)
        res = await self.session.execute(query)
        db_user: Optional[UserModel] = res.scalar()
        if db_user is None:
            return None
        return UserListScheme.model_validate(db_user)

    async def send_friend_request(self, user_id: uuid.UUID, friend_id: uuid.UUID):
        if not self.check_users_exists(user_id, friend_id):
            return None
        req = FriendRequestModel(user_id=user_id, friend_id=friend_id)
        self.session.add(req)
        await self.session.commit()
        return req.id

    async def get_friend_requests(self, user_id: uuid.UUID):
        query = select(FriendRequestModel).options(
            selectinload(FriendRequestModel.user)).filter(FriendRequestModel.friend_id == user_id)
        res = await self.session.execute(query)
        friends: List[FriendRequestModel] = res.scalars().all()
        return [FriendRequestScheme.model_validate(req) for req in friends]

