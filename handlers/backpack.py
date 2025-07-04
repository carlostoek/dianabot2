from aiogram import Router, F
from aiogram.types import Message
from services.user_service import UserService
from services.backpack_service import BackpackService
from utils.helpers import format_backpack

backpack_router = Router()
user_service = UserService()
backpack_service = BackpackService()

@backpack_router.message(F.text == "👜 Abrir mi colección miserable")
async def view_backpack(message: Message):
    user = await user_service.get_or_create_user(message.from_user)
    backpack_items = await backpack_service.get_user_backpack(user.telegram_id)

    if not backpack_items:
        await message.answer("Tu 👜 colección miserable está vacía.\n\nSigue buscando.")
        return

    formatted_backpack = format_backpack(backpack_items)
    await message.answer(f"👜 Tu colección miserable:\n\n{formatted_backpack}")
