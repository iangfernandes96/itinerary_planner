"""Database configuration and session management.

This module provides database connection management, session handling,
and connection pooling for both read and write operations.
"""

import contextlib
import os
from typing import AsyncIterator, Literal

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

# Load environment variables once
load_dotenv()

Base = declarative_base()

# Common database configuration
COMMON_ENGINE_CONFIG = {
    "pool_pre_ping": True,
    "echo": bool(os.getenv("SQL_ECHO", False)),
}

READ_CONFIG = {
    **COMMON_ENGINE_CONFIG,
    "pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 10,
    "execution_options": {"isolation_level": "READ COMMITTED"},
}

WRITE_CONFIG = {
    **COMMON_ENGINE_CONFIG,
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
}

# Convert the URL to async format
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "").replace(
    "postgresql://", "postgresql+asyncpg://"
)


class DatabaseError(Exception):
    """Base exception for database errors."""

    pass


class DatabaseSessionManager:
    """Manages database sessions and connections."""

    def __init__(self) -> None:
        """Initialize session manager with empty engine and sessionmaker instances."""
        self._write_engine: AsyncEngine | None = None
        self._read_engine: AsyncEngine | None = None
        self._write_sessionmaker: async_sessionmaker | None = None
        self._read_sessionmaker: async_sessionmaker | None = None

    def init(self, host: str) -> None:
        """Initialize database engines and session factories."""
        if not host:
            raise DatabaseError("Database URL not provided")

        self._write_engine = create_async_engine(host, **WRITE_CONFIG)
        self._read_engine = create_async_engine(host, **READ_CONFIG)

        self._write_sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._write_engine, expire_on_commit=False
        )

        self._read_sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._read_engine, expire_on_commit=False
        )

    async def close(self) -> None:
        """Close all database connections."""
        if self._write_engine:
            await self._write_engine.dispose()
        if self._read_engine:
            await self._read_engine.dispose()
        self._write_engine = None
        self._read_engine = None
        self._write_sessionmaker = None
        self._read_sessionmaker = None

    async def _handle_transaction_error(
        self, error: Exception, connection: AsyncConnection | None = None
    ) -> None:
        """Handle transaction errors with proper rollback."""
        if connection:
            await connection.rollback()
        raise DatabaseError(f"Database transaction failed: {str(error)}") from error

    @contextlib.asynccontextmanager
    async def connect(
        self, mode: Literal["read", "write"] = "write"
    ) -> AsyncIterator[AsyncConnection]:
        """Get a database connection with automatic error handling."""
        engine = self._write_engine if mode == "write" else self._read_engine
        if engine is None:
            raise DatabaseError("DatabaseSessionManager is not initialized")

        async with engine.begin() as connection:
            try:
                yield connection
            except Exception as e:
                await self._handle_transaction_error(e, connection)

    @contextlib.asynccontextmanager
    async def session(
        self, mode: Literal["read", "write"] = "write"
    ) -> AsyncIterator[AsyncSession]:
        """Get a database session with automatic error handling."""
        sessionmaker = (
            self._write_sessionmaker if mode == "write" else self._read_sessionmaker
        )
        if sessionmaker is None:
            raise DatabaseError("DatabaseSessionManager is not initialized")

        session = sessionmaker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            await self._handle_transaction_error(e)
        finally:
            await session.close()

    async def create_all(self, connection: AsyncConnection) -> None:
        """Create all database tables."""
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection) -> None:
        """Drop all database tables."""
        await connection.run_sync(Base.metadata.drop_all)


# Initialize session manager
sessionmanager = DatabaseSessionManager()
sessionmanager.init(SQLALCHEMY_DATABASE_URL)


async def get_write_db() -> AsyncIterator[AsyncSession]:
    """Get a write database session."""
    async with sessionmanager.session(mode="write") as session:
        yield session


async def get_read_db() -> AsyncIterator[AsyncSession]:
    """Get a read database session."""
    async with sessionmanager.session(mode="read") as session:
        yield session
