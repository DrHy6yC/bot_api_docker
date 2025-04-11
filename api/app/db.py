from typing import Annotated
from collections.abc import AsyncGenerator


from fastapi import Depends
from sqlmodel import Session, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


sqlite_file_name = "database.db"
DATABASE_URL = f"sqlite+aiosqlite:///./{sqlite_file_name}"


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_async_session)]
