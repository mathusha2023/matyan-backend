import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
from src.database.core.data_types import intpk
from src.database.core.base import Base


class FriendModel(Base):
    __tablename__ = "friends"

    id: Mapped[intpk]
    user_id: Mapped[Annotated[uuid.UUID, mapped_column(ForeignKey("users.id"), index=True)]]
    friend_id: Mapped[Annotated[uuid.UUID, mapped_column(ForeignKey("users.id"), index=True)]]
    user: Mapped["UserModel"] = relationship(back_populates="friend_to",
                                             foreign_keys="FriendModel.user_id")
    friend: Mapped["UserModel"] = relationship(back_populates="friend_from",
                                               foreign_keys="FriendModel.friend_id")
