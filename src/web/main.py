# BUILTIN modules
import asyncio
from contextlib import asynccontextmanager

# Third party modules
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from src.business.logic.response_handler import MessageResponseLogic
from src.config.setup import settings
from src.repository.data_adapter import DataOperationsRepository
from src.repository.db import get_async_session, async_engine
from src.repository.models.invoice import InvoiceModelSchema
# Local modules
from src.tools.custom_logging import create_unified_logger
from src.tools.rabbit_client import AbstractRobustConnection, RabbitClient
from src.web.api.documentation import description, servers, tags_metadata
from src.web.health_manager import HealthManager


class Service(FastAPI):
    connection: AbstractRobustConnection = None

    def __init__(self, *args, **kwargs):
        """This class adds RabbitMQ message consumption and unified logging.

        :param args: named arguments.
        :param kwargs: key-value pair arguments.
        """
        super().__init__(*args, **kwargs)

        print(settings.model_dump())
        self.rabbit_client = RabbitClient(
            settings.rabbit_url, settings.service_name, self.process_response_message
        )
        self.level, self.logger = create_unified_logger(settings.service_log_level)

    async def process_response_message(self, message: dict):
        """Send response message to a separate asyncio task for processing.

        Note that the message is discarded when:
          - required metadata structure is missing in the message.
          - status is unknown.

        :param message: MicroService response message.
        """
        pass
        try:
            if not "metadata" in message:  # TODO Check Template Message
                raise RuntimeError(
                    "Message is discarded since it is "
                    "missing required metadata structure."
                )

            # Verify that message status is valid.
            #  TODO validate message with (field) in schema

            worker = MessageResponseLogic(repository=DataOperationsRepository())

            await asyncio.create_task(worker.process_response(message))

        except RuntimeError as why:
            self.logger.error(f"{why}")

        except ValueError as why:
            raw = f"{why}".split("\n")
            errmsg = " ".join([item.split("(type=")[0].strip() for item in raw[1:]])
            self.logger.error(f"Message is discarded since {errmsg}.")


@asynccontextmanager
async def lifespan(service: Service):
    await startup(service)
    yield
    await shutdown(service)


app = Service(
    servers=servers,
    title=settings.name,
    lifespan=lifespan,
    version=settings.version,
    description=description,
    openapi_tags=tags_metadata,
)


async def startup(service: Service):
    """Initialize RabbitMQ."""

    service.logger.info("Establishing RabbitMQ message queue consumer...")
    service.connection = await asyncio.create_task(service.rabbit_client.consume())


async def shutdown(service: Service):
    """Close RabbitMQ."""

    if service.connection:
        service.logger.info("Disconnecting from RabbitMQ...")
        await service.connection.close()


@app.get(
    "/health",
    tags=["health check endpoint"],
)
async def health_check() -> JSONResponse:
    """**Health check endpoint.**"""
    content = await HealthManager(
        app.connection, DataOperationsRepository()
    ).get_status()
    response_code = 200 if content.status else 500
    return JSONResponse(status_code=response_code, content=content.model_dump())


@app.post("/test_write")
async def test_write(
        data: dict,
        db: AsyncIOMotorClient = Depends(get_async_session)
):
    try:
        model_instance = InvoiceModelSchema(**data)
        collection = db["invoice"]
        await collection.insert_one(model_instance.model_dump())
        return {"message": "Write successful"}
    except Exception as e:
        print(e)
        return {"error": f"Error during write: {str(e)}"}
