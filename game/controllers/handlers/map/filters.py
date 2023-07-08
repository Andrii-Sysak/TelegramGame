from datetime import datetime
from typing import Literal

from aiogram.types import Message
from sqlalchemy import select

from game.controllers.handlers.map.utils import directions
from game.db.models import Player, Cell
from game.db.models.actions import Action
from game.db.session import s


async def in_action(
    message: Message, player: Player
) -> Literal[False] | dict[str, Action]:
    action = await s.session.scalar(
        select(Action)
        .where(Action.player_id == player.id)
        .where(Action.end_date > datetime.utcnow())
    )
    if action:
        return {'action': action}
    return False


async def movement(
    message: Message, player: Player
) -> Literal[False] | dict[str, Cell]:
    if message.text in directions.keys():
        dir = directions[message.text]
        cell = await s.session.get(
            Cell,
            (player.region_id, player.x + dir[0], player.y + dir[1])
        )
        return {'dest': cell}

    return False
