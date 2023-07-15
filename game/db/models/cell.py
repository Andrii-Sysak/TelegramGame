from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column
)
from sqlalchemy.ext.associationproxy import (
    AssociationProxy,
    association_proxy
)

from game.db.base import Base
from game.db.types import (
    str50,
    int_pk,
    cell_type_fk
)
from game.db.models.region import Region


class CellType(Base):
    __tablename__ = 'cell_type'

    id: Mapped[int_pk] = mapped_column(init=False)
    slug: Mapped[str50] = mapped_column()
    emoji: Mapped[str50] = mapped_column()
    passable: Mapped[bool] = mapped_column(default=False)
    transparent: Mapped[bool] = mapped_column(default=False)

    def __hash__(self) -> int:
        return hash(self.id)


class Cell(Base):
    __tablename__ = 'cell'

    cell_type_id: Mapped[cell_type_fk]
    type: Mapped[CellType] = relationship(lazy='joined', init=False)

    region_id: Mapped[int_pk] = mapped_column(
        ForeignKey(Region.id, ondelete='CASCADE'), init=True
    )

    x: Mapped[int_pk] = mapped_column(init=True)
    y: Mapped[int_pk] = mapped_column(init=True)

    emoji: AssociationProxy[str] = association_proxy('type', 'emoji')

    def __str__(self) -> str:
        return self.emoji
