from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from game.db.base import Base
from game.db.models.region import Region
from game.db.types import intpk, str50


class CellType(Base):
    __tablename__ = 'cell_type'

    id: Mapped[intpk]
    slug: Mapped[str50]
    emoji: Mapped[str50]
    passable: Mapped[bool]


class Cell(Base):
    __tablename__ = 'cell'

    region_id: Mapped[intpk] = mapped_column(
        ForeignKey(Region.id, ondelete='CASCADE'), init=True
    )
    x: Mapped[intpk] = mapped_column(init=True)
    y: Mapped[intpk] = mapped_column(init=True)
    cell_type_id: Mapped[int] = mapped_column(ForeignKey(CellType.id))

    type: Mapped[CellType] = relationship(lazy='joined', init=False)

    @property
    def emoji(self):
        return self.type.emoji

    def __str__(self):
        return self.emoji
