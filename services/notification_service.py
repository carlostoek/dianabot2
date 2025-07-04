
from sqlalchemy.future import select
from database_init import get_db
from models.notifications import Notification
from random import choice
from datetime import datetime

class NotificationService:
    async def create_notification(self, user_id):
        characters = ["🎲 Lucien", "🍿 Mayordomo"]
        messages = [
            "Alguien desbloqueó algo. No sé para qué, pero aquí estamos.",
            "Lo has logrado... probablemente por accidente.",
            "Notificación relevante… o no tanto.",
            "Este es uno de esos momentos en que fingimos que importa.",
        ]

        character = choice(characters)
        message = choice(messages)

        async for session in get_db():
            new_notification = Notification(
                user_id=user_id,
                notification_type="random",
                message=message,
                tone="sarcasm",
                character=character,
                was_delivered=True
            )
            session.add(new_notification)
            await session.commit()
            await session.refresh(new_notification)

            return {"character": character, "message": message}
