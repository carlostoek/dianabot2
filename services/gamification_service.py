
from sqlalchemy.future import select
from database_init import get_db
from models.gamification import Mission, UserMission
from random import randint

class GamificationService:
    async def get_available_missions(self, telegram_id):
        async for session in get_db():
            from models.core import User
            user_result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = user_result.scalar_one_or_none()

            result = await session.execute(
                select(Mission).join(UserMission, isouter=True).where(UserMission.user_id != user.id if UserMission.user_id else True)
            )
            missions = result.scalars().all()

            return missions

    async def start_mission(self, telegram_id, mission_id):
        async for session in get_db():
            from models.core import User
            user_result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = user_result.scalar_one_or_none()

            new_user_mission = UserMission(
                user_id=user.id,
                mission_id=mission_id,
                progress=0,
                completed=False,
                claimed=False
            )
            session.add(new_user_mission)
            await session.commit()

    async def complete_mission(self, telegram_id):
        async for session in get_db():
            from models.core import User
            user_result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = user_result.scalar_one_or_none()

            result = await session.execute(
                select(UserMission).where(UserMission.user_id == user.id, UserMission.completed == False)
            )
            mission = result.scalar_one_or_none()

            if mission:
                mission.progress += 1

                if randint(1, 2) == 1:  # 50% chance de completar misión
                    mission.completed = True

                await session.commit()
                return mission.completed
            return False
