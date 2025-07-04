from sqlalchemy.orm import Session
from models.user import User
from models.mission import Mission, UserMission
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

class MissionService:
    """Servicio para gestión de misiones"""
    
    # Misiones diarias base
    DAILY_MISSIONS = [
        {
            "id": "daily_1",
            "name": "Primeros pasos",
            "description": "Visita 2 secciones diferentes del menú",
            "reward": 50,
            "required_level": 1,
            "type": "exploration",
            "auto_complete": True
        },
        {
            "id": "daily_2",
            "name": "Explorador curioso",
            "description": "Visita 3 secciones diferentes del bot",
            "reward": 100,
            "required_level": 1,
            "type": "exploration",
            "auto_complete": True
        },
        {
            "id": "daily_3",
            "name": "Jugador dedicado",
            "description": "Juega cualquier juego disponible",
            "reward": 150,
            "required_level": 2,
            "type": "gaming",
            "auto_complete": True
        },
        {
            "id": "daily_4",
            "name": "Lector de historias",
            "description": "Lee una escena de la historia",
            "reward": 200,
            "required_level": 2,
            "type": "story",
            "auto_complete": True
        },
        {
            "id": "daily_5",
            "name": "Devoto de Diana",
            "description": "Completa 3 misiones en un día",
            "reward": 300,
            "required_level": 3,
            "type": "achievement",
            "auto_complete": True
        }
    ]
    
    # Misiones especiales (no diarias)
    SPECIAL_MISSIONS = [
        {
            "id": "special_1",
            "name": "Bienvenido a la mansión",
            "description": "Completa tu primera interacción",
            "reward": 100,
            "required_level": 1,
            "type": "welcome",
            "one_time": True
        },
        {
            "id": "special_2",
            "name": "Primer nivel",
            "description": "Alcanza el nivel 2",
            "reward": 250,
            "required_level": 2,
            "type": "progression",
            "one_time": True
        }
    ]
    
    @classmethod
    def get_daily_missions(cls, user_level: int):
        """Obtiene misiones diarias según el nivel del usuario"""
        available_missions = []
        
        for mission in cls.DAILY_MISSIONS:
            if mission["required_level"] <= user_level:
                available_missions.append(mission)
        
        return available_missions
    
    @classmethod
    def get_special_missions(cls, user_level: int):
        """Obtiene misiones especiales disponibles"""
        available_missions = []
        
        for mission in cls.SPECIAL_MISSIONS:
            if mission["required_level"] <= user_level:
                available_missions.append(mission)
        
        return available_missions
    
    @staticmethod
    def get_user_completed_missions_today(db: Session, user: User):
        """Obtiene misiones completadas hoy por el usuario"""
        today = date.today().isoformat()
        
        completed_missions = db.query(UserMission).filter(
            UserMission.user_id == user.id,
            UserMission.completion_date == today,
            UserMission.is_completed == True
        ).all()
        
        return [mission.mission_id for mission in completed_missions]
    
    @staticmethod
    def complete_mission(db: Session, user: User, mission_id: str):
        """Marca una misión como completada"""
        try:
            today = date.today().isoformat()
            
            # Verificar si ya está completada hoy
            existing = db.query(UserMission).filter(
                UserMission.user_id == user.id,
                UserMission.mission_id == mission_id,
                UserMission.completion_date == today
            ).first()
            
            if existing and existing.is_completed:
                return False, "Misión ya completada hoy"
            
            # Buscar la misión en las listas
            mission_data = None
            for mission in MissionService.DAILY_MISSIONS + MissionService.SPECIAL_MISSIONS:
                if mission["id"] == mission_id:
                    mission_data = mission
                    break
            
            if not mission_data:
                return False, "Misión no encontrada"
            
            # Verificar nivel requerido
            if user.level < mission_data["required_level"]:
                return False, f"Nivel {mission_data['required_level']} requerido"
            
            # Crear o actualizar registro de misión
            if existing:
                existing.is_completed = True
                existing.completion_date = today
            else:
                user_mission = UserMission(
                    user_id=user.id,
                    mission_id=mission_id,
                    is_completed=True,
                    completion_date=today
                )
                db.add(user_mission)
            
            # Añadir recompensa
            user.besitos += mission_data["reward"]
            
            db.commit()
            
            logger.info(f"Misión {mission_id} completada por usuario {user.telegram_id}")
            return True, mission_data
            
        except Exception as e:
            logger.error(f"Error al completar misión: {e}")
            db.rollback()
            return False, str(e)
    
    @staticmethod
    def get_mission_progress(db: Session, user: User):
        """Obtiene el progreso de misiones del usuario"""
        today = date.today().isoformat()
        
        # Misiones completadas hoy
        completed_today = MissionService.get_user_completed_missions_today(db, user)
        
        # Misiones disponibles
        daily_missions = MissionService.get_daily_missions(user.level)
        special_missions = MissionService.get_special_missions(user.level)
        
        # Filtrar misiones especiales ya completadas (one_time)
        available_special = []
        for mission in special_missions:
            if mission.get("one_time", False):
                # Verificar si ya fue completada alguna vez
                ever_completed = db.query(UserMission).filter(
                    UserMission.user_id == user.id,
                    UserMission.mission_id == mission["id"],
                    UserMission.is_completed == True
                ).first()
                
                if not ever_completed:
                    available_special.append(mission)
            else:
                available_special.append(mission)
        
        return {
            "daily_missions": daily_missions,
            "special_missions": available_special,
            "completed_today": completed_today,
            "total_completed_today": len(completed_today)
        }
