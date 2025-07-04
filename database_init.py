
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
# Crear tablas al iniciar el bot
async def init_db():
    async with engine.begin() as conn:
        from models.core import Base as CoreBase
        from models.narrative import Base as NarrativeBase
        from models.vip import Base as VipBase
        from models.gamification import Base as GamificationBase
        from models.notifications import Base as NotificationBase

        await conn.run_sync(CoreBase.metadata.create_all)
        await conn.run_sync(NarrativeBase.metadata.create_all)
        await conn.run_sync(VipBase.metadata.create_all)
        await conn.run_sync(GamificationBase.metadata.create_all)
        await conn.run_sync(NotificationBase.metadata.create_all)
