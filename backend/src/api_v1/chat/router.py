from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.chat.schemas import ChatCreateSchema, MessageCreateSchema
from src.api_v1.chat.service import ChatService, MessageService
from src.database.db import get_async_session
from typing import List

router = APIRouter(prefix="/chats", tags=["Chats"])

@router.post("/", status_code=status.HTTP_200_OK)
async def create_chat(chat_data: ChatCreateSchema,
                      session: AsyncSession = Depends(get_async_session),
                      service: ChatService = Depends(get_chat_service)):
    new_chat = await service.create(item_data=chat_data, session=session)
    return {"status": "Success", "msg": "Chat created", "data": new_chat}


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_chats(user_id: int,
                         session: AsyncSession = Depends(get_async_session),
                         service: ChatService = Depends(get_chat_service)):
    chats = await service.get_user_chats(user_id=user_id, session=session)
    return {"status": "Success", "msg": "User chats fetched", "data": chats}


@router.post("/messages", status_code=status.HTTP_200_OK)
async def create_message(message_data: MessageCreateSchema,
                         session: AsyncSession = Depends(get_async_session),
                         service: MessageService = Depends(get_message_service)):
    new_message = await service.create(item_data=message_data, session=session)
    return {"status": "Success", "msg": "Message sent", "data": new_message}


@router.get("/{chat_id}/messages", status_code=status.HTTP_200_OK)
async def get_chat_messages(chat_id: int,
                            session: AsyncSession = Depends(get_async_session),
                            service: MessageService = Depends(get_message_service)):
    messages = await service.get_chat_messages(chat_id=chat_id, session=session)
    return {"status": "Success", "msg": "Chat messages fetched", "data": messages}


