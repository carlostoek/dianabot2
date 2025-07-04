
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services.gamification_service import GamificationService
from utils.keyboards import get_mission_keyboard
from states.user_states import SelectingMission, PlayingMinigame

router = Router()
gamification_service = GamificationService()

@router.message(Command("missions"))
async def show_missions(message: types.Message, state: FSMContext):
    missions = await gamification_service.get_available_missions(message.from_user.id)

    if missions:
        await message.answer("🎯 Estas son tus gloriosas pérdidas de tiempo:", reply_markup=get_mission_keyboard(missions))
        await state.set_state(SelectingMission.selecting)
    else:
        await message.answer("🎯 No tienes misiones disponibles en este momento.")

@router.callback_query(SelectingMission.selecting)
async def select_mission(callback: types.CallbackQuery, state: FSMContext):
    mission_id = int(callback.data.split("_")[1])
    await gamification_service.start_mission(callback.from_user.id, mission_id)

    await callback.message.answer("🎮 Has comenzado una misión. Responde 'jugar' para continuar.")
    await state.set_state(PlayingMinigame.playing)

@router.message(PlayingMinigame.playing)
async def play_minigame(message: types.Message, state: FSMContext):
    if message.text.lower() == "jugar":
        success = await gamification_service.complete_mission(message.from_user.id)

        if success:
            await message.answer("🎁 Misión completada. Has ganado besitos y probablemente algo más inútil.")
        else:
            await message.answer("❌ No pudiste completar la misión. Inténtalo de nuevo.")

        await state.clear()
    else:
        await message.answer("🎮 Escribe 'jugar' para intentar completar la misión.")
