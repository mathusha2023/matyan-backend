from keycloak import KeycloakOpenID
from src.settings import settings

keycloak_openid = KeycloakOpenID(
    server_url=settings.keycloak_url,
    client_id=settings.keycloak_client,
    realm_name=settings.keycloak_realm,
    client_secret_key=settings.keycloak_secret,
    verify=False
)