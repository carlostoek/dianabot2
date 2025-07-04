from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_menu():
    keyboard = [
        [InlineKeyboardButton(text="🗂️ Gestionar VIP", callback_data="manage_vip")],
        [InlineKeyboardButton(text="🛠️ Configuraciones", callback_data="edit_configs")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
