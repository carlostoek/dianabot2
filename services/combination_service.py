
from sqlalchemy.future import select
from database_init import get_db
from models.narrative import LorePiece

class CombinationService:
    async def combine_pieces(self, code1, code2):
        async for session in get_db():
            result = await session.execute(
                select(LorePiece).where(LorePiece.code == code1)
            )
            piece1 = result.scalar_one_or_none()

            result = await session.execute(
                select(LorePiece).where(LorePiece.code == code2)
            )
            piece2 = result.scalar_one_or_none()

            if piece1 and piece2 and piece1.combinable_with == piece2.code:
                return piece1.combination_result
            return None
