import typing as t
from functools import wraps
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

_session = ContextVar[AsyncSession]('session',)

eng = create_async_engine(
    'postgresql+psycopg://admin:admin@bot-postgres:5432/game',
    echo=True,
    isolation_level='AUTOCOMMIT'
)
sesm = async_sessionmaker(eng)


class _Session:
    maker = sesm

    @property
    def session(self) -> AsyncSession:
        return _session.get()

    @session.setter
    def session(self, value: AsyncSession) -> None:
        _session.set(value)


s = _Session()


DECORATED_FUNCTION = t.TypeVar(
    'DECORATED_FUNCTION', bound=t.Callable[..., t.Awaitable]
)


def session(f: DECORATED_FUNCTION) -> DECORATED_FUNCTION:
    @wraps(f)
    async def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
        s.session = s.maker()
        try:
            r = await f(*args, **kwargs)
            await s.session.commit()
        finally:
            await s.session.close()
        return r
    return t.cast(DECORATED_FUNCTION, decorator)
