import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from game.db.base import Base
from game.db.models.region import Region
from game.db.types import str50


class BackgroundCells(enum.StrEnum):
    default = '⬜'
    minus = '➖'
    dark = '◼'
    small = '▫'


class Player(Base):
    __tablename__ = 'player'

    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str50]

    region_id: Mapped[int] = mapped_column(ForeignKey(Region.id), default=1)
    x: Mapped[int] = mapped_column(default=0)
    y: Mapped[int] = mapped_column(default=0)

    view: Mapped[int] = mapped_column(default=5)
    emoji: Mapped[str50] = mapped_column(default='👻')
    background_emoji: Mapped[BackgroundCells] = mapped_column(
        default=BackgroundCells.default
    )

    region: Mapped[Region] = relationship(lazy='joined', init=False)
