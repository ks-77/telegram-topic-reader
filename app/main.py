import datetime
import json

from fastapi import FastAPI, Request

from app.collecting.models import TelegramMessage
from app.database import sync_session_maker

app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    chat_id = None
    sender_first_name = None
    sender_last_name = None
    sender_username = None
    message_date = None
    topic_name = None

    if "message" in data:
        message = data["message"]
        chat = message.get("chat", {})
        chat_id = chat.get("id", None)

        sender = message.get("from", {})
        sender_first_name = sender.get("first_name", None)
        sender_last_name = sender.get("last_name", None)
        sender_username = sender.get("username", None)

        if "date" in message:
            message_date = datetime.datetime.fromtimestamp(message["date"])

        if "forum_topic_created" in message:
            forum_topic = message["forum_topic_created"]
            topic_name = forum_topic.get("name", None)

    try:
        telegram_message = TelegramMessage(
            chat_id=str(chat_id) if chat_id is not None else None,
            sender_first_name=sender_first_name,
            sender_last_name=sender_last_name,
            sender_username=sender_username,
            message_date=message_date,
            topic_name=topic_name,
            update_data=json.dumps(data)
        )
        sync_session_maker.add(telegram_message)
        sync_session_maker.commit()
    except Exception as e:
        sync_session_maker.rollback()
        print("Error saving message:", e)
    finally:
        sync_session_maker.close()

    return {"ok": True}
