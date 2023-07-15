import typing

from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column
)

from game.db.base import Base
from game.db.types import (
    str50,
    int_pk
)

if typing.TYPE_CHECKING:
    from game.db.models import Cell


class Region(Base):
    __tablename__ = 'region'

    id: Mapped[int_pk] = mapped_column(init=False)
    name: Mapped[str50] = mapped_column()
    x: Mapped[int] = mapped_column()
    y: Mapped[int] = mapped_column()
    size: Mapped[int | None] = mapped_column(default=None)

    map: Mapped[list['Cell']] = relationship(
        init=False,
        cascade='all,delete',
        lazy='selectin',
    )
