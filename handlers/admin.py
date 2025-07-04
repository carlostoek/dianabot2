from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services.admin_service import AdminService
from states.admin_states import AdminStates
from keyboards.admin_inline import get_admin_menu

admin_router = Router()
admin_service = AdminService()

@admin_router.message(F.text == "/admin")
async def open_admin_panel(message: Message, state: FSMContext):
    await message.answer("🛠️ Entrando al glorioso panel de administración. Trata de no romper nada.", reply_markup=get_admin_menu())
    await state.set_state(AdminStates.admin_menu)
