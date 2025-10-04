import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
from src.database.core.data_types import intpk
from src.database.core.base import Base


class FriendRequestModel(Base):
    __tablename__ = "friend_requests"

    id: Mapped[intpk]
    user_id: Mapped[Annotated[uuid.UUID, mapped_column(ForeignKey("users.id"))]]
    friend_id: Mapped[Annotated[uuid.UUID, mapped_column(ForeignKey("users.id"))]]
    user: Mapped["UserModel"] = relationship(back_populates="friend_requests_to",
                                             foreign_keys="FriendRequestModel.user_id")
    friend: Mapped["UserModel"] = relationship(back_populates="friend_requests_from",
                                               foreign_keys="FriendRequestModel.friend_id")
