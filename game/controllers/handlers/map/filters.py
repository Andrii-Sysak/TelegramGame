from typing import Literal

from aiogram.types import Message
from aiogram.filters import Filter

from game.db.models import (
    Cell,
    Player,
    Region
)
from game.db.session import s
from game.db.presets.base import CellType
from game.controllers.handlers.map.utils import directions
from sqlalchemy import select, and_


class MovementFilter(Filter):
    def __init__(self, cell_type: CellType | None = None):
        self.cell_type = cell_type

    async def __call__(
        self, message: Message, player: Player
    ) -> Literal[False] | dict[str, Cell]:
        if message.text in directions.keys():
            dir = directions[message.text]
            x, y = player.x + dir[0], player.y + dir[1]
            region_id = player.region_id

            if abs(x) == 11 or abs(y) == 11:
                x -= dir[0]
                y -= dir[1]
                region = await s.session.scalar(
                    select(Region).where(
                        and_(Region.x == player.region.x + dir[0],
                             Region.y == player.region.y + dir[1])
                    )
                )
                if region is not None:
                    region_id = region.id
                    x = -x if dir[0] else x
                    y = -y if dir[1] else y

            cell = await s.session.get(
                Cell,
                (region_id, x, y)
            )

            if not cell or (
                self.cell_type and cell.type.slug != self.cell_type.slug
            ):
                return False
            return {'dest': cell}
        return False
