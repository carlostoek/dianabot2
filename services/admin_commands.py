"""
Comandos especiales de administrador para gestión rápida
"""
from telegram import Update
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.channel_service import ChannelService
from models.channel import ChannelType, Channel
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
        db = None
        
        try:
            logger.info(f"Argumentos recibidos: {context.args}")
            
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
            channel_id_str = context.args[1]
            channel_name = " ".join(context.args[2:])
            
            if channel_type_str not in ['vip', 'free']:
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
                    f"📝 **El ID debe ser un número entero**\n"
                    f"📋 **Ejemplos válidos:**\n"
                    f"• `-1001234567890`\n"
                    f"• `-1001111111111`\n\n"
                    f"💡 **Cómo obtener el ID:**\n"
                    f"1. Añade @userinfobot al canal\n"
                    f"2. El bot te dará el ID correcto",
                    parse_mode="Markdown"
                )
                return
            
            if not channel_name.strip():
                await update.message.reply_text("❌ El nombre del canal no puede estar vacío")
                return
            
            channel_type = ChannelType.VIP if channel_type_str == 'vip' else ChannelType.FREE
            
            db = get_db_session()
            logger.info("✅ Sesión de BD creada")
            
            try:
                existing = db.query(Channel).filter(Channel.channel_id == channel_id).first()
                
                if existing:
                    await update.message.reply_text(
                        f"⚠️ **Canal ya registrado**\n\n"
                        f"📊 ID: `{channel_id}`\n"
                        f"📝 Nombre actual: {existing.channel_name}\n"
                        f"🏷️ Tipo actual: {existing.channel_type.value.upper()}\n\n"
                        f"💡 Usa un ID diferente o elimina el canal existente",
                        parse_mode="Markdown"
                    )
                    return
                
                channel = ChannelService.register_channel(db, channel_id, channel_name, channel_type)
                logger.info(f"✅ Canal registrado exitosamente: {channel.id}")
                
                emoji = "💎" if channel_type == ChannelType.VIP else "🆓"
                await update.message.reply_text(
                    f"✅ **Canal Registrado Exitosamente**\n\n"
                    f"{emoji} **{channel_name}**\n"
                    f"📊 ID: `{channel_id}`\n"
                    f"🏷️ Tipo: {channel_type.value.upper()}\n\n"
                    f"🎯 Usa /admin para gestionar tarifas y tokens",
                    parse_mode="Markdown"
                )
                
            except Exception as db_error:
                logger.error(f"Error en operación de BD: {db_error}")
                db.rollback()
                raise
                
        except ValueError as e:
            logger.error(f"ValueError en register_channel: {e}")
            await update.message.reply_text(f"❌ Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"Error en register_channel_command: {e}")
            await update.message.reply_text(
                f"❌ Error interno registrando canal\n"
                f"🔍 Detalles: {str(e)}"
            )
        finally:
            if db:
                try:
                    db.close()
                    logger.info("✅ Sesión de BD cerrada")
                except Exception as close_error:
                    logger.error(f"Error cerrando sesión BD: {close_error}")

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

    @staticmethod
    async def clear_channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando para limpiar todos los canales (solo para debugging)"""
        try:
            db = get_db_session()
            try:
                from models.channel import Channel
                count = db.query(Channel).count()
                db.query(Channel).delete()
                db.commit()
                
                await update.message.reply_text(
                    f"🗑️ **Canales eliminados**\n\n"
                    f"📊 Canales eliminados: {count}\n"
                    f"✅ Base de datos limpia"
                )
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error limpiando canales: {e}")
            await update.message.reply_text(f"❌ Error: {e}")
