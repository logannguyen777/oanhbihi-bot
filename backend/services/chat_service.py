import openai
from models.chat_log import ChatLog
from models.enum import RoleEnum
from models.user import get_or_create_user
from sqlalchemy.orm import Session
from datetime import datetime
from .utils.context import get_recent_context

def chat_with_context_service(payload, db: Session):
    # 👤 Tạo hoặc lấy user từ DB
    user = get_or_create_user(payload.sender_id, payload.channel, db)

    # 📝 Ghi lại tin nhắn của người dùng
    db.add(ChatLog(
        user_id=user.id,
        session_id=payload.session_id,
        channel=payload.channel,
        role=RoleEnum.user,
        message=payload.message,
        timestamp=datetime.utcnow(),
    ))
    db.commit()

    # 📚 Lấy lại lịch sử chat gần đây (context)
    context_logs = get_recent_context(user.id, db)

    messages = []
    for log in context_logs:
        role = log.role.value
        if role == "bot":
            role = "assistant"  # ✅ Chuyển 'bot' → 'assistant'
        messages.append({"role": role, "content": log.message})

    # ➕ Thêm câu mới của user
    messages.append({"role": "user", "content": payload.message})

    try:
        # 🤖 Gọi OpenAI để lấy phản hồi
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        print(f"❌ Lỗi khi gọi OpenAI: {e}")
        bot_reply = "Oanh Bihi đang hơi lag 🥺, bạn thử lại sau chút xíu nha~"

    # 💬 Lưu tin nhắn của bot vào DB
    db.add(ChatLog(
        user_id=user.id,
        session_id=payload.session_id,
        channel=payload.channel,
        role=RoleEnum.bot,  # 🧠 DB vẫn lưu là 'bot'
        message=bot_reply,
        timestamp=datetime.utcnow(),
    ))
    db.commit()

    return bot_reply
