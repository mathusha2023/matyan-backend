import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
from src.database.core.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[Annotated[uuid.UUID, mapped_column(primary_key=True)]]
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[Annotated[str, mapped_column(unique=True, index=True)]]
    email: Mapped[Annotated[str, mapped_column(unique=True)]]
    lvl1_solved: Mapped[Annotated[bool, mapped_column(default=False)]]
    lvl2_solved: Mapped[Annotated[bool, mapped_column(default=False)]]
    lvl3_solved: Mapped[Annotated[bool, mapped_column(default=False)]]
    last_login: Mapped[Annotated[datetime, mapped_column(default=datetime.now())]]
