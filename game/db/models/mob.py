from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column
)

from game.db.base import Base
from game.db.types import (
    str50,
    int_pk,
    mob_fk,
    cell_type_fk
)

if TYPE_CHECKING:
    from game.db.models import CellType


class Mob(Base):
    __tablename__ = 'mob'

    id: Mapped[int_pk] = mapped_column(init=False)
    name: Mapped[str50] = mapped_column()
    emoji: Mapped[str50] = mapped_column()
    health: Mapped[int] = mapped_column(default=50)
    bade_damage: Mapped[int] = mapped_column(default=10)

    cells: Mapped[list['CellType']] = relationship(
        secondary='mob__cell_type',
        init=False,
        viewonly=True,
        lazy='noload'
    )


class Mob2CellType(Base):
    __tablename__ = 'mob__cell_type'
    __tableargs__ = (
        CheckConstraint('rate >= 0 AND rate <= 100')
    )

    mob_id: Mapped[mob_fk] = mapped_column(primary_key=True, init=False)
    mob: Mapped[Mob] = relationship(lazy='joined')
    cell_type_id: Mapped[cell_type_fk] = mapped_column(
        primary_key=True, init=False
    )
    cell_type: Mapped['CellType'] = relationship(lazy='joined')
    rate: Mapped[int] = mapped_column(default=50)
