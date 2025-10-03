from pydantic import BaseModel


class KeycloakUserScheme(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
