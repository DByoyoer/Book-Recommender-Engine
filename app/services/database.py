import contextlib
from typing import Any, AsyncIterator

from config import settings
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


# Code from https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308 and
# https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html=
class DatabaseSessionManager:
    def __init__(self, con_url: URL, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(con_url, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine, expire_on_commit=False)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    def engine_exists(self):
        return self._engine is not None


sessionmanager = DatabaseSessionManager(settings.database_url, {"echo": settings.echo_sql})


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session
