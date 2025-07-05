from telegram import Update
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.user_service import UserService
from services.channel_service import ChannelService
from utils.keyboards import user_keyboards, admin_keyboards, back_to_main
from models.user import UserRole
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
            token_param = context.args[0] if context.args else None
            
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

                # Asignar rol de administrador si corresponde
                if user_data.id in [6181290784]:
                    user.role = UserRole.ADMIN
                    db.commit()
                    db.refresh(user)
                
                if token_param:
                    link = await ChannelService().validate_token(user_data.id, token_param)
                    if link:
                        await update.message.reply_text("✅ Token válido. Procesando acceso...")
                        await update.message.reply_text(link)

                # Mensaje de bienvenida con menú según rol
                welcome_text = MessageFormatter.welcome_message_by_role(user, is_new_user)
                keyboard = user_keyboards.get_main_menu_by_role(user)

                await update.message.reply_text(
                    welcome_text,
                    reply_markup=keyboard,
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
        """Handler básico para botones CON DIAGNÓSTICO"""
        try:
            query = update.callback_query
            await query.answer()

            user_data = update.effective_user

            # Importar aquí para evitar referencias antes de la asignación
            from handlers.admin_handlers import AdminHandlers

            # ✅ LOGGING DETALLADO
            logger.info(
                f"🔘 CALLBACK RECIBIDO: '{query.data}' de usuario {user_data.id}"
            )

            db = get_db_session()

            try:
                user = UserService.get_user_by_telegram_id(db, user_data.id)

                if not user:
                    logger.warning(f"❌ Usuario {user_data.id} no encontrado en BD")
                    await query.edit_message_text("❌ Usuario no encontrado. Use /start")
                    return

                logger.info(
                    f"👤 Usuario encontrado: {user.display_name} (Rol: {user.role.value})"
                )

                # ✅ MANEJAR TODOS LOS CALLBACKS AQUÍ TEMPORALMENTE
                if query.data == "main_menu":
                    logger.info("🏠 Procesando main_menu")
                    welcome_text = MessageFormatter.welcome_message_by_role(user, False)
                    keyboard = user_keyboards.get_main_menu_by_role(user)
                    await query.edit_message_text(
                        welcome_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )

                elif query.data == "profile":
                    logger.info("👤 Procesando profile")
                    profile_text = MessageFormatter.user_profile(user)
                    await query.edit_message_text(
                        profile_text,
                        reply_markup=user_keyboards.back_to_main_keyboard(),
                        parse_mode='Markdown'
                    )

                # ✅ CALLBACKS DE ADMIN - MANEJAR AQUÍ TEMPORALMENTE
                elif query.data.startswith("admin_") or query.data == "switch_to_user_view":
                    logger.info(f"🔧 Procesando callback admin: {query.data}")
                
                    if not AdminHandlers.is_admin(user_data.id):
                        await query.edit_message_text("❌ No tienes permisos de administrador.")
                        return
                
                    if query.data == "admin_users":
                        await AdminHandlers._show_users_management(query)
                    elif query.data == "admin_channels":  # ← AÑADIR
                        await AdminHandlers._show_channels_management(query)
                    elif query.data == "admin_tokens":  # ← AÑADIR
                        await AdminHandlers._show_tokens_management(query)
                    elif query.data == "admin_stats":
                        await AdminHandlers._show_stats(query)
                    elif query.data == "admin_broadcast":  # ← AÑADIR
                        await AdminHandlers._show_broadcast_menu(query)
                    elif query.data == "admin_config":  # ← AÑADIR
                        await AdminHandlers._show_config_menu(query)
                    elif query.data == "admin_menu":
                        await AdminHandlers._show_admin_menu(query)
                    elif query.data == "switch_to_user_view":  # ← MOVER AQUÍ
                        await AdminHandlers._switch_to_user_view(query)
                    else:
                        await query.edit_message_text(
                            "🚧 Función en desarrollo\n\n"
                            f"'{query.data}' estará disponible pronto.",
                            reply_markup=admin_keyboards.back_to_admin_keyboard()
                            # ✅ SIN parse_mode para evitar errores
                        )
        
                elif query.data in ["missions", "games", "story"]:
                        logger.info(f"🎮 Procesando: {query.data}")
                        await query.edit_message_text(
                            f"🎩 **{query.data.title()}**\n\n"
                            f"Esta función estará disponible muy pronto.\n\n"
                            f"*Gracias por su paciencia.*",
                            reply_markup=user_keyboards.back_to_main_keyboard(),
                            parse_mode='Markdown'
                        )


                else:
                    logger.warning(f"❓ Callback no reconocido: {query.data}")
                    await query.edit_message_text(
                        f"❓ Opción no reconocida: `{query.data}`\n\n"
                        f"*Regresando al menú principal...*",
                        reply_markup=user_keyboards.back_to_main_keyboard(),
                        parse_mode='Markdown'
                    )
                    
            finally:
                db.close()

        except Exception as e:
            logger.error(f"❌ ERROR en button_handler: {e}")
            logger.error(
                f"❌ Callback data: {query.data if 'query' in locals() else 'N/A'}"
            )
            try:
                await query.edit_message_text("❌ Error procesando botón.")
            except:  # pragma: no cover - si falla el edit, no hacer nada
                pass

