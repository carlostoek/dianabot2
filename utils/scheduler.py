
import asyncio
from tasks.subscription_checker import check_expired_subscriptions
from tasks.mission_assigner import assign_daily_missions
from tasks.notification_dispatcher import dispatch_notifications
from tasks.channel_access import process_channel_tasks

async def run_scheduler(bot):
    while True:
        await check_expired_subscriptions(bot)
        await assign_daily_missions(bot)
        await dispatch_notifications(bot)
        await process_channel_tasks(bot)
        await asyncio.sleep(3600)  # Ejecuta todas las tareas cada hora
