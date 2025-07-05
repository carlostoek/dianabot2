from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from models.user import User
from typing import List, Optional, Dict, Any

class UserKeyboards:
    """Teclados intuitivos optimizados para usuarios no técnicos"""

    def __init__(self):
        # Emojis consistentes para toda la experiencia
        self.EMOJIS = {
            # Navegación principal
            "home": "🏠",
            "back": "◀️",
            "next": "▶️",
            "up": "⬆️",
            "down": "⬇️",
            "refresh": "🔄",
            "close": "❌",
            "menu": "📋",
            # Acciones principales
            "play": "🎮",
            "missions": "🎯",
            "bag": "🎒",
            "gift": "🎁",
            "shop": "🛒",
            "auctions": "🏆",
            "profile": "👤",
            "stats": "📊",
            "help": "❓",
            "settings": "⚙️",
            # Estados y feedback
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "new": "🆕",
            "hot": "🔥",
            "cool": "😎",
            "love": "💕",
            # Recursos del juego
            "besitos": "💋",
            "level": "⭐",
            "xp": "⚡",
            "vip": "👑",
            "time": "⏰",
            "count": "🔢",
            # Juegos y actividades
            "trivia": "🧠",
            "numbers": "🔢",
            "math": "🧮",
            "memory": "🧩",
            "treasure": "💎",
            # Narrativa
            "story": "📖",
            "scroll": "📜",
            "map": "🗺️",
            "key": "🗝️",
            "secret": "🤫",
            # Social
            "friends": "👥",
            "chat": "💬",
            "reaction": "❤️",
            "share": "📤",
            # Admin
            "admin": "🔧",
            "users": "👥",
            "channels": "📢",
            "tokens": "🎫",
            "broadcast": "📤",
            "config": "⚙️",
        }

    def main_menu_keyboard(self, user: User) -> InlineKeyboardMarkup:
        """Menú principal - Diseñado para máxima claridad"""
        buttons = []

        # Primera fila - Actividades principales
        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['missions']} Misiones",
                callback_data="missions",
            ),
            InlineKeyboardButton(
                f"{self.EMOJIS['play']} Juegos",
                callback_data="games"
            ),
        ])

        # Segunda fila - Perfil y Historia
        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['profile']} Perfil",
                callback_data="profile"
            ),
            InlineKeyboardButton(
                f"{self.EMOJIS['story']} Historia",
                callback_data="story"
            ),
        ])

        # Tercera fila - Ayuda
        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['help']} Ayuda",
                callback_data="help"
            ),
        ])

        return InlineKeyboardMarkup(buttons)

    def back_to_main_keyboard(self) -> InlineKeyboardMarkup:
        """Botón para volver al menú principal"""
        return InlineKeyboardMarkup([[
            InlineKeyboardButton(
                f"{self.EMOJIS['home']} Menú Principal",
                callback_data="main_menu"
            )
        ]])

    def missions_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Menú de misiones"""
        buttons = [
            [InlineKeyboardButton(
                f"{self.EMOJIS['time']} Misiones Diarias",
                callback_data="mission_daily"
            )],
            [InlineKeyboardButton(
                f"{self.EMOJIS['back']} Volver",
                callback_data="main_menu"
            )]
        ]
        return InlineKeyboardMarkup(buttons)

    def games_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Menú de juegos"""
        buttons = [
            [InlineKeyboardButton(
                f"{self.EMOJIS['trivia']} Trivia",
                callback_data="game_trivia"
            )],
            [InlineKeyboardButton(
                f"{self.EMOJIS['treasure']} Ruleta",
                callback_data="game_roulette"
            )],
            [InlineKeyboardButton(
                f"{self.EMOJIS['back']} Volver",
                callback_data="main_menu"
            )]
        ]
        return InlineKeyboardMarkup(buttons)

