
from sqlalchemy.future import select
from database_init import get_db
from models.core import User
from models.gamification import Mission, UserMission
from datetime import datetime

async def assign_daily_missions(bot):
    async for session in get_db():
        result = await session.execute(select(User))
        users = result.scalars().all()

        mission_result = await session.execute(select(Mission).where(Mission.mission_type == "daily"))
        daily_missions = mission_result.scalars().all()

        for user in users:
            for mission in daily_missions:
                new_user_mission = UserMission(
                    user_id=user.id,
                    mission_id=mission.id,
                    progress=0,
                    completed=False,
                    claimed=False
                )
                session.add(new_user_mission)

            try:
                await bot.send_message(user.telegram_id, "🎯 Tienes nuevas misiones diarias disponibles.")
            except Exception:
                pass

        await session.commit()
