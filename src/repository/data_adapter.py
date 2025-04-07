# Third party modules
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

# Local modules
from src.repository.db import get_async_session, async_engine, MONGODB_URL


class DataOperationsRepository:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db

    async def create(
            self, collection: str, data: dict,
    ):
        result = await self.db[collection].insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    async def _update(model_instance):
        pass

    async def _read(self, db: AsyncIOMotorClient = Depends(get_async_session)):
        pass
