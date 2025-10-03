import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated, Optional
from src.database.core.data_types import intpk
from src.database.core.base import Base


class GroupModel(Base):
    __tablename__ = "groups"

    id: Mapped[intpk]
    name: Mapped[str]
    member1_id: Mapped[Annotated[uuid.UUID, mapped_column(ForeignKey("users.id"))]]
    member2_id: Mapped[Annotated[Optional[uuid.UUID], mapped_column(ForeignKey("users.id"))]]
    member3_id: Mapped[Annotated[Optional[uuid.UUID], mapped_column(ForeignKey("users.id"))]]
    member4_id: Mapped[Annotated[Optional[uuid.UUID], mapped_column(ForeignKey("users.id"))]]
    member5_id: Mapped[Annotated[Optional[uuid.UUID], mapped_column(ForeignKey("users.id"))]]
    matyan_id: Mapped[Annotated[int, mapped_column(ForeignKey("matyans.id"))]]
