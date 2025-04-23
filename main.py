import asyncio

from src.db.main import init_db
asyncio.run(init_db())