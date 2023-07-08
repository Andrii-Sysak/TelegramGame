from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy import select

from game.controllers.handlers.registration.states import Reg
from game.db.models import Player
from game.db.session import s


class SessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> None:
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
