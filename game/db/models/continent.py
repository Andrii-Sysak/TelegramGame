from typing import (
    TYPE_CHECKING,
    Optional,
)

from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column
)

from game.db.base import Base
from game.db.types import (
    int_pk,
    str50,
    planet_fk,
)
if TYPE_CHECKING:
    from game.db.models import (
        Planet,
        Region,
    )


class Continent(Base):
    __tablename__ = 'continent'

    id: Mapped[int_pk] = mapped_column(init=False)
    name: Mapped[str50] = mapped_column()

    planet: Mapped[Optional['Planet']] = relationship(lazy='joined')
    planet_id: Mapped[planet_fk] = mapped_column(
        unique=False, nullable=True, default=None
    )

    regions: Mapped[list['Region']] = relationship(
        init=False,
        cascade='all,delete',
        lazy='selectin',
    )
