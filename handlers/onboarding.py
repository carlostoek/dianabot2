
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from services.user_service import UserService
from utils.keyboards import get_main_menu
from utils.messages import welcome_message
from states.user_states import UserOnboarding

router = Router()
user_service = UserService()

@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    user = await user_service.get_or_create_user(message.from_user)

    if not user.is_onboarded:
        await message.answer(welcome_message(user), reply_markup=get_main_menu())
        await state.set_state(UserOnboarding.onboarding_complete)
        await user_service.set_onboarded(user)
    else:
        await message.answer(f"🍹 Oh, {user.first_name}... ya nos conocemos.", reply_markup=get_main_menu())
