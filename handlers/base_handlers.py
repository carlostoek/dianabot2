from telegram import Update
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.user_service import UserService
from utils.keyboards import main_menu, back_to_main
from utils.formatters import MessageFormatter
import logging

logger = logging.getLogger(__name__)

class BaseHandlers:
    """Handlers básicos del bot"""
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para el comando /start"""
        try:
            logger.info(f"📨 Comando /start recibido de {update.effective_user.id}")
            
            user_data = update.effective_user
            
            # Usar sesión directa
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
                
                # Mensaje de bienvenida
                welcome_text = MessageFormatter.welcome_message(user, is_new_user)
                
                await update.message.reply_text(
                    welcome_text,
                    reply_markup=main_menu(),
                    parse_mode='Markdown'
                )
                
                logger.info(f"✅ Usuario {user_data.id} {'creado' if is_new_user else 'actualizado'}")
                
            except Exception as e:
                logger.error(f"❌ Error en base de datos: {e}")
                await update.message.reply_text(
                    "❌ Error interno. Intenta de nuevo en unos momentos.",
                    parse_mode='Markdown'
                )
            finally:
                db.close()
            
        except Exception as e:
            logger.error(f"❌ Error en start handler: {e}")
            await update.message.reply_text(
                "❌ Error procesando comando. Use /start para reiniciar.",
                parse_mode='Markdown'
            )
    
    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para el comando /help"""
        try:
            help_text = MessageFormatter.help_message()
            
            await update.message.reply_text(
                help_text,
                reply_markup=back_to_main(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"❌ Error en help handler: {e}")
            await update.message.reply_text(
                "❌ Error mostrando ayuda.",
                parse_mode='Markdown'
            )
    
    @staticmethod
    async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para botones inline"""
        try:
            query = update.callback_query
            await query.answer()
            
            user_data = update.effective_user
            logger.info(f"🔘 Botón presionado: {query.data} por usuario {user_data.id}")
            
            # Usar sesión directa
            db = get_db_session()
            
            try:
                user = UserService.get_user_by_telegram_id(db, user_data.id)
                
                if not user:
                    await query.edit_message_text(
                        "❌ Usuario no encontrado. Use /start para registrarse.",
                        reply_markup=back_to_main()
                    )
                    return
                
                # Manejar diferentes callbacks
                if query.data == "main_menu":
                    welcome_text = MessageFormatter.welcome_message(user, False)
                    await query.edit_message_text(
                        welcome_text,
                        reply_markup=main_menu(),
                        parse_mode='Markdown'
                    )
                
                elif query.data == "profile":
                    profile_text = MessageFormatter.user_profile(user)
                    await query.edit_message_text(
                        profile_text,
                        reply_markup=back_to_main(),
                        parse_mode='Markdown'
                    )
                
                elif query.data in ["missions", "games", "story"]:
                    await query.edit_message_text(
                        f"🎩 **{query.data.title()}**\n\n"
                        f"Esta función estará disponible muy pronto.\n\n"
                        f"*Gracias por su paciencia.*",
                        reply_markup=back_to_main(),
                        parse_mode='Markdown'
                    )
                
                else:
                    await query.edit_message_text(
                        "❓ Opción no reconocida.",
                        reply_markup=back_to_main()
                    )
                    
            except Exception as e:
                logger.error(f"❌ Error en base de datos del button_handler: {e}")
                await query.edit_message_text(
                    "❌ Error procesando solicitud.",
                    reply_markup=back_to_main()
                )
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"❌ Error en button_handler: {e}")
            try:
                await query.edit_message_text(
                    "❌ Error procesando botón.",
                    reply_markup=back_to_main()
                )
            except:
                pass  # Si falla el edit, no hacer nada más
