from contextvars import ContextVar
from functools import wraps
from typing import Callable

from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker,
    AsyncSession
)

_session = ContextVar[AsyncSession]('session', default=None)

eng = create_async_engine(
    'postgresql+psycopg://postgres:postgres@localhost:5432/postgres',
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
    def session(self, value: AsyncSession):
        _session.set(value)


s = _Session()


def session(f: Callable):
    @wraps(f)
    async def decorator(*args, **kwargs):
        s.session = s.maker()
        try:
            await f(*args, **kwargs)
            await s.session.commit()
        finally:
            await s.session.close()

    return decorator
