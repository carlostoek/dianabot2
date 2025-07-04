"""
Handlers completos para juegos
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.game_service import GameService
from services.user_service import UserService
from utils.lucien_voice import LucienVoice
import logging

logger = logging.getLogger(__name__)


class GameHandlers:
    """Handlers para juegos"""

    @staticmethod
    async def game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler principal para juegos"""
        try:
            query = update.callback_query
            await query.answer()

            user_data = update.effective_user
            db = get_db_session()
            try:
                user = UserService.get_user_by_telegram_id(db, user_data.id)
                if not user:
                    await query.edit_message_text("❌ Usuario no encontrado")
                    return

                if query.data == "games":
                    await GameHandlers._show_game_menu(query, db, user)
                elif query.data == "game_trivia":
                    await GameHandlers._start_trivia(query, db, user)
                elif query.data == "game_roulette":
                    await GameHandlers._play_roulette(query, db, user)
                elif query.data.startswith("trivia_answer_"):
                    parts = query.data.split("_")
                    session_id = int(parts[2])
                    answer = int(parts[3])
                    await GameHandlers._process_trivia_answer(query, db, user, session_id, answer)
                else:
                    await query.edit_message_text("❓ Acción no reconocida")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error en game_handler: {e}")
            await query.edit_message_text("❌ Error procesando juego")

    @staticmethod
    async def _show_game_menu(query, db, user):
        """Muestra el menú de juegos"""
        lucien = LucienVoice()

        games = GameService.get_available_games(user.level)
        stats = GameService.get_user_game_stats(db, user)

        text = lucien.game_introduction()
        text += f"\n\n**Tus estadísticas:**\n"
        text += f"🎮 Juegos jugados: **{stats.get('total_games', 0)}**\n"
        text += f"💋 Besitos ganados: **{stats.get('total_besitos_earned', 0)}**\n"
        text += f"💰 Besitos actuales: **{user.besitos}**\n\n"
        text += "*¿A qué te gustaría jugar?*"

        keyboard = []
        for game in games:
            cost_text = f" (Cuesta {game['cost']} besitos)" if game['cost'] > 0 else " (Gratis)"
            keyboard.append(
                [InlineKeyboardButton(f"{game['name']}{cost_text}", callback_data=f"game_{game['id']}")]
            )

        keyboard.append([InlineKeyboardButton("⬅️ Volver", callback_data="main_menu")])

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    @staticmethod
    async def _start_trivia(query, db, user):
        """Inicia una partida de trivia"""
        result = GameService.start_trivia(db, user)

        if not result.get("success"):
            await query.edit_message_text(f"❌ Error: {result['error']}")
            return

        text = "🧠 **Trivia de la Mansión**\n\n"
        text += f"**Pregunta:**\n{result['question']}\n\n"
        text += f"💋 **Recompensa:** {result['reward']} besitos\n\n"
        text += "*Selecciona tu respuesta:*"

        keyboard = []
        for i, option in enumerate(result["options"]):
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"{chr(65 + i)}) {option}",
                        callback_data=f"trivia_answer_{result['session_id']}_{i}",
                    )
                ]
            )

        keyboard.append([InlineKeyboardButton("🎮 Volver a Juegos", callback_data="games")])

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    @staticmethod
    async def _process_trivia_answer(query, db, user, session_id, answer):
        """Procesa la respuesta de trivia"""
        result = GameService.answer_trivia(db, user, session_id, answer)

        if not result.get("success"):
            await query.edit_message_text(f"❌ Error: {result['error']}")
            return

        text = "🧠 **Resultado de Trivia**\n\n"
        text += f"{result['result']}\n\n"
        text += f"💋 Besitos actuales: **{user.besitos}**"

        keyboard = [[InlineKeyboardButton("🎮 Volver a Juegos", callback_data="games")]]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    @staticmethod
    async def _play_roulette(query, db, user):
        """Juega una partida de ruleta"""
        result = GameService.play_roulette(db, user)

        if not result.get("success"):
            await query.edit_message_text(f"❌ {result['error']}")
            return

        text = "🎰 **Ruleta de Besitos**\n\n"
        text += f"Premio: {result['prize']}\n"
        text += f"Costo: {result['cost']} besitos\n"
        text += f"Ganancia neta: {result['net_gain']} besitos\n"
        text += f"💋 Nuevo saldo: **{result['new_balance']}**"

        keyboard = [[InlineKeyboardButton("🎮 Volver a Juegos", callback_data="games")]]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
