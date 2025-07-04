from aiogram import Router, F
from aiogram.types import Message
from services.user_service import UserService
from services.combination_service import CombinationService
from utils.helpers import validate_piece_code

combination_router = Router()
user_service = UserService()
combination_service = CombinationService()

@combination_router.message(F.text.startswith("🧹 Combinar "))
async def combine_pieces(message: Message):
    try:
        user = await user_service.get_or_create_user(message.from_user)
        parts = message.text.replace("🧹 Combinar ", "").split("+")

        if len(parts) != 2:
            await message.answer("Formato inválido. Usa: 🧹 Combinar código1 + código2")
            return

        code1 = parts[0].strip()
        code2 = parts[1].strip()

        if not validate_piece_code(code1) or not validate_piece_code(code2):
            await message.answer("Uno de los códigos es inválido.")
            return

        result = await combination_service.combine(user.telegram_id, code1, code2)

        if result:
            await message.answer(f"Combinación exitosa. Obtuviste: {result.title}")
        else:
            await message.answer("Esa combinación... fascinante... mente inútil.")
    except Exception:
        await message.answer("Hubo un error al intentar combinar las piezas.")
