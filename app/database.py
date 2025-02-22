import contextlib
from typing import AsyncIterator, Literal
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import declarative_base

load_dotenv()

Base = declarative_base()

# Convert the URL to async format
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "").replace(
    "postgresql://", "postgresql+asyncpg://"
)


class DatabaseSessionManager:
    def __init__(self):
        self._write_engine: AsyncEngine | None = None
        self._read_engine: AsyncEngine | None = None
        self._write_sessionmaker: async_sessionmaker | None = None
        self._read_sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        # Write engine optimized for write operations
        self._write_engine = create_async_engine(
            host,
            pool_size=5,  # Smaller pool for writes
            max_overflow=10,
            pool_timeout=30,
            pool_pre_ping=True
        )

        # Read engine optimized for read operations
        self._read_engine = create_async_engine(
            host,
            pool_size=20,  # Larger pool for reads
            max_overflow=30,
            pool_timeout=10,
            pool_pre_ping=True,
            execution_options={
                "isolation_level": "READ COMMITTED"
            }
        )

        self._write_sessionmaker = async_sessionmaker(
            autocommit=False,
            bind=self._write_engine,
            expire_on_commit=False
        )

        self._read_sessionmaker = async_sessionmaker(
            autocommit=False,
            bind=self._read_engine,
            expire_on_commit=False
        )

    async def close(self):
        if self._write_engine:
            await self._write_engine.dispose()
        if self._read_engine:
            await self._read_engine.dispose()
        self._write_engine = None
        self._read_engine = None
        self._write_sessionmaker = None
        self._read_sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self, mode: Literal["read", "write"] = "write") -> AsyncIterator[AsyncConnection]:    # noqa
        engine = self._write_engine if mode == "write" else self._read_engine
        if engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self, mode: Literal["read", "write"] = "write") -> AsyncIterator[AsyncSession]:   # noqa
        sessionmaker = self._write_sessionmaker if mode == "write" else self._read_sessionmaker # noqa
        if sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


# Initialize session manager
sessionmanager = DatabaseSessionManager()
sessionmanager.init(SQLALCHEMY_DATABASE_URL)


async def get_write_db():
    async with sessionmanager.session(mode="write") as session:
        yield session


async def get_read_db():
    async with sessionmanager.session(mode="read") as session:
        yield session
