import typing as t

from aiogram import BaseMiddleware
from sqlalchemy import select
from aiogram.types import (
    Message,
    TelegramObject
)

from game.db.models import Player
from game.db.session import s
from game.controllers.handlers.registration.states import Reg


class SessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: t.Callable[[Message, dict[str, t.Any]], t.Awaitable[t.Any]],
        event: TelegramObject,
        data: dict[str, t.Any]
    ) -> None:
        if not isinstance(event, Message):
            raise NotImplementedError(
                f'Expected Message event type; Got: {type(event)}'
            )
        s.session = s.maker()
        player = await s.session.scalar(
            select(Player)
            .where(Player.soul_id == data['event_from_user'].id)
        )
        if player:
            data['player'] = player
        elif data['raw_state'] is None:
            await data['state'].set_state(Reg.unregistered)
            data['raw_state'] = Reg.unregistered.state
        try:
            await handler(event, data)
            await s.session.commit()
        finally:
            await s.session.close()
        return None
