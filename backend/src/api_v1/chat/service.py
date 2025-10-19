from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.api_v1.common.base_service import BaseService
from src.models.chat import Chat, Message
from src.api_v1.chat.schemas import ChatModelSchema, ChatCreateSchema, MessageModelSchema, MessageCreateSchema

class ChatService(BaseService[Chat, ChatModelSchema]):
    def __init__(self):
        super().__init__(Chat, ChatModelSchema)

    async def get_user_chats(self, user_id: int, session: AsyncSession) -> List[ChatModelSchema]:
        stmt = select(Chat).where(Chat.user_id == user_id)
        result = await session.execute(stmt)
        chats = result.scalars().all()
        return [self._to_schema(chat) for chat in chats]

class MessageService(BaseService[Message, MessageModelSchema]):
    def __init__(self):
        super().__init__(Message, MessageModelSchema)

    async def get_chat_messages(self, chat_id: int, session: AsyncSession) -> List[MessageModelSchema]:
        stmt = select(Message).where(Message.chat_id == chat_id)
        result = await session.execute(stmt)
        messages = result.scalars().all()
        return [self._to_schema(message) for message in messages]
