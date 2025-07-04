
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services.vip_service import VIPService
from states.user_states import VIPValidation

router = Router()
vip_service = VIPService()

@router.message(Command("vip"))
async def start_vip_validation(message: types.Message, state: FSMContext):
    await message.answer("🔑 Por favor, ingresa tu token VIP:")
    await state.set_state(VIPValidation.awaiting_token)

@router.message(VIPValidation.awaiting_token)
async def validate_vip_token(message: types.Message, state: FSMContext):
    token = message.text.strip()
    user_id = message.from_user.id

    success = await vip_service.validate_vip_token(user_id, token)

    if success:
        await message.answer("🍿 ¡Acceso VIP concedido!")
    else:
        await message.answer("❌ Token inválido o expirado.")

    await state.clear()
