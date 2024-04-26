from sqlalchemy.ext.asyncio import AsyncSession

from app.baskend.db import async_session_maker


async def get_db() -> AsyncSession:
    db = async_session_maker()
    try:
        yield db
    finally:
        await db.close()
