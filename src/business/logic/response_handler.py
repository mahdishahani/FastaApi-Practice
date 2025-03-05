# builtins modules
from importlib.metadata import metadata
from typing import Any

# Third party modules

from loguru import logger

# Local modules
from src.repository.data_adapter import DataOperationsRepository

ALL_OPERATIONS = []


class MessageResponseLogic:
    """
    This class implements the Collector business logic layer
    for RabbitMQ response messages.
    """

    def __init__(self, repository: DataOperationsRepository):
        """The class initializer.

        :param repository: Data layer handler object.
        """
        self.repo = repository

    async def _paid_invoice_and_save_to_db(self, message):
        ...

    async def _recognize_user_id(self, user_id, owner_id):
        ...

    async def _recognize_address_id(self, address_id, owner_id):
        ...

    async def _recognize_product_id(self, product_id, owner_id):
        ...

    async def _save_invoice_item_by_invoice_obj(
            self, item_data: list, invoices: Any, owner_id
    ):
        ...

    async def process_response(self, message: dict):
        """Process response message data.
        Implemented business logic:
          - Every received message state is updated in DB.
        :param message: Response message data.
        """
        body, meta_data, operation = message.get("data"), message.get("metadata"), message.get("operation")

        # return body, meta_data, operation

        print(body, "-------", meta_data, "--------", operation)

    @staticmethod
    async def _validate_message(message) -> tuple[str, dict, str]:
        body, meta_data, operation = message.get("data"), message.get("metadata"), message.get("operation")
        if not body or not meta_data or not operation:
            raise ValueError("Message must contain an (data, metadata, operation)")
        if not operation in ALL_OPERATIONS:
            raise ValueError("Message must contain an (data, metadata, operation)")

        return body, meta_data, operation
