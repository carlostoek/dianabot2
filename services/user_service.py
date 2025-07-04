
from sqlalchemy.future import select
from database_init import get_db
from models.core import User

class UserService:
    async def get_or_create_user(self, telegram_user):
        async for session in get_db():
            result = await session.execute(select(User).where(User.telegram_id == telegram_user.id))
            user = result.scalar_one_or_none()

            if user:
                return user

            new_user = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name or "Usuario"
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    async def set_onboarded(self, user):
        async for session in get_db():
            user.is_onboarded = True
            session.add(user)
            await session.commit()
