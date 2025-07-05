from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from typing import List, Optional, Dict, Any

# AÑADIR IMPORTS FALTANTES
try:
    from models.user import User
except ImportError:  # pragma: no cover - fallback para importación
    class User:  # type: ignore
        def __init__(self):
            self.level = 1
            self.besitos = 100
            self.role = None

class UserKeyboards:
    """Teclados diferenciados por rol de usuario"""

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

    def get_main_menu_by_role(self, user: User) -> InlineKeyboardMarkup:
        """Retorna el menú principal según el rol del usuario"""
        if user.is_admin:
            return self.admin_main_menu()
        elif user.is_vip:
            return self.vip_main_menu(user)
        else:
            return self.free_main_menu(user)

    def admin_main_menu(self) -> InlineKeyboardMarkup:
        """Menú principal para administradores"""
        buttons = [
            [
                InlineKeyboardButton(
                    f"{self.EMOJIS['users']} Gestión de Usuarios",
                    callback_data="admin_users",
                ),
                InlineKeyboardButton(
                    f"{self.EMOJIS['channels']} Gestión de Canales",
                    callback_data="admin_channels",
                ),
            ],
            [
                InlineKeyboardButton(
                    f"{self.EMOJIS['tokens']} Tokens de Entrada",
                    callback_data="admin_tokens",
                ),
                InlineKeyboardButton(
                    f"{self.EMOJIS['stats']} Estadísticas",
                    callback_data="admin_stats",
                ),
            ],
            [
                InlineKeyboardButton(
                    f"{self.EMOJIS['broadcast']} Envío Masivo",
                    callback_data="admin_broadcast",
                ),
                InlineKeyboardButton(
                    f"{self.EMOJIS['config']} Configuración",
                    callback_data="admin_config",
                ),
            ],
            [
                InlineKeyboardButton(
                    f"{self.EMOJIS['play']} Vista de Usuario",
                    callback_data="switch_to_user_view",
                )
            ],
        ]
        return InlineKeyboardMarkup(buttons)

    def vip_main_menu(self, user: User) -> InlineKeyboardMarkup:
        """Menú principal para usuarios VIP"""
        buttons = []

        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['treasure']} Contenido Premium",
                callback_data="vip_premium_content",
            ),
            InlineKeyboardButton(
                f"{self.EMOJIS['auctions']} Subastas VIP",
                callback_data="vip_auctions",
            ),
        ])

        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['missions']} Misiones VIP",
                callback_data="missions",
            ),
            InlineKeyboardButton(
                f"{self.EMOJIS['play']} Juegos VIP",
                callback_data="games",
            ),
        ])

        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['profile']} Mi Perfil VIP",
                callback_data="profile",
            ),
            InlineKeyboardButton(
                f"{self.EMOJIS['gift']} Beneficios VIP",
                callback_data="vip_benefits",
            ),
        ])

        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['story']} Historia Exclusiva",
                callback_data="story",
            ),
            InlineKeyboardButton(
                f"{self.EMOJIS['help']} Soporte VIP",
                callback_data="vip_support",
            ),
        ])

        return InlineKeyboardMarkup(buttons)

    def free_main_menu(self, user: User) -> InlineKeyboardMarkup:
        """Menú principal para usuarios gratuitos"""
        buttons = []

        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['missions']} Misiones",
                callback_data="missions",
            ),
            InlineKeyboardButton(
                f"{self.EMOJIS['play']} Juegos",
                callback_data="games",
            ),
        ])

        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['profile']} Mi Perfil",
                callback_data="profile",
            ),
            InlineKeyboardButton(
                f"{self.EMOJIS['story']} Historia",
                callback_data="story",
            ),
        ])

        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['vip']} ¡Hazte VIP!",
                callback_data="upgrade_to_vip",
            ),
            InlineKeyboardButton(
                f"{self.EMOJIS['hot']} Canal Baby",
                callback_data="join_baby_channel",
            ),
        ])

        buttons.append([
            InlineKeyboardButton(
                f"{self.EMOJIS['shop']} Tienda",
                callback_data="shop",
            ),
            InlineKeyboardButton(
                f"{self.EMOJIS['help']} Ayuda",
                callback_data="help",
            ),
        ])

        return InlineKeyboardMarkup(buttons)

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
def main_menu(user: User):
    """Función de compatibilidad - requiere usuario"""
    return user_keyboards.get_main_menu_by_role(user)

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
def get_main_menu(user: User):
    """Alias para obtener el menú principal"""
    return main_menu(user)

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

