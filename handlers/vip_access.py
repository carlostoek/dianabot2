from aiogram import Router, F
from aiogram.types import Message
from services.user_service import UserService
from services.vip_service import VIPService

vip_router = Router()
user_service = UserService()
vip_service = VIPService()

@vip_router.message(F.text.startswith("🔑 Canjear "))
async def redeem_vip_token(message: Message):
    user = await user_service.get_or_create_user(message.from_user)
    token = message.text.replace("🔑 Canjear ", "").strip()

    result = await vip_service.redeem_token(user.telegram_id, token)

    if result:
        await message.answer(f"🍿 Acceso VIP concedido. Bienvenido.")
    else:
        await message.answer("Token inválido o expirado.")
