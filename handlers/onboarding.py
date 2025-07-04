from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from services.user_service import UserService
from states.user_states import UserStates
from utils.helpers import get_welcome_message, get_onboarding_keyboard

onboarding_router = Router()
user_service = UserService()

@onboarding_router.callback_query(F.data == "intro_diana")
async def onboarding_callback(callback: CallbackQuery, state: FSMContext):
    user = await user_service.get_or_create_user(callback.from_user)
    await user_service.mark_as_onboarded(user.telegram_id)
    await state.set_state(UserStates.viewing_backpack)
    await callback.message.edit_text(
        "Oh, un usuario más... acompáñame, supongo.\n\n" + get_welcome_message(user.first_name)
    )
