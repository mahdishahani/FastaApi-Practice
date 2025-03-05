from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from src.repository.models.base import PyObjectId


class InvoiceModelSchema(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    customer_name: str
    amount: float
    status: str  # e.g., "paid", "pending", "cancelled"
    issued_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "customer_name": "John Doe",
                "amount": 150.75,
                "status": "pending",
                "issued_at": "2025-02-23T12:00:00Z"
            }
        }
