
from sqlalchemy.future import select
from database_init import get_db
from models.gamification import Mission
from models.vip import VIPToken
from datetime import datetime, timedelta
import random
import string

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
