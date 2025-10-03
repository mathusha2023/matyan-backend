from sqlalchemy.ext.asyncio import AsyncSession
from src.models import UserModel
from src.schemes import KeycloakUserScheme


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


