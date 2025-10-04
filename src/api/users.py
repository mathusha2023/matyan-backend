import logging
from fastapi import APIRouter, HTTPException

from src.api.dependencies import SessionDepend, UserDepend, TokenDepend
from src.database.repository import UserRepository
from src.schemes import KeycloakUserScheme, UserScheme, SuccessScheme, UserListScheme

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/register")
async def register_user(user: KeycloakUserScheme, session: SessionDepend, token_verify: TokenDepend) -> SuccessScheme:
    logging.debug(f"Registering user: {user}")
    repo = UserRepository(session)
    await repo.add_user(user)
    return SuccessScheme()


@router.get("/userinfo")
async def get_user(session: SessionDepend, user: UserDepend) -> UserScheme:
    repo = UserRepository(session)
    res_user =  await repo.get_user(user.id)
    return res_user


@router.get("/userinfo/{username}")
async def get_user_by_username(session: SessionDepend, username: str, user: UserDepend) -> UserListScheme:
    repo = UserRepository(session)
    try:
        res_user = await repo.get_user_by_username(username)
        return res_user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
