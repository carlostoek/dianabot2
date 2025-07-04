from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    """Menú principal del bot"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 Misiones", callback_data="missions")],
        [InlineKeyboardButton("🎮 Juegos", callback_data="games")],
        [InlineKeyboardButton("👤 Perfil", callback_data="profile")],
        [InlineKeyboardButton("📖 Historia", callback_data="story")]
    ])

def back_to_main():
    """Botón para volver al menú principal"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Menú Principal", callback_data="main_menu")]
    ])

def missions_menu():
    """Menú de misiones"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Misiones Diarias", callback_data="daily_missions")],
        [InlineKeyboardButton("🏆 Logros", callback_data="achievements")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="main_menu")]
    ])

def games_menu():
    """Menú de juegos"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 Trivia", callback_data="game_trivia")],
        [InlineKeyboardButton("🗺️ Aventura", callback_data="game_adventure")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="main_menu")]
    ])

def profile_menu():
    """Menú de perfil"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Estadísticas", callback_data="stats")],
        [InlineKeyboardButton("🎨 Personalizar", callback_data="customize")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="main_menu")]
    ])
  
