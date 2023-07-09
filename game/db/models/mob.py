from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from game.db import Base
from game.db.types import (
    int_pk,
    str50,
    mob_fk,
    cell_type_fk,
)
if TYPE_CHECKING:
    from game.db.models import CellType


class Mob(Base):
    __tablename__ = 'mob'

    id: Mapped[int_pk]
    name: Mapped[str50]
    emoji: Mapped[str50]
    health: Mapped[int] = mapped_column(default=50)
    bade_damage: Mapped[int] = mapped_column(default=10)

    cells: Mapped[list[CellType]] = relationship(
        secondary='mob__cell_type',
        init=False,
        viewonly=True
    )


class Mob2CellType(Base):
    __tablename__ = 'mob__cell_type'
    __tableargs__ = (
        CheckConstraint('rate >= 0 AND rate <= 100')
    )

    mob_id: Mapped[mob_fk] = mapped_column(primary_key=True, init=False)
    mob: Mapped[Mob] = relationship()
    cell_type_id: Mapped[cell_type_fk] = mapped_column(
        primary_key=True, init=False
    )
    cell_type: Mapped['CellType'] = relationship()
    rate: Mapped[int] = mapped_column(default=50)
