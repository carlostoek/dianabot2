
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.keyboards import get_admin_menu
from utils.decorators import admin_only
from states.admin_states import AdminMenu

router = Router()

@router.message(Command("admin"))
@admin_only
async def admin_menu(message: types.Message, state: FSMContext):
    await message.answer("🛠️ Bienvenido al glorioso panel de administración. Trata de no romper nada.", reply_markup=get_admin_menu())
    await state.set_state(AdminMenu.main)
