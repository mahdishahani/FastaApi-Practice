# builtins modules

# Third party modules
from motor.motor_asyncio import AsyncIOMotorClient

# Local modules
from src.config.setup import settings

MONGODB_URL = (
    f"mongodb://{settings.database_username}:{settings.database_password}@"
    f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}?authSource=admin"
)

async_engine = AsyncIOMotorClient(MONGODB_URL)
database = async_engine[settings.database_name]


async def get_async_session():
    yield database
