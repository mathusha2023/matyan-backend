import uuid
from typing import List

from fastapi import APIRouter, HTTPException

from src.api.dependencies import SessionDepend, UserDepend
from src.database.repository import UserRepository
from src.schemes import SuccessScheme, FriendRequestScheme

router = APIRouter(tags=["Friends"], prefix="/users/friends")


@router.post("/requests/{friend_id}")
async def send_friend_request(friend_id: uuid.UUID, session: SessionDepend, user: UserDepend) -> SuccessScheme:
    if str(friend_id) == str(user.id):
        raise HTTPException(status_code=400, detail="You can't send a friend request to yourself")
    repo = UserRepository(session)
    res = await repo.send_friend_request(user.id, friend_id)
    if res is None:
        raise HTTPException(status_code=404, detail="User not found")
    return SuccessScheme()


@router.get("/requests")
async def get_friend_requests(session: SessionDepend, user: UserDepend) -> List[FriendRequestScheme]:
    repo = UserRepository(session)
    res = await repo.get_friend_requests(user.id)
    return res


