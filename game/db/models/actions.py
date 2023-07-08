from datetime import datetime
from enum import (
    StrEnum,
    auto,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from game.db import Base
from game.db.types import (
    player_fk,
    int_pk,
)


class ActionBusynessLevel(StrEnum):
    none = 0
    low = 1
    medium = 3
    high = 5
    blocking = 9


class Action(Base):
    __tablename__ = 'action'

    id: Mapped[int_pk]

    player_id: Mapped[player_fk]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]

    busyness_level: Mapped[ActionBusynessLevel] = mapped_column(
        default=ActionBusynessLevel.none
    )
