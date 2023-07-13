from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from game.db.base import Base
from game.db.models.region import Region
from game.db.types import (
    int_pk,
    str50,
    cell_type_fk,
)


class CellType(Base):
    __tablename__ = 'cell_type'

    id: Mapped[int_pk]
    slug: Mapped[str50]
    emoji: Mapped[str50]
    passable: Mapped[bool] = mapped_column(default=False)
    transparent: Mapped[bool] = mapped_column(default=False)

    def __hash__(self):
        return hash(self.id)


class Cell(Base):
    __tablename__ = 'cell'

    region_id: Mapped[int_pk] = mapped_column(
        ForeignKey(Region.id, ondelete='CASCADE'), init=True
    )
    x: Mapped[int_pk] = mapped_column(init=True)
    y: Mapped[int_pk] = mapped_column(init=True)
    cell_type_id: Mapped[cell_type_fk]

    type: Mapped[CellType] = relationship(lazy='joined', init=False)

    emoji = association_proxy('type', 'emoji')

    def __str__(self):
        return self.emoji
