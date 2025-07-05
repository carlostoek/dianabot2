from datetime import datetime
from sqlalchemy.orm import Session
from models.vip import VIPAccess
from services.channel_service import ChannelService
from core.database import get_db_session
import logging

logger = logging.getLogger(__name__)

class SubscriptionChecker:
    @staticmethod
    async def check_and_expire_vip_access():
        logger.info("Running VIP subscription checker...")
        db = get_db_session()
        try:
            expired_accesses = db.query(VIPAccess).filter(
                VIPAccess.is_active == True,
                VIPAccess.access_expires <= datetime.utcnow()
            ).all()

            for access in expired_accesses:
                logger.info(f"VIP access expired for user {access.user_id} in channel {access.channel_id}")
                # Here you would typically remove the user from the Telegram channel
                # For now, we'll just mark their access as inactive in the DB
                access.is_active = False
                db.add(access)
                # Example of how you might remove them from the channel (requires bot admin rights in channel)
                # await ChannelService.remove_user_from_channel(access.channel_id, access.user_id)

            db.commit()
            logger.info(f"Finished VIP subscription checker. {len(expired_accesses)} accesses expired.")
        except Exception as e:
            logger.error(f"Error in VIP subscription checker: {e}")
        finally:
            db.close()