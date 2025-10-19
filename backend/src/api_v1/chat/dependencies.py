from src.api_v1.chat.service import ChatService, MessageService

def get_chat_service() -> ChatService:
    return ChatService()

def get_message_service() -> MessageService:
    return MessageService()
