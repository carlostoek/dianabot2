
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services.combination_service import CombinationService
from states.user_states import CombiningPieces

router = Router()
combination_service = CombinationService()

@router.message(Command("combine"))
async def start_combination(message: types.Message, state: FSMContext):
    await message.answer("🔑 Ingresa el código de la primera pieza:")
    await state.set_state(CombiningPieces.awaiting_first_piece)

@router.message(CombiningPieces.awaiting_first_piece)
async def receive_first_piece(message: types.Message, state: FSMContext):
    await state.update_data(first_piece=message.text.strip())
    await message.answer("🔑 Ingresa el código de la segunda pieza:")
    await state.set_state(CombiningPieces.awaiting_second_piece)

@router.message(CombiningPieces.awaiting_second_piece)
async def receive_second_piece(message: types.Message, state: FSMContext):
    data = await state.get_data()
    first_piece = data.get("first_piece")
    second_piece = message.text.strip()

    result = await combination_service.combine_pieces(first_piece, second_piece)

    if result:
        await message.answer(f"🎉 ¡Combinación exitosa! Has obtenido: {result}")
    else:
        await message.answer("❌ Combinación no válida. Inténtalo de nuevo con otras piezas.")

    await state.clear()
