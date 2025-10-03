import logging
from fastapi import APIRouter, HTTPException

from src.api.dependencies import SessionDepend, UserDepend
from src.database.repository import UserRepository
from src.schemes import KeycloakUserScheme, UserScheme, SuccessScheme, UserListScheme

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/register")
async def register_user(user: KeycloakUserScheme, session: SessionDepend) -> SuccessScheme:
    logging.debug(f"Registering user: {user}")
    repo = UserRepository(session)
    await repo.add_user(user)
    return SuccessScheme()


@router.get("/userinfo")
async def get_user(session: SessionDepend, user: UserDepend) -> UserScheme:
    repo = UserRepository(session)
    res_user =  await repo.get_user(user.id)
    return res_user


@router.get("/{username}")
async def get_user_by_id(session: SessionDepend, username: str, user: UserDepend) -> UserListScheme:
    repo = UserRepository(session)
    res_user = await repo.get_user_by_username(username)
    if res_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return res_user
