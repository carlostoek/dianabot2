
from utils.notification_scheduler import send_random_notifications

async def dispatch_notifications(bot):
    await send_random_notifications(bot)
