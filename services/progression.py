from sqlalchemy.orm import Session
from models.user import User
from models.game_session import GameSession
import logging
import math

logger = logging.getLogger(__name__)

class LevelSystem:
    """Sistema de niveles y progresión"""
    
    # Experiencia requerida para cada nivel (besitos acumulados)
    XP_LEVELS = [
        0,      # Nivel 1
        500,    # Nivel 2
        1200,   # Nivel 3
        2500,   # Nivel 4
        4500,   # Nivel 5
        7500,   # Nivel 6
        12000,  # Nivel 7
        18000,  # Nivel 8
        26000,  # Nivel 9
        36000,  # Nivel 10
        50000   # Nivel 11+
    ]
    
    # Bonificaciones por nivel
    LEVEL_BONUSES = {
        2: {"besitos": 100, "unlock": "Juegos básicos"},
        3: {"besitos": 200, "unlock": "Misiones especiales"},
        4: {"besitos": 300, "unlock": "Aventuras"},
        5: {"besitos": 500, "unlock": "Trivia avanzada"},
        6: {"besitos": 750, "unlock": "Historias exclusivas"},
        7: {"besitos": 1000, "unlock": "Modo competitivo"},
        8: {"besitos": 1500, "unlock": "Personalización avanzada"},
        9: {"besitos": 2000, "unlock": "Acceso VIP"},
        10: {"besitos": 3000, "unlock": "Secretos de Diana"}
    }
    
    @classmethod
    def calculate_level(cls, total_besitos_earned: int) -> int:
        """Calcula el nivel basado en besitos totales ganados"""
        for level, threshold in enumerate(cls.XP_LEVELS, 1):
            if level == len(cls.XP_LEVELS):
                # Nivel máximo alcanzado, calcular niveles adicionales
                if total_besitos_earned >= threshold:
                    extra_levels = (total_besitos_earned - threshold) // 15000
                    return level + extra_levels
                return level - 1
            
            if level < len(cls.XP_LEVELS) and total_besitos_earned < cls.XP_LEVELS[level]:
                return level
        
        return len(cls.XP_LEVELS)
    
    @classmethod
    def get_level_progress(cls, total_besitos_earned: int) -> dict:
        """Obtiene información detallada del progreso de nivel"""
        current_level = cls.calculate_level(total_besitos_earned)
        
        if current_level >= len(cls.XP_LEVELS):
            # Nivel máximo
            return {
                "current_level": current_level,
                "current_xp": total_besitos_earned,
                "next_level_xp": None,
                "progress_percentage": 100,
                "xp_to_next": 0,
                "is_max_level": True
            }
        
        current_threshold = cls.XP_LEVELS[current_level - 1] if current_level > 1 else 0
        next_threshold = cls.XP_LEVELS[current_level]
        
        xp_in_current_level = total_besitos_earned - current_threshold
        xp_needed_for_level = next_threshold - current_threshold
        progress_percentage = (xp_in_current_level / xp_needed_for_level) * 100
        
        return {
            "current_level": current_level,
            "current_xp": total_besitos_earned,
            "next_level_xp": next_threshold,
            "progress_percentage": min(progress_percentage, 100),
            "xp_to_next": max(0, next_threshold - total_besitos_earned),
            "is_max_level": False
        }
    
    @classmethod
    def check_level_up(cls, db: Session, user: User, old_besitos: int) -> dict:
        """Verifica si el usuario subió de nivel y aplica bonificaciones"""
        try:
            # Calcular nivel anterior y actual
            old_level = cls.calculate_level(old_besitos)
            new_level = cls.calculate_level(user.besitos)
            
            if new_level > old_level:
                # ¡Subida de nivel!
                user.level = new_level
                
                # Aplicar bonificaciones
                total_bonus = 0
                unlocks = []
                
                for level in range(old_level + 1, new_level + 1):
                    if level in cls.LEVEL_BONUSES:
                        bonus_data = cls.LEVEL_BONUSES[level]
                        total_bonus += bonus_data["besitos"]
                        unlocks.append(bonus_data["unlock"])
                
                if total_bonus > 0:
                    user.besitos += total_bonus
                
                db.commit()
                db.refresh(user)
                
                logger.info(f"Usuario {user.telegram_id} subió al nivel {new_level}")
                
                return {
                    "leveled_up": True,
                    "old_level": old_level,
                    "new_level": new_level,
                    "bonus_besitos": total_bonus,
                    "unlocks": unlocks
                }
            
            return {"leveled_up": False}
            
        except Exception as e:
            logger.error(f"Error en check_level_up: {e}")
            db.rollback()
            return {"leveled_up": False, "error": str(e)}

