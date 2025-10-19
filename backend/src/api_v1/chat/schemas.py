from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from src.models.chat import MessageSender

class MessageCreateSchema(BaseModel):
    chat_id: int
    sender: MessageSender
    content: str
    model_config = ConfigDict(from_attributes=True)

class MessageModelSchema(MessageCreateSchema):
    id: int
    created_at: datetime

class ChatCreateSchema(BaseModel):
    user_id: int
    title: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ChatModelSchema(ChatCreateSchema):
    id: int
    created_at: datetime
    messages: List[MessageModelSchema] = []
