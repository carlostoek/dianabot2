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
        """Registra un canal"""
        try:
            # DEBUG
            logger.info(f"Argumentos recibidos: {context.args}")

            if not context.args or len(context.args) < 3:
                await update.message.reply_text(
                    "❌ Uso incorrecto\n\n"
                    "📝 **Formato:**\n"
                    "`/register_channel <tipo> <id> <nombre>`\n\n"
                    "📋 **Ejemplos:**\n"
                    "`/register_channel vip -1001234567890 Canal VIP Diana`\n"
                    "`/register_channel free -1001234567891 Canal Gratuito Diana`\n\n"
                    "💡 **Tipos disponibles:** vip, free\n"
                    "💡 **ID del canal:** Debe ser un número (ej: -1001234567890)",
                    parse_mode="Markdown"
                )
                return

            channel_type_str = context.args[0].lower()
            channel_id_str = context.args[1]
            channel_name = " ".join(context.args[2:])

            if channel_type_str not in ["vip", "free"]:
                await update.message.reply_text(
                    f"❌ Tipo inválido: '{channel_type_str}'\n"
                    f"✅ Tipos válidos: vip, free"
                )
                return

            try:
                channel_id = int(channel_id_str)
            except ValueError:
                await update.message.reply_text(
                    f"❌ ID de canal inválido: '{channel_id_str}'\n\n"
                    "📝 **El ID debe ser un número entero**\n"
                    "📋 **Ejemplos válidos:**\n"
                    "• `-1001234567890`\n"
                    "• `-1001111111111`\n"
                    "• `1234567890`\n\n"
                    "💡 **Cómo obtener el ID:**\n"
                    "1. Añade @userinfobot al canal\n"
                    "2. El bot te dará el ID correcto",
                    parse_mode="Markdown"
                )
                return

            if not channel_name.strip():
                await update.message.reply_text("❌ El nombre del canal no puede estar vacío")
                return

            channel_type = ChannelType.VIP if channel_type_str == "vip" else ChannelType.FREE

            logger.info(
                f"Registrando canal: tipo={channel_type_str}, id={channel_id}, nombre='{channel_name}'"
            )

            db = get_db_session()
            try:
                channel = ChannelService.register_channel(db, channel_id, channel_name, channel_type)

                emoji = "💎" if channel_type == ChannelType.VIP else "🆓"
                await update.message.reply_text(
                    f"✅ **Canal Registrado Exitosamente**\n\n"
                    f"{emoji} **{channel_name}**\n"
                    f"📊 ID: `{channel_id}`\n"
                    f"🏷️ Tipo: {channel_type.value.upper()}\n\n"
                    "🎯 Usa /admin para gestionar tarifas y tokens",
                    parse_mode="Markdown"
                )
            finally:
                db.close()

        except ValueError as e:
            logger.error(f"ValueError en register_channel: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")
        except Exception as e:
            logger.error(f"Error en register_channel_command: {e}")
            logger.error(f"Argumentos que causaron el error: {context.args}")
            await update.message.reply_text(
                f"❌ Error interno registrando canal\n"
                f"🔍 Detalles: {str(e)}\n\n"
                "📝 Verifica el formato del comando"
            )

    @staticmethod
    async def test_register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando de prueba para debugging"""
        try:
            await update.message.reply_text(
                "🔍 **Debug Info**\n\n"
                f"📝 Argumentos recibidos: `{context.args}`\n"
                f"📊 Cantidad de argumentos: {len(context.args) if context.args else 0}\n\n"
                "📋 **Formato esperado:**\n"
                "`/register_channel vip -1001234567890 Canal VIP Diana`\n\n"
                "🧪 **Comando de prueba:**\n"
                "`/register_channel vip -1001111111111 Test`",
                parse_mode="Markdown"
            )
        except Exception as e:
            await update.message.reply_text(f"Error en test: {e}")

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
