from sqlalchemy import Column, String, Integer, Text, DateTime

from app.database import Base


class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String(100), index=True)
    sender_first_name = Column(String(100), nullable=True)
    sender_last_name = Column(String(100), nullable=True)
    sender_username = Column(String(100), nullable=True)
    message_date = Column(DateTime, nullable=True)
    topic_name = Column(String(255), nullable=True)
    update_data = Column(Text)
