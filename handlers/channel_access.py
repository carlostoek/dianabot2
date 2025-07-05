from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services.channel_service import ChannelService
from states.user_states import ChannelJoin

router = Router()
channel_service = ChannelService()

@router.message(Command("join"))
async def start_join(message: types.Message, state: FSMContext):
    await message.answer("🔑 Envía tu token de acceso:")
    await state.set_state(ChannelJoin.awaiting_token)

@router.message(ChannelJoin.awaiting_token)
async def process_token(message: types.Message, state: FSMContext):
    token = message.text.strip()
    user_id = message.from_user.id
    success = await channel_service.validate_token(user_id, token)
    if success:
        await message.answer("✅ Token válido. Procesando acceso...")
    else:
        await message.answer("❌ Token inválido o expirado.")
    await state.clear()
