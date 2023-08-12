from sqlalchemy import (
    ForeignKey,
    CheckConstraint,
    JSON
)
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
    cell_type_fk,
)
from game.db.models.region import Region

class CellType(Base):
    __tablename__ = 'cell_type'
    __tableargs__ = (
        CheckConstraint("permeability >= 0 AND permeability <= 100")
    )

    slug: Mapped[str50] = mapped_column(primary_key=True)
    emoji: Mapped[str50] = mapped_column()
    permeability: Mapped[int] = mapped_column(default=50)
    transparent: Mapped[bool] = mapped_column(default=False)

    def __hash__(self) -> int:
        return hash(self.slug)


class Cell(Base):
    __tablename__ = 'cell'

    cell_type_slug: Mapped[cell_type_fk] = mapped_column()
    type: Mapped[CellType] = relationship(lazy='joined', init=False)

    region_id: Mapped[int_pk] = mapped_column(
        ForeignKey(Region.id, ondelete='CASCADE'), init=True
    )

    x: Mapped[int_pk] = mapped_column(init=True)
    y: Mapped[int_pk] = mapped_column(init=True)

    emoji: AssociationProxy[str] = association_proxy(
        'type', 'emoji', init=False
    )

    unique_data : Mapped[dict] = mapped_column(type_=JSON, init=True, default_factory=dict)

    def __str__(self) -> str:
        return self.emoji
