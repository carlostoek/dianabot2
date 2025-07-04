
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton(text="👜 Abrir mi colección miserable", callback_data="view_backpack")],
        [InlineKeyboardButton(text="📝 Revisar mis pistas", callback_data="check_clues")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
