from typing import Literal

from aiogram.types import Message
from aiogram.filters import Filter

from game.db.models import (
    Cell,
    Player
)
from game.db.session import s
from game.db.presets.base import CellType
from game.controllers.handlers.map.utils import directions


class MovementFilter(Filter):
    def __init__(self, cell_type: CellType | None = None):
        self.cell_type = cell_type

    async def __call__(
        self, message: Message, player: Player
    ) -> Literal[False] | dict[str, Cell]:
        if message.text in directions.keys():
            dir = directions[message.text]
            cell = await s.session.get(
                Cell,
                (player.region_id, player.x + dir[0], player.y + dir[1])
            )
            if not cell or (
                self.cell_type and cell.type.slug != self.cell_type.slug
            ):
                return False
            return {'dest': cell}

        return False
