
from sqlalchemy.future import select
from database_init import get_db
from models.gamification import Mission
from models.vip import VIPToken
from datetime import datetime, timedelta
import random
import string
from models.core import User

class AdminService:
    async def create_mission(self, title, description, reward_besitos):
        async for session in get_db():
            new_mission = Mission(
                mission_type="story",
                title=title,
                description=description,
                reward_besitos=reward_besitos
            )
            session.add(new_mission)
            await session.commit()

    async def generate_vip_token(self, max_uses=1, days_valid=30):
        async for session in get_db():
            token_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            new_token = VIPToken(
                token=token_str,
                max_uses=max_uses,
                expires_at=datetime.utcnow() + timedelta(days=days_valid)
            )
            session.add(new_token)
            await session.commit()
            return token_str
    async def get_basic_stats(self):
        async for session in get_db():
            from sqlalchemy import func
            user_count = await session.scalar(select(func.count(User.id)))
            token_count = await session.scalar(select(func.count(VIPToken.id)))
            return {"users": user_count or 0, "vip_tokens": token_count or 0}

    async def broadcast(self, bot, text: str):
        async for session in get_db():
            result = await session.execute(select(User.telegram_id))
            user_ids = [row[0] for row in result.all()]
        for uid in user_ids:
            try:
                await bot.send_message(uid, text)
            except Exception:
                pass

