from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, Literal
from enum import Enum


class MessageOperation(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    READ = "read"
    CREATE_INVOICE = "create_invoice"

    # Add other operations as needed


class MessageBody(BaseModel):
    content: str = Field(..., min_length=1, description="Message content")
    type: str = Field(..., description="Message type")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional message data")


class MessageMetadata(BaseModel):
    sender: str = Field(..., description="Message sender identifier")
    timestamp: str = Field(..., description="Message timestamp")
    version: str = Field(default="1.0", description="Message version")


class Message(BaseModel):
    body: MessageBody
    metadata: MessageMetadata
    operation: MessageOperation
