import uuid
from typing import List

from fastapi import APIRouter, HTTPException

from src.api.dependencies import SessionDepend, UserDepend
from src.database.repository import UserRepository
from src.schemes import SuccessScheme, FriendRequestScheme, UserListScheme, MyFriendRequestScheme, UserFriendsScheme

router = APIRouter(tags=["Friends"], prefix="/users/friends")


# запросы дружбы, отправленные МНЕ
@router.get("/requests")
async def get_friend_requests(session: SessionDepend, user: UserDepend) -> List[FriendRequestScheme]:
    repo = UserRepository(session)
    res = await repo.get_friend_requests(user.id)
    return res


# запросы дружбы, отправленные МНОЮ
@router.get("/requests/my")
async def get_my_friend_requests(session: SessionDepend, user: UserDepend) -> List[MyFriendRequestScheme]:
    repo = UserRepository(session)
    res = await repo.get_my_friend_requests(user.id)
    return res


@router.post("/requests/{friend_id}")
async def send_friend_request(friend_id: uuid.UUID, session: SessionDepend, user: UserDepend) -> SuccessScheme:
    if str(friend_id) == str(user.id):
        raise HTTPException(status_code=400, detail="You can't send a friend request to yourself")
    repo = UserRepository(session)
    try:
        await repo.send_friend_request(user.id, friend_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return SuccessScheme()


@router.delete("/requests/{friend_id}")
async def cancel_friend_request(friend_id: uuid.UUID, session: SessionDepend, user: UserDepend) -> SuccessScheme:
    repo = UserRepository(session)
    await repo.cancel_friend_request(user.id, friend_id)
    return SuccessScheme()


@router.post("/requests/{request_id}/answer")
async def answer_friend_request(request_id: int, accept: bool, session: SessionDepend, user: UserDepend) -> SuccessScheme:
    repo = UserRepository(session)
    try:
        await repo.answer_friend_request(request_id, user.id, accept)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return SuccessScheme()

@router.get("")
async def get_friends(session: SessionDepend, user: UserDepend) -> List[UserFriendsScheme]:
    repo = UserRepository(session)
    res = await repo.get_friends(user.id)
    return res


@router.delete("/{friend_id}")
async def cancel_friend_request(friend_id: uuid.UUID, session: SessionDepend, user: UserDepend) -> SuccessScheme:
    repo = UserRepository(session)
    await repo.delete_friend(user.id, friend_id)
    return SuccessScheme()
