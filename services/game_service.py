from sqlalchemy.orm import Session
from models.user import User
from models.game_session import GameSession
import json
import random
import logging

logger = logging.getLogger(__name__)

class GameService:
    """Servicio para gestión de juegos"""
    
    # Pre