from aiogram.types import Message
from sqlalchemy import select

from game.controllers.movement.utils import directions
from game.db.models import Player, Cell
from game.db.session import s


async def movement(message: Message, player: Player):
    if message.text in directions.keys():
        dir = directions[message.text]
        cell = await s.session.get(
            Cell,
            (player.region_id, player.x + dir[0], player.y + dir[1])
        )
        return {'dest': cell}

    return False
