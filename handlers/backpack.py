
from aiogram import Router, types
from aiogram.filters import Command
from services.backpack_service import BackpackService
from utils.messages import backpack_message

router = Router()
backpack_service = BackpackService()

@router.message(Command("backpack"))
async def view_backpack(message: types.Message):
    user_id = message.from_user.id
    backpack = await backpack_service.get_user_backpack(user_id)

    if backpack:
        await message.answer(backpack_message(backpack))
    else:
        await message.answer("👜 Tu colección miserable está vacía.")
