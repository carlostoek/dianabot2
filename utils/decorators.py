
from aiogram import types
from config import ADMINS
from utils.validators import is_admin

def admin_only(handler):
    async def wrapper(message: types.Message, *args, **kwargs):
        if not is_admin(message.from_user.id, ADMINS):
            await message.answer("🚫 No tienes permisos para acceder a esta función.")
            return
        return await handler(message, *args, **kwargs)
    return wrapper
