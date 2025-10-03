from sqlalchemy.orm import Mapped
from src.database.core.data_types import intpk
from src.database.core.base import Base


class MatyanModel(Base):
    __tablename__ = "matyans"

    id: Mapped[intpk]
    name: Mapped[str]
    xp: Mapped[int]
