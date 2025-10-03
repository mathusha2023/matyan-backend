from typing import List

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from src.keycloak.keycloak_openid import keycloak_openid
from src.schemes import UserAuthScheme as User

security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Асинхронно проверяет токен и возвращает информацию о пользователе
    """
    try:
        token = credentials.credentials

        # Интроспекция токена
        token_info = await keycloak_openid.introspect(token)

        if not token_info.get("active"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is not active"
            )

        # Получение информации о пользователе
        user_info = await keycloak_openid.userinfo(token)

        return User(
            id=user_info.get("sub"),
            username=user_info.get("preferred_username"),
            email=user_info.get("email"),
            first_name=user_info.get("given_name"),
            last_name=user_info.get("family_name"),
            roles=token_info.get("realm_access", {}).get("roles", [])
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


def require_role(required_roles: List[str]):
    """
    Фабрика зависимостей для проверки ролей
    """

    async def role_checker(user: User = Depends(get_current_user)):
        if not any(role in user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {required_roles}"
            )
        return user

    return role_checker