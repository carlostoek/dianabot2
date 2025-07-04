from aiogram import Router, F
from aiogram.types import Message
from services.user_service import UserService
from services.gamification_service import GamificationService

gamification_router = Router()
user_service = UserService()
gamification_service = GamificationService()

@gamification_router.message(F.text == "🎯 Misiones Diarias")
async def show_daily_missions(message: Message):
    user = await user_service.get_or_create_user(message.from_user)
    missions = await gamification_service.get_daily_missions(user.telegram_id)

    if not missions:
        await message.answer("No tienes misiones asignadas por ahora.")
        return

    response = "🎯 Tus Misiones Diarias:\n\n"
    for mission in missions:
        response += f"🔹 {mission.title}: {mission.description}\n"

    await message.answer(response)

@gamification_router.message(F.text == "🎁 Reclamar Recompensa Diaria")
async def claim_daily_reward(message: Message):
    user = await user_service.get_or_create_user(message.from_user)
    reward = await gamification_service.claim_daily_gift(user.telegram_id)

    if reward:
        await message.answer(f"Has reclamado {reward.besitos_reward} 💎 besitos y {reward.lore_reward} piezas de lore.")
    else:
        await message.answer("Ya reclamaste tu recompensa diaria hoy.")
