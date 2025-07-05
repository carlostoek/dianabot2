from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS
from utils.validators import is_admin


def admin_only(handler):
    @wraps(handler)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        message = update.effective_message
        if user is None or not is_admin(user.id, ADMINS):
            if message:
                await message.reply_text("\ud83d\uddb1 No tienes permisos para acceder a esta funci\u00f3n.")
            return
        return await handler(update, context, *args, **kwargs)
    return wrapper
