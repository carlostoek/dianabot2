from datetime import datetime

class MessageFormatter:
    """Clase para formatear mensajes del bot"""
    
    @staticmethod
    def welcome_message(user, is_new_user=False):
        """Formatea el mensaje de bienvenida"""
        name = user.display_name
        
        if is_new_user:
            return (
                f"🎩 **¡Bienvenido a la mansión, {name}!**\n\n"
                f"Soy Lucien, mayordomo de Lady Diana 👑. "
                f"Ella ha expresado gran interés en conocerte.\n\n"
                f"**Tu estado inicial:**\n"
                f"⭐ Nivel: {user.level}\n"
                f"💋 Besitos: {user.besitos}\n\n"
                f"*¿Qué te gustaría hacer?*"
            )
        else:
            return (
                f"🎩 **¡Bienvenido de vuelta, {name}!**\n\n"
                f"**Tu estado actual:**\n"
                f"⭐ Nivel: {user.level}\n"
                f"💋 Besitos: {user.besitos}\n"
                f"📖 Historia: {user.current_story}\n\n"
                f"*¿En qué puedo asistirte hoy?*"
            )
    
    @staticmethod
    def user_profile(user):
        """Formatea el perfil completo del usuario"""
        name = user.display_name
        member_since = user.created_at.strftime('%d/%m/%Y') if user.created_at else "Desconocido"
        
        return (
            f"👤 **Perfil de {name}**\n\n"
            f"🆔 **ID Telegram:** `{user.telegram_id}`\n"
            f"⭐ **Nivel:** {user.level}\n"
            f"💋 **Besitos:** {user.besitos}\n"
            f"📖 **Historia actual:** {user.current_story}\n"
            f"📅 **Miembro desde:** {member_since}\n"
            f"🟢 **Estado:** {'Activo' if user.is_active else 'Inactivo'}"
        )
    
    @staticmethod
    def help_message():
        """Mensaje de ayuda del bot"""
        return (
            f"🎩 **Guía de la Mansión Diana**\n\n"
            f"**Comandos disponibles:**\n"
            f"• `/start` - Iniciar o reiniciar el bot\n"
            f"• `/help` - Mostrar esta ayuda\n\n"
            f"**Navegación:**\n"
            f"🎯 **Misiones** - Completa tareas para ganar besitos\n"
            f"🎮 **Juegos** - Diviértete y gana recompensas\n"
            f"👤 **Perfil** - Ve tu progreso y estadísticas\n\n"
            f"**Sistema de Besitos 💋:**\n"
            f"Los besitos son la moneda de la mansión. "
            f"Úsalos para desbloquear contenido y subir de nivel.\n\n"
            f"*¡Que disfrutes tu estancia en la mansión!*"
        )
    
    @staticmethod
    def error_message():
        """Mensaje de error genérico"""
        return (
            f"🎩 **Disculpe la molestia...**\n\n"
            f"Ha ocurrido un pequeño inconveniente. "
            f"Por favor, intente nuevamente en unos momentos.\n\n"
            f"Si el problema persiste, use /start para reiniciar."
        )
    
    @staticmethod
    def coming_soon():
        """Mensaje para funciones en desarrollo"""
        return (
            f"🎩 **Próximamente...**\n\n"
            f"Esta función está siendo preparada especialmente "
            f"por Lady Diana. Estará disponible muy pronto.\n\n"
            f"*Gracias por su paciencia.*"
        )
        
