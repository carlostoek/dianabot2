from aiogram import Router
from aiogram.types import Message
from services.notification_service import NotificationService

notifications_router = Router()
notification_service = NotificationService()

@notifications_router.message()
async def handle_notifications(message: Message):
    await notification_service.create_notification(message.from_user.id, "general", "Has interactuado con el bot.", "neutral", "mayordomo")
    await message.answer("🔔 Notificación registrada.")
