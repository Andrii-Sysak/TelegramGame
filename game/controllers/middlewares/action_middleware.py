import typing as t
from datetime import datetime

from aiogram import BaseMiddleware
from sqlalchemy import select
from aiogram.types import (
    Message,
    TelegramObject
)
from aiogram.dispatcher.flags import get_flag

from game.db.models import Player
from game.db.session import s
from game.db.models.action import Action


class ActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: t.Callable[[Message, dict[str, t.Any]], t.Awaitable[t.Any]],
        event: TelegramObject,
        data: dict[str, t.Any],
    ) -> None:
        if not isinstance(event, Message):
            raise NotImplementedError(
                f'Expected Message event type; Got: {type(event)}'
            )
        player: Player = data['player']
        action: int = get_flag(data, 'action')
        if action is not None:
            player_busyness = sum((await s.session.scalars(
                select(Action.busyness_level)
                .where(Action.player_id == player.id)
                .where(Action.end_date > datetime.utcnow())
            )).all())

            if action > (player.busyness_capacity - player_busyness):
                await event.answer('Ти надто зайнятий! Зачекай!')
                return

        await handler(event, data)
