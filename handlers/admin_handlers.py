"""
Handlers para administración del bot - VERSIÓN COMPLETA
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.user_service import UserService
from utils.keyboards import admin_keyboards, user_keyboards
from utils.formatters import MessageFormatter
from models.user import User, UserRole
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)

# IDs de administradores autorizados
ADMIN_IDS = [6181290784]  # Tu Telegram ID


class AdminHandlers:
    """Handlers para funciones de administración"""

    @staticmethod
    def is_admin(user_id: int) -> bool:
        """Verifica si el usuario es administrador"""
        return user_id in ADMIN_IDS

    @staticmethod
    async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /admin para acceder al panel"""
        try:
            user_id = update.effective_user.id

            if not AdminHandlers.is_admin(user_id):
                await update.message.reply_text(
                    "❌ No tienes permisos de administrador.", parse_mode="Markdown"
                )
                return

            text = (
                f"🔧 *Panel de Administración DianaBot*\n\n"
                f"Bienvenida al sistema de gestión completo.\n"
                f"Desde aquí puedes controlar todos los aspectos del bot.\n\n"
                f"*Funciones disponibles:*\n"
                f"👥 Gestión de usuarios y roles\n"
                f"📢 Administración de canales\n"
                f"🎫 Tokens de entrada VIP\n"
                f"📊 Estadísticas en tiempo real\n"
                f"📤 Envío masivo de mensajes\n"
                f"⚙️ Configuración del sistema\n\n"
                f"*Selecciona una opción para continuar:*"
            )

            await update.message.reply_text(
                text,
                reply_markup=admin_keyboards.admin_main_menu(),
                parse_mode="Markdown",
            )

        except Exception as e:
            logger.error(f"Error en admin_command: {e}")
            await update.message.reply_text("❌ Error accediendo al panel admin.")

    @staticmethod
    async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para botones de administración"""
        try:
            query = update.callback_query
            await query.answer()

            user_id = update.effective_user.id

            if not AdminHandlers.is_admin(user_id):
                await query.edit_message_text("❌ No tienes permisos de administrador.")
                return

            # Determinar acción
            if query.data == "admin_menu":
                await AdminHandlers._show_admin_menu(query)
            elif query.data == "admin_users":
                await AdminHandlers._show_users_management(query)
            elif query.data == "admin_channels":
                await AdminHandlers._show_channels_management(query)
            elif query.data == "admin_tokens":
                await AdminHandlers._show_tokens_management(query)
            elif query.data == "admin_stats":
                await AdminHandlers._show_stats(query)
            elif query.data == "admin_broadcast":
                await AdminHandlers._show_broadcast_menu(query)
            elif query.data == "admin_config":
                await AdminHandlers._show_config_menu(query)
            elif query.data == "switch_to_user_view":
                await AdminHandlers._switch_to_user_view(query)
            else:
                await query.edit_message_text(
                    f"🚧 **Función en desarrollo**\n\n"
                    f"La función '{query.data}' estará disponible pronto.\n\n"
                    f"*Mientras tanto, puedes usar las otras opciones.*",
                    reply_markup=admin_keyboards.back_to_admin_keyboard(),
                    parse_mode="Markdown",
                )

        except Exception as e:
            logger.error(f"Error en admin_handler: {e}")
            await query.edit_message_text("❌ Error procesando acción admin.")

    @staticmethod
    async def _show_admin_menu(query):
        """Muestra el menú principal de admin"""
        text = (
            f"🔧 *Panel de Administración*\n\n"
            f"Sistema operativo y funcional.\n"
            f"Todas las funciones están disponibles.\n\n"
            f"*Selecciona una opción:*"
        )

        await query.edit_message_text(
            text, reply_markup=admin_keyboards.admin_main_menu(), parse_mode="Markdown"
        )

    @staticmethod
    async def _show_users_management(query):
        """Muestra gestión de usuarios"""
        db = get_db_session()

        try:
            # Obtener estadísticas de usuarios
            total_users = db.query(User).count()
            active_users = db.query(User).filter(User.is_active == True).count()
            vip_users = db.query(User).filter(User.role == UserRole.VIP).count()
            admin_users = db.query(User).filter(User.role == UserRole.ADMIN).count()

            # Usuarios recientes (últimos 5)
            recent_users = (
                db.query(User).order_by(User.created_at.desc()).limit(5).all()
            )

            text = (
                f"👥 *Gestión de Usuarios*\n\n"
                f"📊 *Estadísticas generales:*\n"
                f"• Total de usuarios: *{total_users}*\n"
                f"• Usuarios activos: *{active_users}*\n"
                f"• Usuarios VIP: *{vip_users}* 💎\n"
                f"• Administradores: *{admin_users}* 👑\n\n"
                f"👤 *Usuarios recientes:*\n"
            )

            for user in recent_users:
                text += (
                    f"• {user.role_emoji} {user.display_name} (Nivel {user.level})\n"
                )

            text += f"\n🔧 *Funciones avanzadas de gestión en desarrollo*"

            keyboard = [
                [InlineKeyboardButton("🔄 Actualizar", callback_data="admin_users")],
                [InlineKeyboardButton("◀️ Panel Admin", callback_data="admin_menu")],
            ]

            await query.edit_message_text(
                text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
            )

        finally:
            db.close()

    @staticmethod
    async def _show_channels_management(query):
        """Muestra gestión de canales"""
        text = (
            f"📢 *Gestión de Canales*\n\n"
            f"🚧 *Próximamente disponible:*\n"
            f"• Registrar canales VIP y gratuitos\n"
            f"• Configurar delays de entrada\n"
            f"• Gestionar auto-expulsiones\n"
            f"• Ver miembros por canal\n"
            f"• Configurar mensajes promocionales\n\n"
            f"*Esta será la función principal para monetización.*"
        )

        await query.edit_message_text(
            text,
            reply_markup=admin_keyboards.back_to_admin_keyboard(),
            parse_mode="Markdown",
        )

    @staticmethod
    async def _show_tokens_management(query):
        """Muestra gestión de tokens"""
        text = (
            f"🎫 *Gestión de Tokens de Entrada*\n\n"
            f"🚧 *Próximamente disponible:*\n"
            f"• Generar tokens VIP personalizados\n"
            f"• Configurar duración de tokens\n"
            f"• Ver tokens activos/expirados\n"
            f"• Revocar tokens específicos\n"
            f"• Estadísticas de uso\n\n"
            f"*Sistema de monetización directa.*"
        )

        await query.edit_message_text(
            text,
            reply_markup=admin_keyboards.back_to_admin_keyboard(),
            parse_mode="Markdown",
        )

    @staticmethod
    async def _show_stats(query):
        """Muestra estadísticas del sistema"""
        db = get_db_session()

        try:
            from models.game_session import GameSession

            # Estadísticas básicas
            total_users = db.query(User).count()
            total_games = db.query(GameSession).count()
            total_besitos = db.query(func.sum(User.besitos)).scalar() or 0

            # Estadísticas por rol
            vip_count = db.query(User).filter(User.role == UserRole.VIP).count()
            free_count = db.query(User).filter(User.role == UserRole.FREE).count()

            text = (
                f"📊 *Estadísticas del Sistema*\n\n"
                f"👥 *Usuarios:*\n"
                f"• Total registrados: *{total_users}*\n"
                f"• Usuarios VIP: *{vip_count}*\n"
                f"• Usuarios gratuitos: *{free_count}*\n\n"
                f"🎮 *Actividad:*\n"
                f"• Partidas jugadas: *{total_games}*\n\n"
                f"💋 *Economía:*\n"
                f"• Besitos en circulación: *{total_besitos:,}*\n"
                f"• Promedio por usuario: *{total_besitos // max(total_users, 1):,}*\n\n"
                f"🔄 _Actualizado en tiempo real_"
            )

            keyboard = [
                [InlineKeyboardButton("🔄 Actualizar", callback_data="admin_stats")],
                [InlineKeyboardButton("◀️ Panel Admin", callback_data="admin_menu")],
            ]

            await query.edit_message_text(
                text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
            )

        finally:
            db.close()

    @staticmethod
    async def _show_broadcast_menu(query):
        """Muestra menú de envío masivo"""
        text = (
            f"📤 *Envío Masivo de Mensajes*\n\n"
            f"🚧 *Próximamente disponible:*\n"
            f"• Enviar a todos los usuarios\n"
            f"• Enviar solo a usuarios VIP\n"
            f"• Enviar a canales específicos\n"
            f"• Programar mensajes\n"
            f"• Adjuntar botones con recompensas\n"
            f"• Preview antes de enviar\n\n"
            f"*Herramienta poderosa para comunicación.*"
        )

        await query.edit_message_text(
            text,
            reply_markup=admin_keyboards.back_to_admin_keyboard(),
            parse_mode="Markdown",
        )

    @staticmethod
    async def _show_config_menu(query):
        """Muestra menú de configuración"""
        text = (
            f"⚙️ *Configuración del Sistema*\n\n"
            f"🚧 *Próximamente disponible:*\n"
            f"• Configurar multiplicadores VIP\n"
            f"• Ajustar recompensas de misiones\n"
            f"• Configurar delays de canales\n"
            f"• Gestionar precios de tienda\n"
            f"• Personalizar mensajes del bot\n"
            f"• Configurar auto-expulsiones\n\n"
            f"*Control total del comportamiento del bot.*"
        )

        await query.edit_message_text(
            text,
            reply_markup=admin_keyboards.back_to_admin_keyboard(),
            parse_mode="Markdown",
        )

    @staticmethod
    async def _switch_to_user_view(query):
        """Cambia a vista de usuario"""
        db = get_db_session()

        try:
            user = UserService.get_user_by_telegram_id(db, query.from_user.id)
            if user:
                welcome_text = MessageFormatter.welcome_message_by_role(user, False)
                keyboard = user_keyboards.get_main_menu_by_role(user)

                await query.edit_message_text(
                    welcome_text, reply_markup=keyboard, parse_mode="Markdown"
                )
        finally:
            db.close()
