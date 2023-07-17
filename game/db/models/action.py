import enum
from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from sqlalchemy_utils import ChoiceType

from game.db.base import Base
from game.db.types import (
    int_pk,
    player_fk
)


class ActionBusynessLevel(enum.IntEnum):
    none = 0
    low = 1
    medium = 3
    high = 5
    blocking = 9


class Action(Base):
    __tablename__ = 'action'

    id: Mapped[int_pk] = mapped_column(init=False)

    player_id: Mapped[player_fk] = mapped_column()
    start_date: Mapped[datetime] = mapped_column()
    end_date: Mapped[datetime] = mapped_column()

    busyness_level: Mapped[ActionBusynessLevel] = mapped_column(
        ChoiceType(ActionBusynessLevel, impl=Integer()),
        default=ActionBusynessLevel.none
    )
