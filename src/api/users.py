import logging
from fastapi import APIRouter

from src.api.dependencies import SessionDepend
from src.database.repository import UserRepository
from src.schemes import KeycloakUserScheme

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/register")
async def register_user(user: KeycloakUserScheme, session: SessionDepend):
    logging.debug(f"Registering user: {user}")
    repo = UserRepository(session)
    await repo.add_user(user)
    return {"message": "Success"}


