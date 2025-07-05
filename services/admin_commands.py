"""
Comandos especiales de administrador para gestión rápida
"""
from telegram import Update
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.channel_service import ChannelService
from models.channel import ChannelType
import logging

logger = logging.getLogger(__name__)


class AdminCommands:
    """Comandos especiales para administradores"""

    @staticmethod
    async def register_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Comando: /register_channel <tipo> <id> <nombre>
        Ejemplo: /register_channel vip -1001234567890 Canal VIP Diana
        """
        try:
            if not context.args or len(context.args) < 3:
                await update.message.reply_text(
                    "❌ Uso incorrecto\n\n"
                    "📝 **Formato:**\n"
                    "`/register_channel <tipo> <id> <nombre>`\n\n"
                    "📋 **Ejemplos:**\n"
                    "`/register_channel vip -1001234567890 Canal VIP Diana`\n"
                    "`/register_channel free -1001234567891 Canal Gratuito Diana`\n\n"
                    "💡 **Tipos disponibles:** vip, free",
                    parse_mode="Markdown"
                )
                return

            channel_type_str = context.args[0].lower()
            channel_id = int(context.args[1])
            channel_name = " ".join(context.args[2:])

            # Validar tipo
            if channel_type_str not in ['vip', 'free']:
                await update.message.reply_text("❌ Tipo inválido. Usa: vip o free")
                return

            channel_type = ChannelType.VIP if channel_type_str == 'vip' else ChannelType.FREE

            # Registrar canal
            db = get_db_session()
            try:
                channel = ChannelService.register_channel(db, channel_id, channel_name, channel_type)

                emoji = "💎" if channel_type == ChannelType.VIP else "🆓"
                await update.message.reply_text(
                    f"✅ **Canal Registrado Exitosamente**\n\n"
                    f"{emoji} **{channel_name}**\n"
                    f"📊 ID: `{channel_id}`\n"
                    f"🏷️ Tipo: {channel_type.value.upper()}\n\n"
                    f"🎯 Usa /admin para gestionar tarifas y tokens",
                    parse_mode="Markdown"
                )

            finally:
                db.close()

        except ValueError as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        except Exception as e:
            logger.error(f"Error en register_channel_command: {e}")
            await update.message.reply_text("❌ Error interno registrando canal")

    @staticmethod
    async def list_channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando: /list_channels"""
        try:
            db = get_db_session()
            try:
                channels = ChannelService.get_channels(db)

                if not channels:
                    await update.message.reply_text("📋 No hay canales registrados")
                    return

                text = "📋 **Canales Registrados**\n\n"

                for channel in channels:
                    emoji = "💎" if channel.channel_type == ChannelType.VIP else "🆓"
                    status = "🟢" if channel.is_active else "🔴"

                    text += f"{emoji} {status} **{channel.channel_name}**\n"
                    text += f"   📊 ID: `{channel.channel_id}`\n"
                    text += f"   🏷️ Tipo: {channel.channel_type.value.upper()}\n\n"

                await update.message.reply_text(text, parse_mode="Markdown")

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error en list_channels_command: {e}")
            await update.message.reply_text("❌ Error obteniendo canales")
