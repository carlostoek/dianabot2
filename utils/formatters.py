from datetime import datetime
from models.user import User


class MessageFormatter:
    """Formateo de mensajes diferenciado por roles"""

    @staticmethod
    def welcome_message_by_role(user: User, is_new_user=False):
        """Mensaje de bienvenida según el rol del usuario"""

        if user.is_admin:
            return MessageFormatter._admin_welcome(user, is_new_user)
        elif user.is_vip:
            return MessageFormatter._vip_welcome(user, is_new_user)
        else:
            return MessageFormatter._free_welcome(user, is_new_user)

    @staticmethod
    def _admin_welcome(user: User, is_new_user):
        """Bienvenida para administradores"""
        return (
            f"👑 **Panel de Administración**\n\n"
            f"Bienvenida, **{user.display_name}**.\n"
            f"Sistema DianaBot operativo y listo.\n\n"
            f"**Estado del sistema:**\n"
            f"⭐ Tu nivel: **{user.level}**\n"
            f"💋 Besitos: **{user.besitos}**\n\n"
            f"*Selecciona una función administrativa:*"
        )

    @staticmethod
    def _vip_welcome(user: User, is_new_user):
        """Bienvenida para usuarios VIP"""
        multiplier_text = f" (x{user.besitos_multiplier})" if user.besitos_multiplier > 1.0 else ""

        return (
            f"💎 **¡Bienvenida de vuelta, VIP!**\n\n"
            f"Hola **{user.display_name}**, tu acceso premium está activo.\n\n"
            f"**Tu estado VIP:**\n"
            f"⭐ Nivel: **{user.level}**\n"
            f"💋 Besitos: **{user.besitos}**{multiplier_text}\n"
            f"👑 Membresía: **VIP Activa**\n\n"
            f"*Accede a tu contenido exclusivo:*"
        )

    @staticmethod
    def _free_welcome(user: User, is_new_user):
        """Bienvenida para usuarios gratuitos"""
        if is_new_user:
            return (
                f"🎩 **¡Bienvenido a la mansión, {user.display_name}!**\n\n"
                f"Soy Lucien, mayordomo de Lady Diana 👑. "
                f"Ella ha expresado interés en conocerte.\n\n"
                f"**Tu estado inicial:**\n"
                f"⭐ Nivel: **{user.level}**\n"
                f"💋 Besitos: **{user.besitos}**\n\n"
                f"💎 *¿Te interesa el acceso VIP para contenido exclusivo?*"
            )
        else:
            return (
                f"🎩 **¡Bienvenido de vuelta, {user.display_name}!**\n\n"
                f"**Tu progreso actual:**\n"
                f"⭐ Nivel: **{user.level}**\n"
                f"💋 Besitos: **{user.besitos}**\n"
                f"📖 Historia: *{user.current_story}*\n\n"
                f"💎 *¡Descubre los beneficios VIP!*"
            )

    @staticmethod
    def user_profile(user: User):
        """Formatea el perfil del usuario"""
        member_since = user.created_at.strftime('%d/%m/%Y') if user.created_at else "Desconocido"

        return (
            f"{user.role_emoji} **Perfil de {user.display_name}**\n\n"
            f"🆔 **ID:** `{user.telegram_id}`\n"
            f"👤 **Rol:** {user.role.value.upper()}\n"
            f"⭐ **Nivel:** {user.level}\n"
            f"💋 **Besitos:** {user.besitos}\n"
            f"📖 **Historia:** {user.current_story}\n"
            f"📅 **Miembro desde:** {member_since}\n"
            f"🟢 **Estado:** {'Activo' if user.is_active else 'Inactivo'}"
        )

    @staticmethod
    def help_message():
        """Mensaje de ayuda genérico"""
        return (
            f"🎩 **Guía de la Mansión Diana**\n\n"
            f"**Comandos disponibles:**\n"
            f"• `/start` - Iniciar el bot\n"
            f"• `/help` - Mostrar ayuda\n\n"
            f"**Navegación:**\n"
            f"Usa los botones para navegar por el sistema.\n\n"
            f"*¡Disfruta tu estancia en la mansión!*"
        )

