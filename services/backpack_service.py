
from sqlalchemy.future import select
from database_init import get_db
from models.core import User
from models.narrative import LorePiece, UserBackpack

class BackpackService:
    async def get_user_backpack(self, telegram_id):
        async for session in get_db():
            result = await session.execute(
                select(UserBackpack, LorePiece)
                .join(User, User.id == UserBackpack.user_id)
                .join(LorePiece, LorePiece.id == UserBackpack.lore_piece_id)
                .where(User.telegram_id == telegram_id)
            )
            records = result.all()

            backpack = []
            for user_backpack, lore_piece in records:
                backpack.append({
                    "title": lore_piece.title,
                    "description": lore_piece.description,
                    "rarity": lore_piece.rarity
                })

            return backpack
