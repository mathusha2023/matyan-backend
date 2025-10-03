from fastapi import APIRouter, HTTPException
from starlette import status
from src.keycloak.keycloak_openid import keycloak_openid
from src.api.dependencies import UserDepend
from src.schemes import RefreshTokenScheme, TokenScheme, AuthUrlScheme, UserRoleScheme
from src.settings import settings
from src.schemes import UserAuthScheme as User

router = APIRouter(tags=["Authorization"], prefix="/auth")


@router.get("/login")
async def login_redirect() -> AuthUrlScheme:
    """
    Генерирует URL для перенаправления на Keycloak
    """
    auth_url = await keycloak_openid.auth_url(
        redirect_uri=settings.keycloak_redirect_url,
        scope="openid email profile",
        state="random_state_string"
    )
    return AuthUrlScheme(auth_url=auth_url)


@router.get("/callback")
async def auth_callback(code: str) -> TokenScheme:
    """
    Обрабатывает callback от Keycloak после аутентификации
    """
    try:
        # Обмен code на токены
        tokens = await keycloak_openid.token(
            grant_type="authorization_code",
            code=code,
            redirect_uri=settings.keycloak_redirect_url
        )

        return TokenScheme(
            access_token=tokens["access_token"],
            refresh_token=tokens.get("refresh_token"),
            expires_in=tokens["expires_in"],
            token_type=tokens["token_type"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {str(e)}"
        )


@router.post("/refresh")
async def refresh_token(refresh_token: RefreshTokenScheme) -> TokenScheme:
    """
    Обновление access token с помощью refresh token
    """
    try:
        tokens = await keycloak_openid.refresh_token(refresh_token.refresh_token)
        return TokenScheme(
            access_token=tokens["access_token"],
            refresh_token=tokens.get("refresh_token"),
            expires_in=tokens["expires_in"],
            token_type=tokens["token_type"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.post("/logout")
async def logout(refresh_token: RefreshTokenScheme) -> dict:
    """
    Выход из системы (инвалидация токенов)
    """
    try:
        await keycloak_openid.logout(refresh_token.refresh_token)
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Logout failed: {str(e)}"
        )


@router.get("/me", summary="Get all user data")
async def get_user_data(user: User = UserDepend) -> User:
    """
    Получение информации о пользователе из токена
    """
    return user


@router.get("/roles", summary="Get user roles")
async def get_roles(user: User = UserDepend) -> UserRoleScheme:
    """
    Получение ролей пользователя из токена
    """
    return UserRoleScheme(roles=user.roles)