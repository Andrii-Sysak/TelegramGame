import typing

from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column
)

from game.db.base import Base
from game.db.types import int_pk, str50
if typing.TYPE_CHECKING:
    from game.db.models import Continent


class Planet(Base):
    __tablename__ = 'planet'

    id: Mapped[int_pk] = mapped_column(init=False)
    name: Mapped[str50] = mapped_column()

    continents: Mapped[list['Continent']] = relationship(
        init=False,
        cascade='all,delete',
        lazy='selectin',
    )
