from typing import (
    TYPE_CHECKING,
    Optional
)

from sqlalchemy import (
    Index,
    CheckConstraint
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
    soul_fk,
    region_fk
)

if TYPE_CHECKING:
    from game.db.models import (
        Soul,
        Region
    )
    from game.db.models.soul import BackgroundCells


class Player(Base):
    __tablename__ = 'player'
    __tableargs__ = (
        Index(None, 'region_id', 'x', 'y'),
        CheckConstraint('busyness_capacity < 18')
    )

    name: Mapped[str50] = mapped_column()
    id: Mapped[int_pk] = mapped_column(init=False)

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

    view: AssociationProxy[int] = association_proxy('soul', 'view', init=False)
    background_emoji: AssociationProxy['BackgroundCells'] = association_proxy(
        'soul', 'background_emoji', init=False
    )

    health: Mapped[int] = mapped_column(default=50)
    base_damage: Mapped[int] = mapped_column(default=10)
