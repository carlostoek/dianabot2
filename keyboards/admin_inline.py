
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_menu():
    keyboard = [
        [InlineKeyboardButton(text="🗂️ Gestionar Misiones", callback_data="manage_missions")],
        [InlineKeyboardButton(text="🔑 Gestionar Tokens VIP", callback_data="manage_tokens")],
        [InlineKeyboardButton(text="🛠️ Configuraciones Generales", callback_data="edit_config")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