class AdminKeyboards:
    """Teclados para administradores"""

    def __init__(self):
        self.EMOJIS = {
            "admin": "🔧",
            "users": "👥",
            "channels": "📢",
            "tokens": "🎫",
            "stats": "📊",
            "broadcast": "📤",
            "config": "⚙️",
            "back": "◀️",
            "home": "🏠",
        }

    def admin_main_menu(self) -> InlineKeyboardMarkup:
        """Menú principal de administrador"""
        buttons = [
            [
                InlineKeyboardButton(
                    f"{self.EMOJIS['users']} Gestión de Usuarios",
                    callback_data="admin_users"
                ),
                InlineKeyboardButton(
                    f"{self.EMOJIS['channels']} Gestión de Canales",
                    callback_data="admin_channels"
                ),
            ],
            [
                InlineKeyboardButton(
                    f"{self.EMOJIS['tokens']} Gestión de Tokens",
                    callback_data="admin_tokens"
                ),
                InlineKeyboardButton(
                    f"{self.EMOJIS['stats']} Estadísticas",
                    callback_data="admin_stats"
                ),
            ],
            [
                InlineKeyboardButton(
                    f"{self.EMOJIS['broadcast']} Broadcast",
                    callback_data="admin_broadcast"
                ),
                InlineKeyboardButton(
                    f"{self.EMOJIS['config']} Configuración",
                    callback_data="admin_config"
                ),
            ],
            [
                InlineKeyboardButton(
                    f"{self.EMOJIS['home']} Menú Usuario",
                    callback_data="main_menu"
                )
            ]
        ]
        return InlineKeyboardMarkup(buttons)

    def back_to_admin_keyboard(self) -> InlineKeyboardMarkup:
        """Botón para volver al menú admin"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f"{self.EMOJIS['back']} Panel Admin",
                    callback_data="admin_menu",
                )
            ]
        ])

    def tokens_menu(self) -> InlineKeyboardMarkup:
        buttons = [
            [InlineKeyboardButton("⚙️ Configurar Tarifas", callback_data="token_tariffs")],
            [InlineKeyboardButton("🔗 Generar Token", callback_data="token_generate")],
            [InlineKeyboardButton(f"{self.EMOJIS['back']} Volver", callback_data="admin_menu")],
        ]
        return InlineKeyboardMarkup(buttons)

    def tariff_duration_keyboard(self) -> InlineKeyboardMarkup:
        buttons = [
            [InlineKeyboardButton("1 día", callback_data="tariff_days_1"), InlineKeyboardButton("7 días", callback_data="tariff_days_7")],
            [InlineKeyboardButton("15 días", callback_data="tariff_days_15"), InlineKeyboardButton("30 días", callback_data="tariff_days_30")],
        ]
        return InlineKeyboardMarkup(buttons)

    def tariffs_list_keyboard(self, tariffs) -> InlineKeyboardMarkup:
        rows = []
        for t in tariffs:
            rows.append([InlineKeyboardButton(t.name, callback_data=f"gen_tariff_{t.id}")])
        rows.append([InlineKeyboardButton(f"{self.EMOJIS['back']} Volver", callback_data="admin_tokens")])
        return InlineKeyboardMarkup(rows)

# Instancias globales para compatibilidad
user_keyboards = UserKeyboards()
admin_keyboards = AdminKeyboards()

# Funciones de compatibilidad con el código existente
def main_menu():
    """Función de compatibilidad"""
    class DummyUser:
        def __init__(self):
            self.level = 1
            self.besitos = 100

    dummy_user = DummyUser()
    return user_keyboards.main_menu_keyboard(dummy_user)

def back_to_main():
    """Función de compatibilidad"""
    return user_keyboards.back_to_main_keyboard()

def missions_menu():
    """Función de compatibilidad"""
    return user_keyboards.missions_menu_keyboard()

def games_menu():
    """Función de compatibilidad"""
    return user_keyboards.games_menu_keyboard()

def get_admin_menu():
    """Función que faltaba para admin"""
    return admin_keyboards.admin_main_menu()

def profile_menu():
    """Menú de perfil"""
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("📊 Estadísticas", callback_data="stats"),
        InlineKeyboardButton("🎨 Personalizar", callback_data="customize")
    ], [
        InlineKeyboardButton("◀️ Volver", callback_data="main_menu")
    ]])

# Aliases y utilidades para compatibilidad con código antiguo
def get_main_menu():
    """Alias para obtener el menú principal"""
    return main_menu()

def get_mission_keyboard(missions: List[Any]) -> InlineKeyboardMarkup:
    """Genera un teclado para seleccionar misiones"""
    buttons = []
    for m in missions:
        title = getattr(m, "title", str(m))
        mission_id = getattr(m, "id", 0)
        buttons.append([InlineKeyboardButton(title, callback_data=f"mission_{mission_id}")])
    if not buttons:
        buttons.append([InlineKeyboardButton("❌ Sin misiones", callback_data="main_menu")])
    buttons.append([InlineKeyboardButton("◀️ Volver", callback_data="main_menu")])
    return InlineKeyboardMarkup(buttons)

