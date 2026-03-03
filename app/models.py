from typing import Literal

from pydantic import BaseModel, Field

FieldType = Literal["solana", "evm"]


class ChatRequest(BaseModel):
    field: FieldType = Field(..., description="Chain field: solana or evm")
    message: str = Field(..., min_length=1, description="User message")


class ChatResponse(BaseModel):
    reply: str
