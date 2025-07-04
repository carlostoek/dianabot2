from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import get_db
from services.mission_service import MissionService
from services.user_service import UserService
from services.progression import ProgressionService, LevelSystem
from utils.lucien_voice import LucienVoice
from utils.formatters import MessageFormatter
from datetime import date
import logging

logger = logging.getLogger(__name__)

class MissionHandlers:
    """Handlers completos para la gestión de misiones"""
    
    def __init__(self):
        self.lucien = LucienVoice()
    
    @staticmethod
    async def mission_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler principal para misiones"""
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
                if query.data == "missions":
                    await MissionHandlers._show_mission_menu(query, db, user)
                elif query.data == "mission_daily":
                    await MissionHandlers._show_daily_missions(query, db, user)
                elif query.data == "mission_special":
                    await MissionHandlers._show_special_missions(query, db, user)
                elif query.data.startswith("mission_complete_"):
                    mission_id = query.data.replace("mission_complete_", "")
                    await MissionHandlers._complete_mission(query, db, user, mission_id)
                elif query.data == "mission_progress":
                    await MissionHandlers._show_mission_progress(query, db, user)
                else:
                    await query.edit_message_text("❓ Acción no reconocida")
                    
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error en mission_handler: {e}")
            await query.edit_message_text("❌ Error procesando misión")
    
    @staticmethod
    async def _show_mission_menu(query, db, user):
        """Muestra el menú principal de misiones"""
        lucien = LucienVoice()
        
        # Obtener progreso de misiones
        progress = MissionService.get_mission_progress(db, user)
        completed_today = progress["total_completed_today"]
        
        text = lucien.mission_introduction()
        text += f"\n\n**Tu progreso hoy:**\n"
        text += f"✅ Misiones completadas: **{completed_today}**\n"
        text += f"⭐ Nivel actual: **{user.level}**\n"
        text += f"💋 Besitos: **{user.besitos}**\n\n"
        text += "*¿Qué tipo de misiones te interesan?*"
        
        keyboard = [
            [InlineKeyboardButton("📅 Misiones Diarias", callback_data="mission_daily")],
            [InlineKeyboardButton("⭐ Misiones Especiales", callback_data="mission_special")],
            [InlineKeyboardButton("📊 Mi Progreso", callback_data="mission_progress")],
            [InlineKeyboardButton("⬅️ Volver", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def _show_daily_missions(query, db, user):
        """Muestra las misiones diarias disponibles"""
        lucien = LucienVoice()
        
        # Obtener misiones diarias
        daily_missions = MissionService.get_daily_missions(user.level)
        completed_today = MissionService.get_user_completed_missions_today(db, user)
        
        text = f"{lucien.EMOJIS['lucien']} **Misiones Diarias**\n\n"
        text += f"*Estas misiones se renuevan cada día a medianoche.*\n\n"
        
        keyboard = []
        
        if not daily_missions:
            text += "📭 No hay misiones diarias disponibles para tu nivel."
        else:
            for mission in daily_missions:
                status = "✅" if mission["id"] in completed_today else "⏳"
                reward_text = f"{mission['reward']} besitos"
                
                text += f"{status} **{mission['name']}**\n"
                text += f"   📝 {mission['description']}\n"
                text += f"   💋 Recompensa: {reward_text}\n"
                text += f"   📊 Nivel requerido: {mission['required_level']}\n\n"
                
                # Solo mostrar botón si no está completada
                if mission["id"] not in completed_today:
                    keyboard.append([InlineKeyboardButton(
                        f"🎯 {mission['name']}",
                        callback_data=f"mission_complete_{mission['id']}"
                    )])
        
        keyboard.append([InlineKeyboardButton("⬅️ Volver a Misiones", callback_data="missions")])
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def _show_special_missions(query, db, user):
        """Muestra las misiones especiales disponibles"""
        lucien = LucienVoice()
        
        # Obtener misiones especiales
        special_missions = MissionService.get_special_missions(user.level)
        
        text = f"{lucien.EMOJIS['lucien']} **Misiones Especiales**\n\n"
        text += f"*Estas son misiones únicas con recompensas extraordinarias.*\n\n"
        
        keyboard = []
        
        if not special_missions:
            text += "📭 No hay misiones especiales disponibles para tu nivel."
        else:
            for mission in special_missions:
                # Verificar si ya fue completada (para misiones one_time)
                if mission.get("one_time", False):
                    from models.mission import UserMission
                    completed = db.query(UserMission).filter(
                        UserMission.user_id == user.id,
                        UserMission.mission_id == mission["id"],
                        UserMission.is_completed == True
                    ).first()
                    
                    if completed:
                        continue  # No mostrar misiones ya completadas
                
                reward_text = f"{mission['reward']} besitos"
                
                text += f"⭐ **{mission['name']}**\n"
                text += f"   📝 {mission['description']}\n"
                text += f"   💋 Recompensa: {reward_text}\n"
                text += f"   📊 Nivel requerido: {mission['required_level']}\n"
                
                if mission.get("one_time", False):
                    text += f"   🔒 Misión única\n"
                
                text += "\n"
                
                keyboard.append([InlineKeyboardButton(
                    f"⭐ {mission['name']}",
                    callback_data=f"mission_complete_{mission['id']}"
                )])
        
        keyboard.append([InlineKeyboardButton("⬅️ Volver a Misiones", callback_data="missions")])
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def _complete_mission(query, db, user, mission_id):
        """Completa una misión específica"""
        lucien = LucienVoice()
        
        # Intentar completar la misión
        success, result = MissionService.complete_mission(db, user, mission_id)
        
        if success:
            mission_data = result
            old_besitos = user.besitos - mission_data["reward"]
            
            # Verificar subida de nivel
            level_result = LevelSystem.check_level_up(db, user, old_besitos)
            
            text = lucien.mission_completed(mission_data["name"], mission_data["reward"])
            
            if level_result.get("leveled_up", False):
                text += f"\n\n🎉 **¡SUBISTE DE NIVEL!**\n"
                text += f"Nuevo nivel: **{level_result['new_level']}** ⭐\n"
                
                if level_result.get("bonus_besitos", 0) > 0:
                    text += f"Bonus de nivel: **{level_result['bonus_besitos']} besitos** 💋\n"
                
                if level_result.get("unlocks"):
                    text += f"Desbloqueado: *{', '.join(level_result['unlocks'])}*\n"
            
            # Actualizar progreso de usuario
            db.refresh(user)
            text += f"\n💋 Besitos totales: **{user.besitos}**"
            
        else:
            text = f"{lucien.EMOJIS['lucien']} **No se pudo completar la misión**\n\n"
            text += f"❌ {result}"
        
        keyboard = [
            [InlineKeyboardButton("🎯 Ver más misiones", callback_data="missions")],
            [InlineKeyboardButton("🏠 Menú principal", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    @staticmethod
    async def _show_mission_progress(query, db, user):
        """Muestra el progreso detallado de misiones del usuario"""
        lucien = LucienVoice()
        
        # Obtener estadísticas
        stats = ProgressionService.get_user_stats(db, user)
        progress = MissionService.get_mission_progress(db, user)
        level_info = LevelSystem.get_level_progress(user.total_besitos_earned)
        
        text = f"{lucien.EMOJIS['lucien']} **Tu Progreso en Misiones**\n\n"
        
        # Estadísticas generales
        text += f"👤 **{user.display_name}**\n"
        text += f"⭐ Nivel: **{user.level}**\n"
        text += f"💋 Besitos: **{user.besitos}**\n"
        text += f"🎯 Misiones completadas: **{stats.get('missions_completed', 0)}**\n"
        text += f"📅 Completadas hoy: **{progress['total_completed_today']}**\n\n"
        
        # Progreso de nivel
        if not level_info["is_max_level"]:
            progress_bar = "▓" * int(level_info["progress_percentage"] / 10) + "░" * (10 - int(level_info["progress_percentage"] / 10))
            text += f"**Progreso al siguiente nivel:**\n"
            text += f"[{progress_bar}] {level_info['progress_percentage']:.1f}%\n"
            text += f"Faltan: **{level_info['xp_to_next']} besitos**\n\n"
        else:
            text += f"🏆 **¡Nivel máximo alcanzado!**\n\n"
        
        # Misiones disponibles
        daily_available = len([m for m in progress["daily_missions"] if m["id"] not in progress["completed_today"]])
        special_available = len(progress["special_missions"])
        
        text += f"**Misiones disponibles:**\n"
        text += f"📅 Diarias: **{daily_available}**\n"
        text += f"⭐ Especiales: **{special_available}**\n"
        
        keyboard = [
            [InlineKeyboardButton("📅 Misiones Diarias", callback_data="mission_daily")],
            [InlineKeyboardButton("⭐ Misiones Especiales", callback_data="mission_special")],
            [InlineKeyboardButton("⬅️ Volver a Misiones", callback_data="missions")]
        ]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
