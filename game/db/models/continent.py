import typing

from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column
)

from game.db.base import Base
from game.db.types import int_pk, str50
if typing.TYPE_CHECKING:
    from game.db.models import Region



class Continent(Base):
    __tablename__ = 'continent'

    id: Mapped[int_pk] = mapped_column(init=False)
    name: Mapped[str50] = mapped_column()
    x: Mapped[int] = mapped_column()
    y: Mapped[int] = mapped_column()
    size: Mapped[int | None] = mapped_column(default=None)

    map: Mapped[list['Region']] = relationship(
        init = False,
        cascade='all,delete',
        lazy='selectin',
    )
