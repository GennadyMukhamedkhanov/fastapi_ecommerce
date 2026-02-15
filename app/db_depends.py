from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Предоставляет асинхронную сессию SQLAlchemy для работы с базой данных PostgreSQL.
    """
    session = async_session_maker()

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()

    # async with async_session_maker() as session:
    #     yield session


@asynccontextmanager
async def get_session_manager_commit():
    async for session in get_async_db():
        yield session


async def func():
    async with get_session_manager_commit() as db:
        await db.execute()
