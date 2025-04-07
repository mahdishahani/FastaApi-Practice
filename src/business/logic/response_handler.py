# builtins modules
from importlib.metadata import metadata
from typing import Any

# Third party modules

from loguru import logger

# Local modules
from src.repository.data_adapter import DataOperationsRepository
from src.business.schemas.message_schema import Message, MessageBody, MessageMetadata, MessageOperation
from src.repository.models.invoice import InvoiceModelSchema

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

    async def _create_invoice(self, validated_data: dict):
        try:
            invoice_data = InvoiceModelSchema(**validated_data).model_dump(by_alias=True)

            print("invoice data ---------------------", invoice_data)

            result = await self.repo.create("invoices", invoice_data)
            return result
        except Exception as e:
            raise ValueError(f"Failed to create invoice: {str(e)}")

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
        print("message -------------------", message)
        validated_data = self._validate_message(message)
        body, meta_data, operation = validated_data.body, validated_data.metadata, validated_data.operation

        print("data ------------------------------", body.model_dump().get("data"))

        if operation.value == MessageOperation.CREATE_INVOICE.value:
            invoice_id = await self._create_invoice(body.model_dump().get("data"))
            print(f"Invoice created with ID: {invoice_id}")

        # return body, meta_data, operation

        print(body, "-------", meta_data, "--------", operation)

    @staticmethod
    def _validate_message(message: dict) -> Message:
        try:
            validated_message = Message(
                body=MessageBody(**message.get('body', {})),
                metadata=MessageMetadata(**message.get('metadata', {})),
                operation=message.get('operation')
            )
            return validated_message
        except Exception as e:
            raise ValueError(f"Message validation failed: {str(e)}")
