from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.mission_service import MissionService
from services.user_service import UserService
from utils.lucien_voice import LucienVoice
import logging

logger = logging.getLogger(__name__)


class MissionHandlers:
    """Handlers para el módulo de misiones."""

    @staticmethod
    async def mission_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Router principal para callbacks de misiones."""
        query = update.callback_query
        await query.answer()
        db = get_db_session()
        try:
            user = UserService.get_user_by_telegram_id(db, update.effective_user.id)
            if not user:
                await query.edit_message_text("❌ Usuario no encontrado. Use /start")
                return

            if query.data == "missions":
                await MissionHandlers._show_mission_menu(query, db, user)
            elif query.data == "mission_daily":
                await MissionHandlers._show_daily_missions(query, db, user)
            elif query.data.startswith("mission_complete_"):
                mission_id = query.data.replace("mission_complete_", "")
                await MissionHandlers._complete_mission(query, db, user, mission_id)
            else:
                await query.edit_message_text("❓ Acción no reconocida")
        except Exception as exc:
            logger.error(f"Error en mission_handler: {exc}")
            try:
                await query.edit_message_text("❌ Error procesando solicitud.")
            except Exception:
                pass
        finally:
            db.close()

    @staticmethod
    async def _show_mission_menu(query, db, user):
        """Despliega el menú principal de misiones."""
        try:
            completed = MissionService.get_user_completed_missions_today(db, user)
            lucien = LucienVoice()
            text = lucien.mission_introduction()
            text += (
                f"\n\n{LucienVoice.EMOJIS['completed']} Misiones completadas hoy: **{len(completed)}**\n"
                f"{LucienVoice.EMOJIS['star']} Nivel actual: **{user.level}**\n"
                f"{LucienVoice.EMOJIS['besitos']} Besitos: **{user.besitos}**"
            )

            keyboard = [
                [InlineKeyboardButton("📅 Misiones Diarias", callback_data="mission_daily")],
                [InlineKeyboardButton("🏠 Menú principal", callback_data="main_menu")],
            ]
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )
        except Exception as exc:
            logger.error(f"Error mostrando menú de misiones: {exc}")
            await query.edit_message_text("❌ Error al mostrar misiones.")

    @staticmethod
    async def _show_daily_missions(query, db, user):
        """Lista las misiones diarias disponibles."""
        try:
            missions = MissionService.get_daily_missions(user.level)
            completed = MissionService.get_user_completed_missions_today(db, user)
            lucien = LucienVoice()
            text = lucien.daily_header() + "\n\n"
            keyboard = []

            if not missions:
                text += "📭 No hay misiones diarias disponibles para tu nivel."
            else:
                for mission in missions:
                    status = LucienVoice.EMOJIS['completed'] if mission['id'] in completed else LucienVoice.EMOJIS['pending']
                    text += (
                        f"{status} *{mission['name']}* - {mission['reward']} {LucienVoice.EMOJIS['besitos']}\n"
                        f"   {mission['description']}\n"
                    )
                    if mission['id'] not in completed:
                        keyboard.append([
                            InlineKeyboardButton(
                                f"🎯 Completar: {mission['name']}",
                                callback_data=f"mission_complete_{mission['id']}",
                            )
                        ])
            keyboard.append([InlineKeyboardButton("⬅️ Volver", callback_data="missions")])
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )
        except Exception as exc:
            logger.error(f"Error mostrando misiones diarias: {exc}")
            await query.edit_message_text("❌ Error al mostrar misiones.")

    @staticmethod
    async def _complete_mission(query, db, user, mission_id: str):
        """Marca una misión como completada y otorga la recompensa."""
        try:
            success, result = MissionService.complete_mission(db, user, mission_id)
            lucien = LucienVoice()
            if success:
                text = lucien.mission_completed(result['name'], result['reward'])
                text += f"\n\n{LucienVoice.EMOJIS['besitos']} Total: **{user.besitos}**"
            else:
                text = f"{LucienVoice.EMOJIS['lucien']} {result}"

            keyboard = [
                [InlineKeyboardButton("🎯 Ver más misiones", callback_data="mission_daily")],
                [InlineKeyboardButton("🏠 Menú principal", callback_data="main_menu")],
            ]
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )
        except Exception as exc:
            logger.error(f"Error completando misión {mission_id}: {exc}")
            await query.edit_message_text("❌ No se pudo completar la misión.")

