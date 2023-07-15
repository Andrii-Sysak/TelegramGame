import typing as t
import asyncio

from game.db.session import session

DELAYED_COROUTINE_RETURN_TYPE = t.TypeVar('DELAYED_COROUTINE_RETURN_TYPE')


@session
async def delay(
    coro: t.Awaitable[DELAYED_COROUTINE_RETURN_TYPE],
    _delay: int,
    /
) -> DELAYED_COROUTINE_RETURN_TYPE:
    await asyncio.sleep(_delay)
    return await coro
