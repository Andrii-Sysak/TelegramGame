import enum
from typing import (
    TYPE_CHECKING,
    Optional,
)

from sqlalchemy import (
    ForeignKey,
    Index,
    CheckConstraint,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from game.db.base import Base
from game.db.types import (
    str50,
    int_pk,
    region_fk,
    soul_fk,
)
if TYPE_CHECKING:
    from game.db.models import Region, Soul
    from game.db.models.soul import BackgroundCells


class Player(Base):
    __tablename__ = 'player'
    __tableargs__ = (
        Index(None, 'region_id', 'x', 'y'),
        CheckConstraint('busyness_capacity < 18')
    )

    id: Mapped[int_pk]
    name: Mapped[str50]

    soul: Mapped[Optional['Soul']] = relationship(lazy='joined')
    soul_id: Mapped[soul_fk] = mapped_column(
        unique=True, nullable=True, default=None
    )

    busyness_capacity: Mapped[int] = mapped_column(default=10)

    region_id: Mapped[region_fk] = mapped_column(default=1)
    x: Mapped[int] = mapped_column(default=0)
    y: Mapped[int] = mapped_column(default=0)

    emoji: Mapped[str50] = mapped_column(default='👻')

    region: Mapped['Region'] = relationship(lazy='joined', init=False)

    view: int = association_proxy('soul', 'view', init=False)
    background_emoji: 'BackgroundCells' = association_proxy(
        'soul', 'background_emoji', init=False
    )
