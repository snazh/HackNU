# from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
# from sqlalchemy.orm import relationship
# from datetime import datetime
# import enum
#
# from src.database import Base
#
#
# class MessageSender(enum.Enum):
#     user = "user"
#     bot = "bot"
#
#
# class Chat(Base):
#     __tablename__ = "chat"
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
#     title = Column(String(255), nullable=True)  # optional chat title
#     created_at = Column(DateTime, default=datetime.utcnow)
#
#     user = relationship("User", back_populates="chats")
#     messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
#
#
# class Message(Base):
#     __tablename__ = "message"
#     chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"))
#     sender = Column(Enum(MessageSender), nullable=False)
#     content = Column(Text, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#
#     chat = relationship("Chat", back_populates="messages")
