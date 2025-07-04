from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.user_service import UserService
from services.gamification_service import GamificationService

gamification_router = Router()
user_service = UserService()
gamification_service = GamificationService()

@gamification_router.callback_query(F.data == "daily_missions")
async def show_daily_missions(callback: CallbackQuery):
    user = await user_service.get_or_create_user(callback.from_user)
    missions = await gamification_service.get_daily_missions(user.telegram_id)

    if not missions:
        await callback.message.edit_text("No tienes misiones asignadas por ahora.")
        return

    response = "🎯 Tus Misiones Diarias:\n\n"
    for mission in missions:
        response += f"🔹 {mission.title}: {mission.description}\n"

    await callback.message.edit_text(response)

@gamification_router.callback_query(F.data == "claim_daily")
async def claim_daily_reward(callback: CallbackQuery):
    user = await user_service.get_or_create_user(callback.from_user)
    reward = await gamification_service.claim_daily_gift(user.telegram_id)

    if reward:
        await callback.message.edit_text(
            f"Has reclamado {reward.besitos_reward} 💎 besitos y {reward.lore_reward} piezas de lore."
        )
    else:
        await callback.message.edit_text("Ya reclamaste tu recompensa diaria hoy.")
