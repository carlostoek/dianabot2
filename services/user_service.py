from sqlalchemy.orm import Session
from models.user import User
from core.config import Config
import logging

logger = logging.getLogger(__name__)

class UserService:
    """Servicio para gestión de usuarios"""
    
    @staticmethod
    def create_or_update_user(db: Session, telegram_id: int, username: str = None, first_name: str = None):
        """Crea un nuevo usuario o actualiza uno existente"""
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                # Crear nuevo usuario
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    besitos=Config.INITIAL_BESITOS,
                    total_besitos_earned=Config.INITIAL_BESITOS
                )
                db.add(user)
                logger.info(f"Nuevo usuario creado: {telegram_id}")
            else:
                # Actualizar usuario existente
                if username and user.username != username:
                    user.username = username
                if first_name and user.first_name != first_name:
                    user.first_name = first_name
                logger.info(f"Usuario actualizado: {telegram_id}")
            
            db.commit()
            db.refresh(user)
            return user
            
        except Exception as e:
            logger.error(f"Error al crear/actualizar usuario {telegram_id}: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def get_user_by_telegram_id(db: Session, telegram_id: int):
        """Obtiene un usuario por su telegram_id"""
        try:
            return db.query(User).filter(User.telegram_id == telegram_id).first()
        except Exception as e:
            logger.error(f"Error al obtener usuario {telegram_id}: {e}")
            return None
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """Obtiene un usuario por su ID interno"""
        try:
            return db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logger.error(f"Error al obtener usuario por ID {user_id}: {e}")
            return None
    
    @staticmethod
    def add_besitos(db: Session, user: User, amount: int, track_total: bool = True):
        """Añade besitos a un usuario"""
        try:
            if amount < 0:
                raise ValueError("La cantidad de besitos no puede ser negativa")
            
            user.besitos += amount
            
            if track_total:
                user.total_besitos_earned += amount
            
            db.commit()
            db.refresh(user)
            
            logger.info(f"Añadidos {amount} besitos al usuario {user.telegram_id}")
            return user
            
        except Exception as e:
            logger.error(f"Error al añadir besitos: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def subtract_besitos(db: Session, user: User, amount: int):
        """Resta besitos a un usuario"""
        try:
            if amount < 0:
                raise ValueError("La cantidad de besitos no puede ser negativa")
            
            if user.besitos < amount:
                raise ValueError("Besitos insuficientes")
            
            user.besitos -= amount
            db.commit()
            db.refresh(user)
            
            logger.info(f"Restados {amount} besitos al usuario {user.telegram_id}")
            return user
            
        except Exception as e:
            logger.error(f"Error al restar besitos: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def update_story_progress(db: Session, user: User, new_story: str):
        """Actualiza el progreso de la historia del usuario"""
        try:
            user.current_story = new_story
            db.commit()
            db.refresh(user)
            logger.info(f"Historia actualizada para usuario {user.telegram_id}: {new_story}")
            return user
        except Exception as e:
            logger.error(f"Error al actualizar historia: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def deactivate_user(db: Session, user: User):
        """Desactiva un usuario"""
        try:
            user.is_active = False
            db.commit()
            db.refresh(user)
            logger.info(f"Usuario {user.telegram_id} desactivado")
            return user
        except Exception as e:
            logger.error(f"Error al desactivar usuario: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def get_active_users_count(db: Session):
        """Obtiene el número de usuarios activos"""
        try:
            return db.query(User).filter(User.is_active == True).count()
        except Exception as e:
            logger.error(f"Error al contar usuarios activos: {e}")
            return 0
            
