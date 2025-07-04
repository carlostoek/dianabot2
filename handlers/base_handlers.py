from telegram import Update
from telegram.ext import ContextTypes
from core.database import get_db
from services.user_service import UserService
from utils.keyboards import main_menu, back_to_main, missions_menu, games_menu, profile_menu
from utils.formatters import MessageFormatter
import logging

logger = logging.getLogger(__name__)

class BaseHandlers:
    """Handlers básicos del bot"""
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para el comando /start"""
        try:
            user_data = update.effective_user
            
            # ✅ MANEJO CORRECTO DE get_db()
            db_gen = get_db()
            db = next(db_gen)
            
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
                
                # Enviar mensaje de bienvenida
                welcome_text = MessageFormatter.welcome_message(user, is_new_user)
                
                await update.message.reply_text(
                    welcome_text,
                    reply_markup=main_menu(),
                    parse_mode='Markdown'
                )
                
                logger.info(f"Usuario {user_data.id} {'creado' if is_new_user else 'actualizado'}")
                
            finally:
                # ✅ CERRAR SESIÓN DB
                db.close()
            
        except Exception as e:
            logger.error(f"Error en start handler: {e}")
            await update.message.reply_text(
                MessageFormatter.error_message(),
                parse_mode='Markdown'
            )
    
    @staticmethod
    async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para botones inline"""
        try:
            query = update.callback_query
            await query.answer()
            
            user_data = update.effective_user
            
            # ✅ MANEJO CORRECTO DE get_db()
            db_gen = get_db()
            db = next(db_gen)
            
            try:
                user = UserService.get_user_by_telegram_id(db, user_data.id)
                
                if not user:
                    await query.edit_message_text(
                        "❌ Usuario no encontrado. Use /start para registrarse.",
                        reply_markup=back_to_main()
                    )
                    return
                
                # ✅ RESTO DE LA LÓGICA MANTIENE LA MISMA IMPLEMENTACIÓN...
                if query.data == "main_menu":
                    welcome_