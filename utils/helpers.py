def get_welcome_message(first_name):
    return f"Bienvenido, {first_name}. Este lugar responde solo a quienes entienden que lo valioso nunca se entrega fácilmente."

def format_backpack(backpack_items):
    return "\n".join([f"🔹 {item.title} ({item.rarity})" for item in backpack_items])

def get_onboarding_keyboard():
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    keyboard = [
        [KeyboardButton(text="👜 Abrir mi colección miserable")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def validate_piece_code(code):
    return code.isalnum() and len(code) <= 10
