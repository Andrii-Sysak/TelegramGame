import typing

from sqlalchemy.orm import Mapped, relationship, mapped_column

from game.db.base import Base
from game.db.types import int_pk, str50
if typing.TYPE_CHECKING:
    from game.db.models import Cell


class Region(Base):
    __tablename__ = 'region'

    id: Mapped[int_pk]
    name: Mapped[str50]
    x: Mapped[int]
    y: Mapped[int]
    size: Mapped[int | None] = mapped_column(default=None)

    map: Mapped[list['Cell']] = relationship(
        init=False,
        cascade='all,delete',
        lazy='selectin',
    )
