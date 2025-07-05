from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.channel_service import ChannelService
from models.channel import ChannelType
from utils.keyboards import admin_keyboards
import logging

logger = logging.getLogger(__name__)

class ChannelHandlers:
    """Handlers para gestión de canales"""

    @staticmethod
    async def channel_management_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler principal para gestión de canales"""
        try:
            query = update.callback_query
            await query.answer()

            if query.data == "admin_channels":
                await ChannelHandlers._show_channel_menu(query)
            elif query.data == "channel_register":
                await ChannelHandlers._show_register_options(query)
            elif query.data == "channel_list":
                await ChannelHandlers._show_channel_list(query)
            elif query.data == "channel_tariffs":
                await ChannelHandlers._show_tariff_management(query)

        except Exception as e:
            logger.error(f"Error en channel_management_handler: {e}")
            await query.edit_message_text("❌ Error procesando gestión de canales.")

    @staticmethod
    async def _show_channel_menu(query):
        """Muestra el menú principal de gestión de canales"""
        db = get_db_session()

        try:
            channels = ChannelService.get_channels(db)

            text = (
                "📢 Gestión de Canales\n\n"
                f"Canales registrados: {len(channels)}\n\n"
                "Selecciona una opción:"
            )

            keyboard = [
                [InlineKeyboardButton("➕ Registrar Canal", callback_data="channel_register")],
                [InlineKeyboardButton("📋 Ver Canales", callback_data="channel_list")],
                [InlineKeyboardButton("💰 Gestionar Tarifas", callback_data="channel_tariffs")],
                [InlineKeyboardButton("🎫 Generar Tokens", callback_data="channel_tokens")],
                [InlineKeyboardButton("◀️ Panel Admin", callback_data="admin_menu")]
            ]

            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        finally:
            db.close()

    # Métodos placeholder para futuras implementaciones
    @staticmethod
    async def _show_register_options(query):
        await query.edit_message_text("🚧 Función en desarrollo", reply_markup=admin_keyboards.back_to_admin_keyboard())

    @staticmethod
    async def _show_channel_list(query):
        await query.edit_message_text("🚧 Función en desarrollo", reply_markup=admin_keyboards.back_to_admin_keyboard())

    @staticmethod
    async def _show_tariff_management(query):
        await query.edit_message_text("🚧 Función en desarrollo", reply_markup=admin_keyboards.back_to_admin_keyboard())
