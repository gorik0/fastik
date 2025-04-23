from src.config import Config
from sqlmodel import SQLModel, create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession

from sqlalchemy.orm import sessionmaker


engine = create_async_engine(url=Config.DATABASE_URL,echo=True)

async def init_db():

    async with engine.begin() as conn:
        from src.db.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session()->AsyncSession:
    Session = sessionmaker(bind=engine,expire_on_commit=False, class_ = AsyncSession)
    async with Session() as session:
        yield session