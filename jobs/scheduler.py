from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tasks.subscription_checker import SubscriptionChecker
import logging

logger = logging.getLogger(__name__)

def setup_scheduler():
    scheduler = AsyncIOScheduler()

    # Schedule the VIP subscription checker to run daily
    scheduler.add_job(
        SubscriptionChecker.check_and_expire_vip_access,
        'interval',
        days=1,
        id='vip_subscription_checker',
        replace_existing=True
    )

    logger.info("Scheduler configured with VIP subscription checker.")
    return scheduler
