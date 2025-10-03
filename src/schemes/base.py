from pydantic import BaseModel, ConfigDict


class BaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=False)


class SuccessScheme(BaseScheme):
    message: str = "Success"
