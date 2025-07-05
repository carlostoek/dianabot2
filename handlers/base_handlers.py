from telegram import Update
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.user_service import UserService
from utils.keyboards import user_keyboards
from utils.formatters import MessageFormatter
from models.user import UserRole
import logging

logger = logging.getLogger(__name__)

class BaseHandlers:
    """Handlers básicos del bot"""
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para el comando /start - CON ROLES"""
        try:
            user_data = update.effective_user
            db = get_db_session()

            try:
                # Verificar si es usuario nuevo
                existing_user = UserService.get_user_by_telegram_id(db, user_data.id)
                is_new_user = existing_user is None

                # Crear o actualizar usuario
                user = UserService.create_or_update_user(
                    db=db,
                    telegram_id=user_data.id,
                    username=user_data.username,
                    first_name=user_data.first_name
                )

                # ASIGNAR ROL SI ES ADMIN
                if user_data.id in [6181290784]:  # Tu ID de admin
                    user.role = UserRole.ADMIN
                    db.commit()
                    db.refresh(user)

                # Generar mensaje y menú según rol
                welcome_text = MessageFormatter.welcome_message_by_role(user, is_new_user)
                keyboard = user_keyboards.get_main_menu_by_role(user)

                await update.message.reply_text(
                    welcome_text,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )

                logger.info(
                    f"Usuario {user_data.id} ({user.role.value}) {'creado' if is_new_user else 'actualizado'}"
                )

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error en start handler: {e}")
            await update.message.reply_text("❌ Error interno. Intenta de nuevo.")
    
    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para el comando /help"""
        try:
            help_text = MessageFormatter.help_message()
            await update.message.reply_text(help_text, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"❌ Error en help: {e}")
    
    @staticmethod
    async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler básico para botones"""
        try:
            query = update.callback_query
            await query.answer()

            user_data = update.effective_user
            db = get_db_session()

            try:
                user = UserService.get_user_by_telegram_id(db, user_data.id)

                if not user:
                    await query.edit_message_text("❌ Usuario no encontrado. Use /start")
                    return

                logger.info(
                    f"🔘 Botón presionado: {query.data} por usuario {user_data.id} ({user.role.value})"
                )

                # Manejar diferentes callbacks
                if query.data == "main_menu":
                    welcome_text = MessageFormatter.welcome_message_by_role(user, False)
                    keyboard = user_keyboards.get_main_menu_by_role(user)
                    await query.edit_message_text(
                        welcome_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )

                elif query.data == "profile":
                    profile_text = MessageFormatter.user_profile(user)
                    await query.edit_message_text(
                        profile_text,
                        reply_markup=user_keyboards.back_to_main_keyboard(),
                        parse_mode='Markdown'
                    )

                elif query.data in ["missions", "games", "story"]:
                    await query.edit_message_text(
                        f"🎩 **{query.data.title()}**\n\n"
                        f"Esta función estará disponible muy pronto.\n\n"
                        f"*Gracias por su paciencia.*",
                        reply_markup=user_keyboards.back_to_main_keyboard(),
                        parse_mode='Markdown'
                    )

                else:
                    await query.edit_message_text(
                        "❓ Opción no reconocida.",
                        reply_markup=user_keyboards.back_to_main_keyboard()
                    )

            finally:
                db.close()

        except Exception as e:
            logger.error(f"❌ Error en button_handler: {e}")
            try:
                await query.edit_message_text("❌ Error procesando botón.")
            except:
                pass
