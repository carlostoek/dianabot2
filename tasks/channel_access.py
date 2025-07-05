from services.channel_service import ChannelService

channel_service = ChannelService()

async def process_channel_tasks(bot):
    await channel_service.activate_pending(bot)
    await channel_service.expire_access(bot)
