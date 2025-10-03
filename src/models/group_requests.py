from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
from src.database.core.data_types import intpk
from src.database.core.base import Base


class GroupRequestModel(Base):
    __tablename__ = "group_requests"

    id: Mapped[intpk]
    group_id: Mapped[Annotated[int, mapped_column(ForeignKey("groups.id"))]]
    user_id: Mapped[Annotated[int, mapped_column(ForeignKey("users.id"))]]
    friend_id: Mapped[Annotated[int, mapped_column(ForeignKey("users.id"))]]
