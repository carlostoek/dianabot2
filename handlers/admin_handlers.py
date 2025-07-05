"""
Handlers para administración del bot
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.user_service import UserService
from services.channel_service import ChannelService
from utils.keyboards import admin_keyboards
from core.config import Config
import logging

logger = logging.getLogger(__name__)

# IDs de administradores autorizados
ADMIN_IDS = [6181290784]  # Añade tu Telegram ID aquí

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
                    "❌ No tienes permisos de administrador.",
                    parse_mode='Markdown'
                )
                return
            
            text = (
                f"🔧 **Panel de Administración**\n\n"
                f"Bienvenido al sistema de gestión de DianaBot.\n"
                f"Selecciona una opción para continuar:"
            )
            
            await update.message.reply_text(
                text,
                reply_markup=admin_keyboards.admin_main_menu(),
                parse_mode='Markdown'
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
            elif query.data == "token_tariffs":
                await AdminHandlers._show_tariffs(query)
            elif query.data == "tariff_add":
                await AdminHandlers._start_add_tariff(query, context)
            elif query.data.startswith("tariff_days_"):
                await AdminHandlers._tariff_set_duration(query, context)
            elif query.data == "token_generate":
                await AdminHandlers._start_token_generation(query, context)
            elif query.data.startswith("gen_tariff_"):
                await AdminHandlers._generate_token(query, context)
            elif query.data == "admin_stats":
                await AdminHandlers._show_stats(query)
            else:
                await query.edit_message_text(
                    f"🚧 **Función en desarrollo**\n\n"
                    f"La función '{query.data}' estará disponible pronto.",
                    reply_markup=admin_keyboards.back_to_admin_keyboard(),
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logger.error(f"Error en admin_handler: {e}")
            await query.edit_message_text("❌ Error procesando acción admin.")
    
    @staticmethod
    async def _show_admin_menu(query):
        """Muestra el menú principal de admin"""
        text = (
            f"🔧 **Panel de Administración**\n\n"
            f"Sistema operativo y funcional.\n"
            f"Selecciona una opción:"
        )
        
        await query.edit_message_text(
            text,
            reply_markup=admin_keyboards.admin_main_menu(),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def _show_users_management(query):
        """Muestra gestión de usuarios"""
        db = get_db_session()
        
        try:
            # Obtener estadísticas básicas de usuarios
            from models.user import User
            total_users = db.query(User).count()
            active_users = db.query(User).filter(User.is_active == True).count()
            
            text = (
                f"👥 **Gestión de Usuarios**\n\n"
                f"📊 **Estadísticas:**\n"
                f"• Total de usuarios: **{total_users}**\n"
                f"• Usuarios activos: **{active_users}**\n\n"
                f"🚧 *Funciones avanzadas en desarrollo*"
            )
            
            await query.edit_message_text(
                text,
                reply_markup=admin_keyboards.back_to_admin_keyboard(),
                parse_mode='Markdown'
            )
            
        finally:
            db.close()

    @staticmethod
    async def _show_channels_management(query):
        """Gestión de canales"""
        db = get_db_session()
        try:
            from models.channel_management import Channel
            total_channels = db.query(Channel).count()

            text = (
                f"📢 **Gestión de Canales**\n\n"
                f"• Canales registrados: **{total_channels}**\n\n"
                f"🚧 *Funciones avanzadas en desarrollo*"
            )

            await query.edit_message_text(
                text,
                reply_markup=admin_keyboards.back_to_admin_keyboard(),
                parse_mode='Markdown',
            )

        finally:
            db.close()

    @staticmethod
    async def _show_tokens_management(query):
        """Menú principal de tokens"""
        db = get_db_session()
        try:
            from models.channel_management import EntryToken
            total_tokens = db.query(EntryToken).count()

            text = (
                f"🎫 **Gestión de Tokens**\n\n"
                f"Tokens generados: **{total_tokens}**\n"
                f"Selecciona una opción:"
            )

            await query.edit_message_text(
                text,
                reply_markup=admin_keyboards.tokens_menu(),
                parse_mode='Markdown',
            )

        finally:
            db.close()

    @staticmethod
    async def _show_tariffs(query):
        db = get_db_session()
        try:
            from models.channel_management import TokenTariff
            tariffs = db.query(TokenTariff).all()
            if tariffs:
                lines = [f"• {t.name}: {t.duration_days} días - {t.cost} besitos" for t in tariffs]
                text = "\n".join(lines)
            else:
                text = "No hay tarifas configuradas."
            await query.edit_message_text(
                f"💲 **Tarifas Disponibles**\n\n{text}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("➕ Nueva Tarifa", callback_data="tariff_add")],
                    [InlineKeyboardButton("◀️ Volver", callback_data="admin_tokens")],
                ]),
                parse_mode='Markdown',
            )
        finally:
            db.close()

    @staticmethod
    async def _start_add_tariff(query, context):
        context.user_data['tariff'] = {}
        await query.edit_message_text(
            "Selecciona la duración para la nueva tarifa:",
            reply_markup=admin_keyboards.tariff_duration_keyboard()
        )

    @staticmethod
    async def _tariff_set_duration(query, context):
        days = int(query.data.split('_')[-1])
        context.user_data.setdefault('tariff', {})['duration'] = days
        context.user_data['awaiting_cost'] = True
        await query.edit_message_text(
            f"Ingresa el costo para {days} días:",
            parse_mode='Markdown'
        )

    @staticmethod
    async def _start_token_generation(query, context):
        service = ChannelService()
        tariffs = await service.get_tariffs()
        if not tariffs:
            await query.edit_message_text(
                "No hay tarifas configuradas.",
                reply_markup=admin_keyboards.back_to_admin_keyboard()
            )
            return
        await query.edit_message_text(
            "Selecciona la tarifa para el token:",
            reply_markup=admin_keyboards.tariffs_list_keyboard(tariffs)
        )

    @staticmethod
    async def _generate_token(query, context):
        tariff_id = int(query.data.split('_')[-1])
        service = ChannelService()
        token = await service.create_token_from_tariff(channel_id=1, tariff_id=tariff_id)
        if not token:
            await query.edit_message_text("Error generando token.", reply_markup=admin_keyboards.back_to_admin_keyboard())
            return
        link = f"https://t.me/{query.message.bot.username}?start={token.token}"
        await query.edit_message_text(
            f"Token generado:\n{link}",
            reply_markup=admin_keyboards.back_to_admin_keyboard(),
            parse_mode='Markdown'
        )

    @staticmethod
    async def admin_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not AdminHandlers.is_admin(user_id):
            return
        if context.user_data.get('awaiting_cost'):
            try:
                cost = int(update.message.text.strip())
            except ValueError:
                await update.message.reply_text("Ingresa un número válido para el costo:")
                return
            context.user_data['tariff']['cost'] = cost
            context.user_data.pop('awaiting_cost')
            context.user_data['awaiting_name'] = True
            await update.message.reply_text("Ingresa un nombre para la tarifa:")
        elif context.user_data.get('awaiting_name'):
            name = update.message.text.strip()
            data = context.user_data.get('tariff', {})
            service = ChannelService()
            await service.create_tariff(name=name, duration_days=data.get('duration',1), cost=data.get('cost',0))
            context.user_data.pop('awaiting_name')
            context.user_data.pop('tariff', None)
            await update.message.reply_text("Tarifa guardada.")
    
    @staticmethod
    async def _show_stats(query):
        """Muestra estadísticas del sistema"""
        db = get_db_session()
        
        try:
            from models.user import User
            from models.game_session import GameSession
            
            # Estadísticas básicas
            total_users = db.query(User).count()
            total_games = db.query(GameSession).count()
            total_besitos = db.query(User).with_entities(
                db.func.sum(User.besitos)
            ).scalar() or 0
            
            text = (
                f"📊 **Estadísticas del Sistema**\n\n"
                f"👥 **Usuarios:**\n"
                f"• Total registrados: **{total_users}**\n\n"
                f"🎮 **Actividad:**\n"
                f"• Partidas jugadas: **{total_games}**\n\n"
                f"💋 **Economía:**\n"
                f"• Besitos en circulación: **{total_besitos:,}**\n\n"
                f"🔄 *Actualizado en tiempo real*"
            )
            
            await query.edit_message_text(
                text,
                reply_markup=admin_keyboards.back_to_admin_keyboard(),
                parse_mode='Markdown'
            )
            
        finally:
            db.close()

