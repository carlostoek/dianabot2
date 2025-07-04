from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import get_db
from services.game_service import GameService
from services.user_service import UserService
from services.progression import ProgressionService
from utils.lucien_voice import LucienVoice
from models.game_session import GameSession
import json
import random
import logging

logger = logging.getLogger(__name__)

class GameHandlers:
    """Handlers completos para la gestión de juegos"""
    
    def __init__(self):
        self.lucien = LucienVoice()
    
    @staticmethod
    async def game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler principal para juegos"""
        try:
            query = update.callback_query
            await query.answer()
            
            user_data = update.effective_user
            db_gen = get_db()
            db = next(db_gen)
            
            try:
                user = UserService.get_user_by_telegram_id(db, user_data.id)
                if not user:
                    await query.edit_message_text("❌ Usuario no encontrado. Use /start")
                    return
                
                # Determinar acción según callback_data
                if query.data == "games":
                    await GameHandlers._show_game_menu(query, db, user)
                elif query.data == "game_trivia":
                    await GameHandlers._start_trivia(query, db, user)
                elif query.data == "game_adventure":
                    await GameHandlers._start_adventure(query, db, user)
                elif query.data.startswith("trivia_answer_"):
                    answer = query.data.replace("trivia_answer_", "")
                    await GameHandlers._process_trivia_answer(query, db, user, answer)
                elif query.data.startswith("adventure_choice_"):
                    choice = query.data.replace("adventure_choice_", "")
                    await GameHandlers._process_adventure_choice(query, db, user, choice)
                elif query.data == "game_leaderboard":
                    await GameHandlers._show_leaderboard(query, db, user)
                else:
                    await query.edit_message_text("❓ Acción no reconocida")
                    
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error en game_handler: