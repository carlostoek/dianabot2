from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import get_db
from services.user_service import UserService
from story.chapter_1 import StoryManager
from utils.lucien_voice import LucienVoice
import logging

logger = logging.getLogger(__name__)

class StoryHandlers:
    """Handlers para el sistema narrativo"""
    
    def __init__(self):
        self.story_manager = StoryManager()
        self.lucien = LucienVoice()
    
    async def story_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menú principal de historias"""
        try:
            query = update.callback_query
            user_data = update.effective_user
            
            db_gen = get_db()
            db = next(db_gen)
            
            try:
                user = UserService.get_user_by_telegram_id(db, user_data.id)
                if not user:
                    await query.edit_message_text("❌ Usuario no encontrado.")
                    return
                
                # Obtener capítulos disponibles
                available_chapters = self.story_manager.get_available_chapters(user.level)
                
                text = self.lucien.story_introduction()
                text += f"\n\n**Capítulos disponibles:**\n"
                
                keyboard = []
                for chapter_id in available_chapters:
                    if chapter_id == "chapter_1":
                        keyboard.append([InlineKeyboardButton(
                            "📖 Capítulo 1: Bienvenida a la Mansión",
                            callback_data=f"story_chapter_{chapter_id}"
                        )])
                
                keyboard.append([InlineKeyboardButton("⬅️ Volver", callback_data="main_menu")])
                
                await query.edit_message_text(
                    text,
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode='Markdown'
                )
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error en story_menu: {e}")
            await query.edit_message_text("❌ Error al cargar historias.")
    
    async def chapter_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para capítulos específicos"""
        try:
            query = update.callback_query
            user_data = update.effective_user
            
            # Extraer chapter_id del callback_data
            chapter_id = query.data.replace("story_chapter_", "")
            
            db_gen = get_db()
            db = next(db_gen)
            
            try:
                user = UserService.get_user_by_telegram_id(db, user_data.id)
                if not user:
                    await query.edit_message_text("❌ Usuario no encontrado.")
                    return
                
                # Obtener primera escena del capítulo
                scene_data = self.story_manager.get_scene(
                    chapter_id, 
                    "entrance", 
                    {"name": user.display_name, "level": user.level}
                )
                
                if not scene_data:
                    await query.edit_message_text("❌ Capítulo no encontrado.")
                    return
                
                # Actualizar progreso de historia del usuario
                UserService.update_story_progress(db, user, f"{chapter_id}_entrance")
                
                # Crear teclado con opciones
                keyboard = []
                for choice in scene_data["choices"]:
                    # Verificar requisitos (simplificado)
                    keyboard.append([
                        InlineKeyboardButton(choice.get("text", "Continuar"),
                                             callback_data="main_menu")
                    ])

                await query.edit_message_text(
                    scene_data.get("text", "..."),
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="Markdown",
                )

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error en chapter_handler: {e}")
            await query.edit_message_text("❌ Error al cargar capítulo.")
