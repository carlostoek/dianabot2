
from sqlalchemy.future import select
from database_init import get_db
from models.vip import VIPToken, VIPAccess
from models.core import User
from datetime import datetime, timedelta

class VIPService:
    async def validate_vip_token(self, telegram_id, token_str):
        async for session in get_db():
            result = await session.execute(select(VIPToken).where(VIPToken.token == token_str))
            token = result.scalar_one_or_none()

            if token and token.used_count < token.max_uses and token.expires_at > datetime.utcnow():
                token.used_count += 1
                await session.commit()

                user_result = await session.execute(select(User).where(User.telegram_id == telegram_id))
                user = user_result.scalar_one_or_none()

                if user:
                    vip_access = VIPAccess(
                        user_id=user.id,
                        channel_id=123456789,
                        access_expires=datetime.utcnow() + timedelta(days=30)
                    )
                    session.add(vip_access)
                    await session.commit()
                    return True
            return False
