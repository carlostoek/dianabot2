"""
Sistema de tracking real de misiones
"""
from sqlalchemy.orm import Session
from models.user import User
from models.mission import UserMission
from services.mission_service import MissionService
from services.user_service import UserService
from datetime import date
import logging

logger = logging.getLogger(__name__)

class MissionTracker:
    """Rastrea el progreso real de misiones"""

    @staticmethod
    def track_action(db: Session, user: User, action: str, data: dict = None):
        """Rastrea una acción del usuario y verifica misiones"""
        try:
            completed_missions = []
            data = data or {}

            # Obtener misiones pendientes del usuario
            today = date.today().isoformat()
            completed_today = MissionService.get_user_completed_missions_today(db, user)
            available_missions = MissionService.get_daily_missions(user.level)

            # Verificar cada misión según la acción
            for mission in available_missions:
                if mission["id"] in completed_today:
                    continue  # Ya completada

                if MissionTracker._check_mission_completion(mission, action, data, user, db):
                    # Completar misión automáticamente
                    success, result = MissionService.complete_mission(db, user, mission["id"])
                    if success:
                        completed_missions.append(mission)
                        logger.info(f"Misión auto-completada: {mission['name']} para usuario {user.telegram_id}")

            return completed_missions

        except Exception as e:
            logger.error(f"Error en track_action: {e}")
            return []

    @staticmethod
    def _check_mission_completion(mission: dict, action: str, data: dict, user: User, db: Session) -> bool:
        """Verifica si una misión específica se completó con la acción"""

        mission_id = mission["id"]

        # MISIÓN: Primeros pasos - Explorar menú principal
        if mission_id == "daily_1" and action == "menu_visit":
            sections_visited = data.get("sections_visited", [])
            required_sections = ["missions", "games", "profile"]
            return len(set(sections_visited) & set(required_sections)) >= 2

        # MISIÓN: Explorador curioso - Visitar todas las secciones
        elif mission_id == "daily_2" and action == "menu_visit":
            sections_visited = data.get("sections_visited", [])
            required_sections = ["missions", "games", "profile", "story"]
            return len(set(sections_visited) & set(required_sections)) >= 3

        # MISIÓN: Jugador dedicado - Participar en un juego
        elif mission_id == "daily_3" and action == "game_played":
            return True  # Cualquier juego cuenta

        # MISIÓN: Coleccionista de historias - Leer una historia
        elif mission_id == "daily_4" and action == "story_read":
            return True  # Cualquier historia cuenta

        # MISIÓN: Devoto de Diana - Completar 3 misiones en un día
        elif mission_id == "daily_5":
            completed_today = MissionService.get_user_completed_missions_today(db, user)
            return len(completed_today) >= 2  # Ya tiene 2, esta sería la 3ra

        return False

    @staticmethod
    def get_user_session_data(db: Session, user: User) -> dict:
        """Obtiene datos de sesión del usuario para tracking"""
        # Aquí podrías usar Redis o una tabla temporal
        # Por ahora, usamos un sistema simple basado en la sesión actual
        return {
            "sections_visited": [],
            "games_played": 0,
            "stories_read": 0,
            "session_start": date.today().isoformat()
        }

    @staticmethod
    def update_user_session_data(db: Session, user: User, data: dict):
        """Actualiza datos de sesión del usuario"""
        # Implementación simple - en producción usarías Redis
        pass
