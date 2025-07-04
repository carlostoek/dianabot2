from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_daily_mission_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="🎯 Misiones Diarias", callback_data="daily_missions")],
        [InlineKeyboardButton(text="🎁 Reclamar Recompensa Diaria", callback_data="claim_daily")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
