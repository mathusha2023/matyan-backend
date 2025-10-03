from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.core import db_session
from src.keycloak.auth import get_current_user

SessionDepend = Annotated[AsyncSession, Depends(db_session.create_session)]
UserDepend = Depends(get_current_user)
