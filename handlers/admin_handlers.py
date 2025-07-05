"""
Handlers para administración del bot - VERSIÓN CORREGIDA FINAL
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.user_service import UserService
from utils.keyboards import admin_keyboards, user_keyboards
from utils.formatters import MessageFormatter
from models.user import User, UserRole
from sqlalchemy import func  # Import necesario para funciones agregadas
from config import ADMINS
import logging
from services.token_service import TokenService

logger = logging.getLogger(__name__)

# IDs de administradores autorizados
ADMIN_IDS = ADMINS


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
            elif query.data == "admin_generate_token":
                await AdminHandlers._start_token_config(query, context)
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
    async def _start_token_config(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE):
        """Inicia el proceso de configuración de un nuevo token."""
        user_id = query.from_user.id
        if not AdminHandlers.is_admin(user_id):
            await query.edit_message_text("❌ No tienes permisos de administrador.")
            return

        context.user_data[user_id] = {
            "state": "WAITING_FOR_TOKEN_NAME"
        }
        await query.edit_message_text(
            "📝 Por favor, ingresa el **nombre** del nuevo token:",
            parse_mode="Markdown"
        )

    @staticmethod
    async def handle_token_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja la entrada del nombre del token."""
        user_id = update.effective_user.id
        if not AdminHandlers.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permisos de administrador.")
            return

        if context.user_data.get(user_id, {}).get("state") == "WAITING_FOR_TOKEN_NAME":
            token_name = update.message.text
            if not token_name:
                await update.message.reply_text("El nombre del token no puede estar vacío. Por favor, inténtalo de nuevo.")
                return

            db = get_db_session()
            try:
                existing_token = TokenService.get_token_by_name(db, token_name)
                if existing_token:
                    await update.message.reply_text(
                        f"Ya existe un token con el nombre '{token_name}'. Por favor, elige otro nombre."
                    )
                    return
            finally:
                db.close()

            context.user_data[user_id]["token_name"] = token_name
            context.user_data[user_id]["state"] = "WAITING_FOR_TOKEN_DURATION"

            keyboard = [
                [InlineKeyboardButton("1 Día", callback_data="token_duration_1")],
                [InlineKeyboardButton("1 Semana", callback_data="token_duration_7")],
                [InlineKeyboardButton("2 Semanas", callback_data="token_duration_14")],
                [InlineKeyboardButton("1 Mes", callback_data="token_duration_30")],
                [InlineKeyboardButton("◀️ Cancelar", callback_data="cancel_token_config")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"Has nombrado el token como **'{token_name}'**. Ahora, selecciona la **duración**:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ Comando inesperado. Usa /admin para empezar.")

    @staticmethod
    async def handle_token_duration_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja la selección de duración del token."""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id
        if not AdminHandlers.is_admin(user_id):
            await query.edit_message_text("❌ No tienes permisos de administrador.")
            return

        if query.data == "cancel_token_config":
            if user_id in context.user_data:
                del context.user_data[user_id]
            await query.edit_message_text(
                "Configuración de token cancelada.",
                reply_markup=admin_keyboards.admin_main_menu(),
                parse_mode="Markdown"
            )
            return

        if context.user_data.get(user_id, {}).get("state") == "WAITING_FOR_TOKEN_DURATION":
            try:
                duration_days = int(query.data.replace("token_duration_", ""))
                context.user_data[user_id]["token_duration"] = duration_days
                context.user_data[user_id]["state"] = "WAITING_FOR_TOKEN_PRICE"

                await query.edit_message_text(
                    f"Duración seleccionada: **{duration_days} días**. Ahora, ingresa el **precio** del token (ej. 10.50):",
                    parse_mode="Markdown"
                )
            except ValueError:
                await query.edit_message_text("❌ Duración inválida. Por favor, selecciona una opción válida.")
        else:
            await query.edit_message_text("❌ Comando inesperado. Usa /admin para empezar.")

    @staticmethod
    async def handle_token_price_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja la entrada del precio del token y guarda el token."""
        user_id = update.effective_user.id
        if not AdminHandlers.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permisos de administrador.")
            return

        if context.user_data.get(user_id, {}).get("state") == "WAITING_FOR_TOKEN_PRICE":
            try:
                token_price = float(update.message.text)
                if token_price < 0:
                    await update.message.reply_text("El precio no puede ser negativo. Por favor, ingresa un precio válido.")
                    return

                token_name = context.user_data[user_id]["token_name"]
                token_duration = context.user_data[user_id]["token_duration"]

                db = get_db_session()
                try:
                    new_token = TokenService.create_token(db, token_name, token_duration, token_price)
                    await update.message.reply_text(
                        f"✅ Token **'{new_token.name}'** creado exitosamente:\n"
                        f"Duración: **{new_token.duration_days} días**\n"
                        f"Precio: **{new_token.price:.2f}**",
                        reply_markup=admin_keyboards.admin_main_menu(),
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    logger.error(f"Error al guardar el token en DB: {e}")
                    await update.message.reply_text(
                        "❌ Error al guardar el token. Por favor, inténtalo de nuevo.",
                        reply_markup=admin_keyboards.admin_main_menu()
                    )
                finally:
                    db.close()

                # Limpiar el estado del usuario
                if user_id in context.user_data:
                    del context.user_data[user_id]

            except ValueError:
                await update.message.reply_text("❌ Precio inválido. Por favor, ingresa un número (ej. 10.50).")
        else:
            await update.message.reply_text("❌ Comando inesperado. Usa /admin para empezar.")

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
            
