from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.user_service import UserService
from services.backpack_service import BackpackService
from utils.helpers import format_backpack

backpack_router = Router()
user_service = UserService()
backpack_service = BackpackService()

@backpack_router.callback_query(F.data == "open_backpack")
async def view_backpack(callback: CallbackQuery):
    user = await user_service.get_or_create_user(callback.from_user)
    backpack_items = await backpack_service.get_user_backpack(user.telegram_id)

    if not backpack_items:
        await callback.message.edit_text("Tu 👜 colección miserable está vacía.\n\nSigue buscando.")
        return

    formatted_backpack = format_backpack(backpack_items)
    await callback.message.edit_text(f"👜 Tu colección miserable:\n\n{formatted_backpack}")
