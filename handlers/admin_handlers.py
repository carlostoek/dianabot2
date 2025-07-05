"""
Handlers para administración del bot - VERSIÓN CORREGIDA FINAL
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from core.database import get_db_session
from services.user_service import UserService
from services.vip_service import VIPService
from utils.keyboards import admin_keyboards, user_keyboards
from utils.formatters import MessageFormatter
from models.user import User, UserRole
from sqlalchemy import func
from config import ADMINS
import logging
from states.admin_states import VipTariff, VipToken

logger = logging.getLogger(__name__)

ADMIN_IDS = ADMINS

class AdminHandlers:
    @staticmethod
    def is_admin(user_id: int) -> bool:
        return user_id in ADMIN_IDS

    @staticmethod
    async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user_id = update.effective_user.id

            if not AdminHandlers.is_admin(user_id):
                await update.message.reply_text(
                    "❌ No tienes permisos de administrador.", parse_mode="Markdown"
                )
                return

            text = (
                "🔧 **Panel de Administración DianaBot**\n\n"
                "Bienvenida al sistema de gestión completo.\n"
                "Desde aquí puedes controlar todos los aspectos del bot.\n\n"
                "**Funciones disponibles:**\n"
                "👥 Gestión de usuarios y roles\n"
                "📢 Administración de canales\n"
                "🎫 Tokens de entrada VIP\n"
                "📊 Estadísticas en tiempo real\n"
                "📤 Envío masivo de mensajes\n"
                "⚙️ Configuración del sistema\n\n"
                "*Selecciona una opción para continuar:*"
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
        try:
            query = update.callback_query
            await query.answer()

            user_id = update.effective_user.id

            if not AdminHandlers.is_admin(user_id):
                await query.edit_message_text("❌ No tienes permisos de administrador.")
                return

            if query.data == "admin_menu":
                await AdminHandlers._show_admin_menu(query)
            elif query.data == "admin_users":
                await AdminHandlers._show_users_management(query)
            elif query.data == "admin_channels":
                await AdminHandlers._show_channels_management(query)
            elif query.data == "admin_tokens":
                await AdminHandlers._show_tokens_management(query)
            elif query.data == "admin_vip_tariffs":
                await AdminHandlers._show_vip_tariffs_management(query)
            elif query.data == "admin_add_tariff":
                await AdminHandlers._add_tariff_start(query, context)
                return ConversationHandler.END # End current conversation if any
            elif query.data.startswith("admin_add_tariff_duration_"):
                duration = int(query.data.split("_")[-1])
                await AdminHandlers._add_tariff_duration(query, context, duration)
                return ConversationHandler.END
            elif query.data == "admin_vip_generate_token":
                await AdminHandlers._generate_token_start(query, context)
                return ConversationHandler.END
            elif query.data.startswith("admin_generate_token_for_tariff_"):
                tariff_id = int(query.data.split("_")[-1])
                await AdminHandlers._generate_token_select_tariff(query, context, tariff_id)
                return ConversationHandler.END
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
                    "🚧 **Función en desarrollo**\n\n"
                    f"La función '{query.data}' estará disponible pronto.\n\n"
                    "*Mientras tanto, puedes usar las otras opciones.*",
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
            "🔧 **Panel de Administración**\n\n"
            "Sistema operativo y funcional.\n"
            "Todas las funciones están disponibles.\n\n"
            "*Selecciona una opción:*"
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
                "👥 **Gestión de Usuarios**\n\n"
                "📊 **Estadísticas generales:**\n"
                f"• Total de usuarios: **{total_users}**\n"
                f"• Usuarios activos: **{active_users}**\n"
                f"• Usuarios VIP: **{vip_users}** 💎\n"
                f"• Administradores: **{admin_users}** 👑\n\n"
                "👤 **Usuarios recientes:**\n"
            )

            for user in recent_users:
                text += f"• {user.role_emoji} {user.display_name} (Nivel {user.level})\n"

            text += "\n🔧 *Funciones avanzadas de gestión en desarrollo*"

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
        """Muestra gestión de canales - AHORA FUNCIONAL"""
        # Importar el nuevo handler
        from handlers.channel_handlers import ChannelHandlers

        # Redirigir al handler específico de canales
        await ChannelHandlers._show_channel_menu(query)

    @staticmethod
    async def _show_tokens_management(query):
        text = "🎫 **Gestión de Tokens VIP**\n\n" \
               "Desde aquí puedes configurar las tarifas para el acceso VIP y generar tokens para tus usuarios.\n\n" \
               "*Selecciona una opción:*"
        await query.edit_message_text(
            text,
            reply_markup=admin_keyboards.tokens_menu(),
            parse_mode="Markdown"
        )

    @staticmethod
    async def _show_vip_tariffs_management(query):
        db = get_db_session()
        try:
            tariffs = await VIPService.get_all_tariffs(db)
            if tariffs:
                text = "💰 **Tarifas VIP Configuradas:**\n\n"
                for t in tariffs:
                    text += f"• **{t.name}**: {t.duration_days} días, {t.cost} 💋\n"
            else:
                text = "❌ No hay tarifas VIP configuradas aún.\n\n"
            text += "\n*Selecciona una opción:*"
            await query.edit_message_text(
                text,
                reply_markup=admin_keyboards.tariffs_list_keyboard(tariffs),
                parse_mode="Markdown"
            )
        finally:
            db.close()

    @staticmethod
    async def _add_tariff_start(query, context):
        await query.edit_message_text(
            "📝 **Nueva Tarifa VIP**\n\n"
            "Por favor, ingresa el *nombre* para esta nueva tarifa (ej. 'Acceso Mensual', 'Pase Semanal'):",
            parse_mode="Markdown",
            reply_markup=admin_keyboards.back_to_tariffs_keyboard()
        )
        context.user_data['new_tariff'] = {}
        return VipTariff.waiting_for_name

    @staticmethod
    async def _add_tariff_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        tariff_name = update.message.text
        context.user_data['new_tariff']['name'] = tariff_name
        await update.message.reply_text(
            f"Has establecido el nombre de la tarifa como: **{tariff_name}**\n\n"
            "Ahora, selecciona la *duración* en días para esta tarifa:",
            parse_mode="Markdown",
            reply_markup=admin_keyboards.tariff_duration_keyboard()
        )
        return VipTariff.waiting_for_duration

    @staticmethod
    async def _add_tariff_duration(query, context, duration: int):
        context.user_data['new_tariff']['duration_days'] = duration
        await query.edit_message_text(
            f"Has establecido la duración de la tarifa como: **{duration} días**\n\n"
            "Finalmente, ingresa el *costo* en besitos (solo números, ej. '1000'):",
            parse_mode="Markdown",
            reply_markup=admin_keyboards.back_to_tariffs_keyboard()
        )
        return VipTariff.waiting_for_cost

    @staticmethod
    async def _add_tariff_cost(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            cost = float(update.message.text)
            if cost <= 0:
                raise ValueError
            context.user_data['new_tariff']['cost'] = cost

            db = get_db_session()
            try:
                tariff_data = context.user_data['new_tariff']
                await VIPService.add_tariff(
                    db,
                    tariff_data['name'],
                    tariff_data['duration_days'],
                    tariff_data['cost']
                )
                await update.message.reply_text(
                    "✅ Tarifa VIP creada exitosamente.",
                    reply_markup=admin_keyboards.back_to_tariffs_keyboard()
                )
            finally:
                db.close()
            return ConversationHandler.END
        except ValueError:
            await update.message.reply_text(
                "❌ Costo inválido. Por favor, ingresa un número positivo para el costo:",
                reply_markup=admin_keyboards.back_to_tariffs_keyboard()
            )
            return VipTariff.waiting_for_cost

    @staticmethod
    async def _generate_token_start(query, context):
        db = get_db_session()
        try:
            tariffs = await VIPService.get_all_tariffs(db)
            if not tariffs:
                await query.edit_message_text(
                    "❌ No hay tarifas VIP configuradas. Por favor, configura una tarifa primero.",
                    reply_markup=admin_keyboards.back_to_vip_tokens_keyboard()
                )
                return ConversationHandler.END

            text = "🔗 **Generar Token VIP**\n\n" \
                   "Selecciona la tarifa para la cual deseas generar un token:"
            await query.edit_message_text(
                text,
                reply_markup=admin_keyboards.tariffs_list_keyboard(tariffs),
                parse_mode="Markdown"
            )
            return VipToken.waiting_for_tariff_selection
        finally:
            db.close()

    @staticmethod
    async def _generate_token_select_tariff(query, context, tariff_id: int):
        db = get_db_session()
        try:
            tariff = await VIPService.get_tariff_by_id(db, tariff_id)
            if not tariff:
                await query.edit_message_text(
                    "❌ Tarifa no encontrada. Por favor, intenta de nuevo.",
                    reply_markup=admin_keyboards.back_to_vip_tokens_keyboard()
                )
                return ConversationHandler.END

            context.user_data['new_token'] = {'tariff_id': tariff_id}
            await query.edit_message_text(
                f"Has seleccionado la tarifa: **{tariff.name}** ({tariff.duration_days} días, {tariff.cost} 💋)\n\n"
                "Ahora, por favor, ingresa el *ID del canal* de Telegram al que este token dará acceso:",
                parse_mode="Markdown",
                reply_markup=admin_keyboards.back_to_vip_tokens_keyboard()
            )
            return VipToken.waiting_for_channel_id
        finally:
            db.close()

    @staticmethod
    async def _generate_token_channel_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            channel_id = int(update.message.text)
            if channel_id == 0: # Telegram channel IDs are usually negative for supergroups/channels
                raise ValueError

            db = get_db_session()
            try:
                tariff_id = context.user_data['new_token']['tariff_id']
                admin_id = update.effective_user.id
                token_link = await VIPService.generate_vip_token(db, tariff_id, channel_id, admin_id)

                await update.message.reply_text(
                    "✅ Token VIP generado exitosamente.\n\n"
                    f"Comparte este enlace con el usuario:\n`{token_link}`",
                    parse_mode="Markdown",
                    reply_markup=admin_keyboards.back_to_vip_tokens_keyboard()
                )
            finally:
                db.close()
            return ConversationHandler.END
        except ValueError:
            await update.message.reply_text(
                "❌ ID de canal inválido. Por favor, ingresa un número válido para el ID del canal:",
                reply_markup=admin_keyboards.back_to_vip_tokens_keyboard()
            )
            return VipToken.waiting_for_channel_id

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
                "📊 **Estadísticas del Sistema**\n\n"
                "👥 **Usuarios:**\n"
                f"• Total registrados: **{total_users}**\n"
                f"• Usuarios VIP: **{vip_count}** 💎\n"
                f"• Usuarios gratuitos: **{free_count}** 🆓\n\n"
                "🎮 **Actividad:**\n"
                f"• Partidas jugadas: **{total_games}**\n\n"
                "💋 **Economía:**\n"
                f"• Besitos en circulación: **{total_besitos:,}**\n"
                f"• Promedio por usuario: **{total_besitos//max(total_users,1):,}**\n\n"
                "🔄 *Actualizado en tiempo real*"
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
        """Muestra menú de envío masivo - SIN MARKDOWN"""
        text = (
            "📤 Envío Masivo de Mensajes\n\n"
            "🚧 Próximamente disponible:\n"
            "• Enviar a todos los usuarios\n"
            "• Enviar solo a usuarios VIP\n"
            "• Enviar a canales específicos\n"
            "• Programar mensajes\n"
            "• Adjuntar botones con recompensas\n"
            "• Preview antes de enviar\n\n"
            "Herramienta poderosa para comunicación."
        )

        await query.edit_message_text(
            text,
            reply_markup=admin_keyboards.back_to_admin_keyboard()
            # ✅ SIN parse_mode
        )

    @staticmethod
    async def _show_config_menu(query):
        """Muestra menú de configuración - SIN MARKDOWN"""
        text = (
            "⚙️ Configuración del Sistema\n\n"
            "🚧 Próximamente disponible:\n"
            "• Configurar multiplicadores VIP\n"
            "• Ajustar recompensas de misiones\n"
            "• Configurar delays de canales\n"
            "• Gestionar precios de tienda\n"
            "• Personalizar mensajes del bot\n"
            "• Configurar auto-expulsiones\n\n"
            "Control total del comportamiento del bot."
        )

        await query.edit_message_text(
            text,
            reply_markup=admin_keyboards.back_to_admin_keyboard()
            # ✅ SIN parse_mode
        )

    @staticmethod
    async def _switch_to_user_view(query):
        """Cambia a vista de usuario - VERSIÓN SIMPLE"""
        db = get_db_session()

        try:
            user = UserService.get_user_by_telegram_id(db, query.from_user.id)
            if user:
                # Mensaje simple sin Markdown problemático
                text = (
                    f"🏠 Vista de Usuario\n\n"
                    f"Hola {user.display_name}!\n"
                    f"Nivel: {user.level}\n"
                    f"Besitos: {user.besitos}\n"
                    f"Rol: {user.role.value}\n\n"
                    f"Selecciona una opción:"
                )

                keyboard = user_keyboards.get_main_menu_by_role(user)

                await query.edit_message_text(text, reply_markup=keyboard)
            else:
                await query.edit_message_text(
                    "❌ Usuario no encontrado. Usa /start",
                    reply_markup=user_keyboards.back_to_main_keyboard(),
                )
        finally:
            db.close()
            
