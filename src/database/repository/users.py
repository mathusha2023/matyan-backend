import uuid
from typing import Optional

from sqlalchemy import select, func, and_, or_, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import UserModel, FriendRequestModel, FriendModel
from src.schemes import KeycloakUserScheme, UserScheme, FriendRequestScheme, UserListScheme, MyFriendRequestScheme, \
    UserFriendsScheme


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

    async def check_friends(self, user_id: uuid.UUID, friend_id: uuid.UUID):
        query = select(func.count(FriendModel.id)).filter(
            or_(and_(FriendModel.user_id == user_id, FriendModel.friend_id == friend_id),
                and_(FriendModel.user_id == friend_id, FriendModel.friend_id == user_id)))
        res = await self.session.execute(query)
        return res.scalar() > 0

    async def get_user(self, user_id: uuid.UUID):
        query = select(UserModel).filter(UserModel.id == user_id)
        res = await self.session.execute(query)
        db_user: Optional[UserModel] = res.scalar()
        if db_user is None:
            raise Exception("User not found")
        return UserScheme.model_validate(db_user)

    async def get_user_by_username(self, username: str):
        query = select(UserModel).filter(UserModel.username == username)
        res = await self.session.execute(query)
        db_user: Optional[UserModel] = res.scalar()
        if db_user is None:
            raise Exception("User not found")
        return UserListScheme.model_validate(db_user)

    async def send_friend_request(self, user_id: uuid.UUID, friend_id: uuid.UUID):
        if not await self.check_users_exists(user_id, friend_id):
            raise Exception("User not found")
        if await self.check_friends(user_id, friend_id):  # already friends
            raise Exception("Already friends")
        req = FriendRequestModel(user_id=user_id, friend_id=friend_id)
        try:
            self.session.add(req)
            await self.session.commit()
            return req.id
        except IntegrityError as e:
            raise Exception("Friend request already exists")

    async def cancel_friend_request(self, user_id: uuid.UUID, friend_id: uuid.UUID):
        query = delete(FriendRequestModel).filter(FriendRequestModel.user_id == user_id, FriendRequestModel.friend_id == friend_id)
        await self.session.execute(query)
        await self.session.commit()

    async def get_friend_requests(self, user_id: uuid.UUID):
        query = select(FriendRequestModel).options(
            selectinload(FriendRequestModel.user)).filter(FriendRequestModel.friend_id == user_id)
        res = await self.session.execute(query)
        friends: [FriendRequestModel] = res.scalars().all()
        return [FriendRequestScheme.model_validate(f) for f in friends]

    async def get_my_friend_requests(self, user_id: uuid.UUID):
        query = select(FriendRequestModel).options(
            selectinload(FriendRequestModel.friend)).filter(FriendRequestModel.user_id == user_id)
        res = await self.session.execute(query)
        users: [FriendRequestModel] = res.scalars().all()
        return [MyFriendRequestScheme.model_validate(f) for f in users]

    async def answer_friend_request(self, id: int, friend_id: uuid.UUID, accept: bool):
        query = select(FriendRequestModel).filter(FriendRequestModel.id == id)
        res = await self.session.execute(query)
        req: Optional[FriendRequestModel] = res.scalar()
        if req is None:
            raise Exception("Friend request not found")
        if str(req.friend_id) != str(friend_id):
            raise Exception("It is not your friend request")
        if accept:
            f: FriendModel = FriendModel(user_id=req.user_id, friend_id=req.friend_id)
            self.session.add(f)
        await self.session.delete(req)
        await self.session.commit()
        return accept

    async def get_friends(self, user_id: uuid.UUID):
        query1 = select(FriendModel).options(selectinload(FriendModel.friend)).filter(FriendModel.user_id == user_id)
        query2 = select(FriendModel).options(selectinload(FriendModel.user)).filter(FriendModel.friend_id == user_id)
        res1 = await self.session.execute(query1)
        res2 = await self.session.execute(query2)
        friends1 = [UserFriendsScheme.model_validate(f.friend) for f in res1.scalars().all()]
        friends2 = [UserFriendsScheme.model_validate(f.user) for f in res2.scalars().all()]
        return friends1 + friends2

    async def delete_friend(self, user_id: uuid.UUID, friend_id: uuid.UUID):
        query1 = delete(FriendModel).filter(FriendModel.user_id == user_id, FriendModel.friend_id == friend_id)
        query2 = delete(FriendModel).filter(FriendModel.user_id == friend_id, FriendModel.friend_id == user_id)
        await self.session.execute(query1)
        await self.session.execute(query2)
        await self.session.commit()

