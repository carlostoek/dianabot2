def get_welcome_message(first_name):
    return f"Bienvenido, {first_name}. Este lugar responde solo a quienes entienden que lo valioso nunca se entrega fácilmente."

def format_backpack(backpack_items):
    return "\n".join([f"🔹 {item.title} ({item.rarity})" for item in backpack_items])

def get_onboarding_keyboard():
    """Return main menu as inline keyboard."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = [
        [InlineKeyboardButton(text="✨ Conocer a Diana", callback_data="intro_diana")],
        [InlineKeyboardButton(text="👜 Abrir mi colección", callback_data="open_backpack")],
        [InlineKeyboardButton(text="🎯 Misiones Diarias", callback_data="daily_missions")],
        [InlineKeyboardButton(text="🎁 Reclamar Recompensa Diaria", callback_data="claim_daily")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def validate_piece_code(code):
    return code.isalnum() and len(code) <= 10
