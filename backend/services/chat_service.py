from sqlalchemy.orm import Session
from datetime import datetime
from models.chat_log import ChatLog
from models.enum import RoleEnum
from models.user import get_or_create_user
from .utils.context import get_recent_context
from services.openai_client import get_openai_client


def chat_with_context_service(payload, db: Session):
    # 👤 Tạo hoặc lấy user
    user = get_or_create_user(payload.sender_id, payload.channel, db)

    # 📝 Ghi lại tin nhắn của người dùng
    try:
        db.add(ChatLog(
            user_id=user.id,
            session_id=payload.session_id,
            channel=payload.channel,
            role=RoleEnum.user,
            message=payload.message,
            timestamp=datetime.utcnow(),
        ))
        db.commit()
    except Exception as e:
        print(f"❌ Lỗi ghi log user: {e}")
        db.rollback()

    # 📚 Lấy context gần đây
    try:
        context_logs = get_recent_context(user.id, db)
        messages = []

        for log in context_logs:
            role = log.role.value
            if role == "bot":
                role = "assistant"
            messages.append({"role": role, "content": log.message})

        messages.append({"role": "user", "content": payload.message})
    except Exception as e:
        print(f"❌ Lỗi khi lấy context: {e}")
        messages = [{"role": "user", "content": payload.message}]

    # 🔑 Lấy OpenAI client từ cấu hình DB
    try:
        client = get_openai_client(db)
    except Exception as e:
        print(f"❌ Lỗi khi lấy OpenAI client: {e}")
        return "Oanh Bihi đang hơi lag 🥺, bạn thử lại sau chút xíu nha~"

    # 🤖 Gọi OpenAI lấy phản hồi
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        print(f"❌ Lỗi khi gọi OpenAI: {e}")
        bot_reply = "Oanh Bihi đang hơi lag 🥺, bạn thử lại sau chút xíu nha~"

    # 💬 Lưu phản hồi của bot
    try:
        db.add(ChatLog(
            user_id=user.id,
            session_id=payload.session_id,
            channel=payload.channel,
            role=RoleEnum.bot,
            message=bot_reply,
            timestamp=datetime.utcnow(),
        ))
        db.commit()
    except Exception as e:
        print(f"❌ Lỗi ghi log bot: {e}")
        db.rollback()

    return bot_reply
