
from aiogram import Router, types
from aiogram.filters import Command
from services.notification_service import NotificationService

router = Router()
notification_service = NotificationService()

@router.message(Command("notify"))
async def send_notification(message: types.Message):
    user_id = message.from_user.id
    notification = await notification_service.create_notification(user_id)

    if notification:
        await message.answer(f"{notification['character']} {notification['message']}")
    else:
        await message.answer("🔔 No hay notificaciones pendientes.")
