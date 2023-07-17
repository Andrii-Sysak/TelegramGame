from enum import StrEnum

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from sqlalchemy_utils import ChoiceType

from game.db.base import Base
from game.db.types import int_pk


class BackgroundCells(StrEnum):
    default = '⬜'
    minus = '➖'
    dark = '◼'
    small = '▫'


class Soul(Base):
    __tablename__ = 'soul'

    id: Mapped[int_pk] = mapped_column()

    view: Mapped[int] = mapped_column(default=5)
    background_emoji: Mapped[BackgroundCells] = mapped_column(
        ChoiceType(BackgroundCells, impl=String(2)),
        default=BackgroundCells.default
    )

    fire_element: Mapped[int] = mapped_column(default=5)
    water_element: Mapped[int] = mapped_column(default=5)
    tree_element: Mapped[int] = mapped_column(default=5)
    metal_element: Mapped[int] = mapped_column(default=5)
    earth_element: Mapped[int] = mapped_column(default=5)
