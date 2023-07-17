import typing as t
import asyncio
from datetime import (
    datetime,
    timedelta
)
from functools import wraps

from aiogram import flags
from sqlalchemy import delete

from game.db.models import Player
from game.db.session import s
from game.utils.delay import delay
from game.db.models.action import (
    Action,
    ActionBusynessLevel
)

DECORATED_FUNCTION = t.TypeVar(
    'DECORATED_FUNCTION', bound=t.Callable[..., t.Awaitable]
)


def action(
    level: ActionBusynessLevel, _delay: int | t.Callable[[], int]
) -> t.Callable[[DECORATED_FUNCTION], DECORATED_FUNCTION]:
    """
    decorator factory for automated workflow(creation, deletion)
    decorated function must accept 'player' argument
    If you need to use some data that will be initialized later(e.x. config)
    you can pass a callable as a delay
    """
    def decorator(f: DECORATED_FUNCTION) -> DECORATED_FUNCTION:
        f = flags.action(level)(f)

        @wraps(f)
        async def wrapper(
            *args: t.Any, player: Player, **kwargs: t.Any
        ) -> t.Any:
            seconds = _delay() if callable(_delay) else _delay
            a = Action(
                player_id=player.id,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(seconds=seconds),
                busyness_level=level
            )
            s.session.add(a)
            await s.session.flush()
            result = await f(*args, player=player, **kwargs)
            asyncio.create_task(delay(
                s.session.execute(delete(Action).where(Action.id == a.id)),
                seconds
            ))
            return result
        return t.cast(DECORATED_FUNCTION, wrapper)
    return decorator
