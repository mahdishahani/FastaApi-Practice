# Third party modules
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

# Local modules
from src.repository.db import get_async_session


class DataOperationsRepository:
    @staticmethod
    async def _write(model_instance):
        pass

    @staticmethod
    async def _update(model_instance):
        pass

    async def _read(self, db: AsyncIOMotorClient = Depends(get_async_session)):
        pass
