import asyncio
import typing as t


DELAYED_COROUTINE_RETURN_TYPE = t.TypeVar('DELAYED_COROUTINE_RETURN_TYPE')


async def delay(
    coro: t.Awaitable[DELAYED_COROUTINE_RETURN_TYPE],
    _delay: int,
    /
) -> DELAYED_COROUTINE_RETURN_TYPE:
    await asyncio.sleep(_delay)
    return await coro
