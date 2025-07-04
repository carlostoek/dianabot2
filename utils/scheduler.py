import asyncio
from tasks.subscription_checker import check_subscriptions
from tasks.mission_assigner import assign_daily_missions
from tasks.notification_dispatcher import dispatch_notifications

async def scheduler(bot):
    while True:
        await check_subscriptions(bot)
        await assign_daily_missions(bot)
        await dispatch_notifications(bot)
        await asyncio.sleep(3600)  # Ejecuta cada hora