class AchievementSystem:
    """Sistema de logros y achievements"""
    
    ACHIEVEMENTS = {
        "first_steps": {
            "name": "Primeros Pasos",
            "description": "Completa tu primera misión",
            "reward": 100,
            "icon": "👶",
            "condition": "missions_completed >= 1"
        },
        "mission_master": {
            "name": "Maestro de Misiones",
            "description": "Completa 10 misiones",
            "reward": 500,
            "icon": "🎯",
            "condition": "missions_completed >= 10"
        },
        "game_enthusiast": {
            "name": "Entusiasta de Juegos",
            "description": "Juega 5 partidas",
            "reward": 300,
            "icon": "🎮",
            "condition": "games_played >= 5"
        },
        "besitos_collector": {
            "name": "Coleccionista de Besitos",
            "description": "Acumula 1000 besitos",
            "reward": 200,
            "icon": "💋",
            "condition": "total_besitos >= 1000"
        },
        "level_climber": {
            "name": "Escalador de Niveles",
            "description": "Alcanza el nivel 5",
            "reward": 750,
            "icon": "⭐",
            "condition": "level >= 5"
        },
        "daily_devotee": {
            "name": "Devoto Diario",
            "description": "Completa misiones diarias 7 días seguidos",
            "reward": 1000,
            "icon": "📅",
            "condition": "daily_streak >= 7"
        },
        "story_seeker": {
            "name": "Buscador de Historias",
            "description": "Lee 3 historias completas",
            "reward": 400,
            "icon": "📖",
            "condition": "stories_read >= 3"
        },
        "diana_favorite": {
            "name": "Favorito de Diana",
            "description": "Alcanza el nivel 10",
            "reward": 2000,
            "icon": "👑",
            "condition": "level >= 10"
        }
    }
    
    @classmethod
    def check_achievements(cls, db: Session, user: User, user_stats: dict) -> list:
        """Verifica qué logros ha desbloqueado el usuario"""
        unlocked_achievements = []
        
        for achievement_id, achievement in cls.ACHIEVEMENTS.items():
            # Verificar si ya tiene este logro
            # (Aquí necesitarías una tabla de user_achievements)
            
            # Evaluar condición
            condition = achievement["condition"]
            
            # Reemplazar variables en la condición
            for stat_name, stat_value in user_stats.items():
                condition = condition.replace(stat_name, str(stat_value))
            
            try:
                if eval(condition):
                    unlocked_achievements.append({
                        "id": achievement_id,
                        "name": achievement["name"],
                        "description": achievement["description"],
                        "reward": achievement["reward"],
                        "icon": achievement["icon"]
                    })
            except:
                continue
        
        return unlocked_achievements

class ProgressionService:
    """Servicio principal de progresión"""
    
    @staticmethod
    def get_user_stats(db: Session, user: User) -> dict:
        """Obtiene estadísticas completas del usuario"""
        try:
            # Contar misiones completadas
            missions_completed = db.query(UserMission).filter(
                UserMission.user_id == user.id,
                UserMission.is_completed == True
            ).count()
            
            # Contar juegos jugados
            games_played = db.query(GameSession).filter(
                GameSession.user_id == user.id
            ).count()
            
            # Calcular progreso de nivel
            level_progress = LevelSystem.get_level_progress(user.besitos)
            
            return {
                "level": user.level,
                "besitos": user.besitos,
                "total_besitos": user.besitos,  # Aquí deberías trackear besitos totales ganados
                "missions_completed": missions_completed,
                "games_played": games_played,
                "stories_read": 0,  # Implementar cuando tengas sistema de historias
                "daily_streak": 0,  # Implementar sistema de rachas
                "level_progress": level_progress
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de usuario: {e}")
            return {}
    
    @staticmethod
    def award_experience(db: Session, user: User, amount: int, source: str = "unknown") -> dict:
        """Otorga experiencia (besitos) al usuario y verifica subidas de nivel"""
        try:
            old_besitos = user.besitos
            user.besitos += amount
            
            # Verificar subida de nivel
            level_result = LevelSystem.check_level_up(db, user, old_besitos)
            
            logger.info(f"Usuario {user.telegram_id} ganó {amount} besitos de {source}")
            
            return {
                "besitos_gained": amount,
                "new_total": user.besitos,
                "level_up": level_result
            }
            
        except Exception as e:
            logger.error(f"Error otorgando experiencia: {e}")
            db.rollback()
            return {"error": str(e)}
    
    @staticmethod
    def get_leaderboard(db: Session, category: str = "level", limit: int = 10) -> list:
        """Obtiene tabla de líderes"""
        try:
            if category == "level":
                users = db.query(User).filter(User.is_active == True).order_by(
                    User.level.desc(), User.besitos.desc()
                ).limit(limit).all()
            elif category == "besitos":
                users = db.query(User).filter(User.is_active == True).order_by(
                    User.besitos.desc()
                ).limit(limit).all()
            else:
                return []
            
            leaderboard = []
            for i, user in enumerate(users, 1):
                leaderboard.append({
                    "rank": i,
                    "username": user.display_name,
                    "level": user.level,
                    "besitos": user.besitos,
                    "telegram_id": user.telegram_id,
                })
            return leaderboard
        except Exception as e:
            logger.error(f"Error obteniendo leaderboard: {e}")
            return []
