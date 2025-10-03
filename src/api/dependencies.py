from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.core import db_session
from src.keycloak.auth import get_current_user
from src.schemes import UserAuthScheme

SessionDepend = Annotated[AsyncSession, Depends(db_session.create_session)]
UserDepend = Annotated[UserAuthScheme, Depends(get_current_user)]
