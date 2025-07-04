"""
Servicio completo de juegos
"""
from sqlalchemy.orm import Session
from models.user import User
from models.game_session import GameSession
from services.user_service import UserService
from services.mission_tracker import MissionTracker
import json
import random
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class GameService:
    """Servicio para gestión de juegos"""

    # PREGUNTAS DE TRIVIA
    TRIVIA_QUESTIONS = [
        {
            "id": 1,
            "question": "¿Cuál es el nombre del mayordomo de la mansión?",
            "options": ["Lucien", "Sebastian", "Alfred", "James"],
            "correct": 0,
            "reward": 75,
        },
        {
            "id": 2,
            "question": "¿Cómo se llama la moneda de la mansión?",
            "options": ["Monedas", "Besitos", "Puntos", "Gemas"],
            "correct": 1,
            "reward": 50,
        },
        {
            "id": 3,
            "question": "¿Quién es la dueña de la mansión?",
            "options": ["Lady Ana", "Lady Diana", "Lady Sofia", "Lady Elena"],
            "correct": 1,
            "reward": 100,
        },
        {
            "id": 4,
            "question": "¿Qué necesitas para subir de nivel?",
            "options": ["Tiempo", "Besitos", "Amigos", "Suerte"],
            "correct": 1,
            "reward": 60,
        },
    ]

    # CONFIGURACIÓN DE RULETA
    ROULETTE_PRIZES = [
        {"prize": "10 besitos", "value": 10, "probability": 30},
        {"prize": "25 besitos", "value": 25, "probability": 25},
        {"prize": "50 besitos", "value": 50, "probability": 20},
        {"prize": "100 besitos", "value": 100, "probability": 15},
        {"prize": "200 besitos", "value": 200, "probability": 8},
        {"prize": "¡JACKPOT! 500 besitos", "value": 500, "probability": 2},
    ]

    @staticmethod
    def get_available_games(user_level: int) -> list:
        """Obtiene juegos disponibles según el nivel del usuario"""
        games = [
            {
                "id": "trivia",
                "name": "🧠 Trivia de la Mansión",
                "description": "Responde preguntas sobre la mansión",
                "min_level": 1,
                "cost": 0,
            }
        ]

        if user_level >= 2:
            games.append(
                {
                    "id": "roulette",
                    "name": "🎰 Ruleta de Besitos",
                    "description": "Gira la ruleta y gana premios",
                    "min_level": 2,
                    "cost": 20,
                }
            )

        return [game for game in games if user_level >= game["min_level"]]

    @staticmethod
    def start_trivia(db: Session, user: User) -> dict:
        """Inicia una nueva partida de trivia"""
        try:
            # Seleccionar pregunta aleatoria
            question = random.choice(GameService.TRIVIA_QUESTIONS)

            # Crear sesión de juego
            game_session = GameSession(
                user_id=user.id,
                game_type="trivia",
                current_data=json.dumps(
                    {
                        "question_id": question["id"],
                        "question": question["question"],
                        "options": question["options"],
                        "correct_answer": question["correct"],
                        "reward": question["reward"],
                    }
                ),
            )

            db.add(game_session)
            db.commit()
            db.refresh(game_session)

            # Tracking de misión
            MissionTracker.track_action(db, user, "game_played", {"game_type": "trivia"})

            return {
                "success": True,
                "session_id": game_session.id,
                "question": question["question"],
                "options": question["options"],
                "reward": question["reward"],
            }

        except Exception as e:
            logger.error(f"Error iniciando trivia: {e}")
            db.rollback()
            return {"success": False, "error": str(e)}

    @staticmethod
    def answer_trivia(db: Session, user: User, session_id: int, answer: int) -> dict:
        """Procesa respuesta de trivia"""
        try:
            # Obtener sesión de juego
            session = (
                db.query(GameSession)
                .filter(
                    GameSession.id == session_id,
                    GameSession.user_id == user.id,
                    GameSession.status == "active",
                )
                .first()
            )

            if not session:
                return {"success": False, "error": "Sesión no encontrada"}

            # Obtener datos de la pregunta
            game_data = json.loads(session.current_data)
            correct_answer = game_data["correct_answer"]
            reward = game_data["reward"]

            # Verificar respuesta
            is_correct = answer == correct_answer

            if is_correct:
                # Otorgar recompensa
                UserService.add_besitos(db, user, reward)
                session.score = reward
                session.besitos_earned = reward
                result_text = f"🎉 ¡Correcto! Has ganado {reward} besitos"
            else:
                session.score = 0
                result_text = f"❌ Incorrecto. La respuesta correcta era: {game_data['options'][correct_answer]}"

            # Finalizar sesión
            session.status = "completed"
            db.commit()

            return {
                "success": True,
                "correct": is_correct,
                "result": result_text,
                "reward": reward if is_correct else 0,
                "correct_answer": game_data["options"][correct_answer],
            }

        except Exception as e:
            logger.error(f"Error procesando respuesta trivia: {e}")
            db.rollback()
            return {"success": False, "error": str(e)}

    @staticmethod
    def play_roulette(db: Session, user: User) -> dict:
        """Juega la ruleta de besitos"""
        try:
            # Verificar que el usuario pueda pagar
            cost = 20
            if user.besitos < cost:
                return {
                    "success": False,
                    "error": f"Necesitas {cost} besitos para jugar la ruleta",
                }

            # Cobrar el costo
            UserService.subtract_besitos(db, user, cost)

            # Seleccionar premio basado en probabilidades
            total_prob = sum(prize["probability"] for prize in GameService.ROULETTE_PRIZES)
            rand = random.randint(1, total_prob)

            current_prob = 0
            selected_prize = None

            for prize in GameService.ROULETTE_PRIZES:
                current_prob += prize["probability"]
                if rand <= current_prob:
                    selected_prize = prize
                    break

            if not selected_prize:
                selected_prize = GameService.ROULETTE_PRIZES[0]  # Fallback

            # Otorgar premio
            prize_value = selected_prize["value"]
            UserService.add_besitos(db, user, prize_value)

            # Crear sesión de juego
            game_session = GameSession(
                user_id=user.id,
                game_type="roulette",
                score=prize_value,
                besitos_earned=prize_value - cost,
                status="completed",
                current_data=json.dumps(
                    {
                        "cost": cost,
                        "prize": selected_prize["prize"],
                        "value": prize_value,
                    }
                ),
            )

            db.add(game_session)
            db.commit()

            # Tracking de misión
            MissionTracker.track_action(db, user, "game_played", {"game_type": "roulette"})

            return {
                "success": True,
                "prize": selected_prize["prize"],
                "value": prize_value,
                "cost": cost,
                "net_gain": prize_value - cost,
                "new_balance": user.besitos,
            }

        except Exception as e:
            logger.error(f"Error en ruleta: {e}")
            db.rollback()
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_user_game_stats(db: Session, user: User) -> dict:
        """Obtiene estadísticas de juegos del usuario"""
        try:
            sessions = db.query(GameSession).filter(GameSession.user_id == user.id).all()

            stats = {
                "total_games": len(sessions),
                "total_besitos_earned": sum(s.besitos_earned for s in sessions),
                "trivia_played": len([s for s in sessions if s.game_type == "trivia"]),
                "roulette_played": len([s for s in sessions if s.game_type == "roulette"]),
                "best_trivia_score": max(
                    [s.score for s in sessions if s.game_type == "trivia"], default=0
                ),
            }

            return stats

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
