# DianaBot - Telegram Bot in Python using Aiogram 3

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

API_TOKEN = "7729570402:AAHHPqCQ9eUg2D0hJzlWjYIXd5Hw3_QfYGE"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- Data Models (in-memory for demo purposes) ---

class UserData:
    def __init__(self):
        self.level = 1
        self.points = 0
        self.missions_completed = set()
        self.current_scene = 0
        self.vip_expiry = None
        self.stats = {
            "besitos": 0,
            "missions_done": 0,
            "games_played": 0,
            "trivias_won": 0,
        }

users = {}

missions = {
    1: {"title": "Primer Besito", "description": "Envía 5 besitos para ganar puntos.", "reward": 10},
    2: {"title": "Explorador", "description": "Desbloquea 3 escenas narrativas.", "reward": 20},
    3: {"title": "Trivia Novato", "description": "Gana tu primera trivia.", "reward": 15},
    4: {"title": "Ruleta Rápida", "description": "Juega 3 partidas de ruleta.", "reward": 25},
    5: {"title": "VIP Aspirante", "description": "Consigue estado VIP por 1 día.", "reward": 50},
}

narrative_scenes = [
    "Lucien: Bienvenido a la aventura, valiente explorador. ¿Listo para comenzar?",
    "Lucien: Cada misión te acerca más a la verdad oculta en este mundo.",
    "Lucien: Recuerda, los besitos son la moneda de tu progreso.",
    "Lucien: La ruleta puede cambiar tu destino, ¡gira con sabiduría!",
    "Lucien: Has desbloqueado un secreto antiguo, sigue adelante.",
]

trivia_questions = [
    {"question": "¿Cuál es la capital de Francia?", "options": ["Madrid", "París", "Berlín", "Roma"], "answer": 1},
    {"question": "¿Cuántos continentes hay en la Tierra?", "options": ["5", "6", "7", "8"], "answer": 2},
    {"question": "¿Quién escribió 'Cien años de soledad'?", "options": ["Gabriel García Márquez", "Pablo Neruda", "Mario Vargas Llosa", "Julio Cortázar"], "answer": 0},
]

# --- States for FSM ---

class NarrativeStates(StatesGroup):
    in_narrative = State()

class TriviaStates(StatesGroup):
    in_trivia = State()
    question_index = State()
    score = State()

class RouletteStates(StatesGroup):
    in_roulette = State()

# --- Utils Module ---

class LucienVoice:
    @staticmethod
    def welcome(user_name: str) -> str:
        return f"👋 ¡Hola, {user_name}! Soy Lucien, tu narrador en esta aventura. ¡Vamos a comenzar! 🌟"

    @staticmethod
    def narrative(scene_index: int) -> str:
        if 0 <= scene_index < len(narrative_scenes):
            return narrative_scenes[scene_index]
        return "Lucien: No hay más escenas por ahora."

    @staticmethod
    def format_profile(user_id: int) -> str:
        user = users.get(user_id)
        if not user:
            return "Usuario no encontrado."
        return (
            f"👤 Perfil de usuario:\n"
            f"Nivel: {user.level}\n"
            f"Puntos (Besitos): {user.points}\n"
            f"Misiones completadas: {len(user.missions_completed)}\n"
            f"Escena narrativa actual: {user.current_scene + 1} / {len(narrative_scenes)}\n"
            f"VIP activo: {'Sí' if user.vip_expiry and user.vip_expiry > datetime.now() else 'No'}\n"
            f"\n📊 Estadísticas:\n"
            f"Besitos dados: {user.stats['besitos']}\n"
            f"Misiones completadas: {user.stats['missions_done']}\n"
            f"Juegos jugados: {user.stats['games_played']}\n"
            f"Trivias ganadas: {user.stats['trivias_won']}\n"
        )

# --- Keyboards Module ---

class Keyboards:
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.button(text="🎯 Misiones", callback_data="menu_missions")
        kb.button(text="🎮 Juegos", callback_data="menu_games")
        kb.button(text="👤 Perfil", callback_data="menu_profile")
        kb.adjust(1)
        return kb.as_markup()

    @staticmethod
    def missions_menu(user_id: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for mid, mission in missions.items():
            status = "✅" if mid in users.get(user_id, UserData()).missions_completed else "❌"
            kb.button(text=f"{status} {mission['title']}", callback_data=f"mission_{mid}")
        kb.button(text="⬅️ Volver", callback_data="menu_main")
        kb.adjust(1)
        return kb.as_markup()

    @staticmethod
    def games_menu() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.button(text="❓ Trivia", callback_data="game_trivia")
        kb.button(text="🎡 Ruleta", callback_data="game_roulette")
        kb.button(text="⬅️ Volver", callback_data="menu_main")
        kb.adjust(1)
        return kb.as_markup()

    @staticmethod
    def profile_menu() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.button(text="📖 Narrativa", callback_data="menu_narrative")
        kb.button(text="⬅️ Volver", callback_data="menu_main")
        kb.adjust(1)
        return kb.as_markup()

    @staticmethod
    def narrative_menu(user_id: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        user = users.get(user_id, UserData())
        if user.current_scene > 0:
            kb.button(text="⬅️ Escena anterior", callback_data="narrative_prev")
        if user.current_scene < len(narrative_scenes) - 1:
            kb.button(text="Siguiente escena ➡️", callback_data="narrative_next")
        kb.button(text="⬅️ Volver", callback_data="menu_profile")
        kb.adjust(1)
        return kb.as_markup()

    @staticmethod
    def trivia_question(question_index: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        q = trivia_questions[question_index]
        for i, option in enumerate(q["options"]):
            kb.button(text=option, callback_data=f"trivia_answer_{question_index}_{i}")
        kb.adjust(1)
        return kb.as_markup()

    @staticmethod
    def roulette_menu() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.button(text="🎡 Girar ruleta", callback_data="roulette_spin")
        kb.button(text="⬅️ Volver", callback_data="menu_games")
        kb.adjust(1)
        return kb.as_markup()

# --- Handlers Module ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = UserData()
    await message.answer(LucienVoice.welcome(message.from_user.first_name), reply_markup=Keyboards.main_menu())

@dp.callback_query(Text(startswith="menu_"))
async def menu_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    if data == "menu_main":
        await callback.message.edit_text("Menú Principal:", reply_markup=Keyboards.main_menu())
    elif data == "menu_missions":
        await callback.message.edit_text("🎯 Misiones disponibles:", reply_markup=Keyboards.missions_menu(user_id))
    elif data == "menu_games":
        await callback.message.edit_text("🎮 Juegos disponibles:", reply_markup=Keyboards.games_menu())
    elif data == "menu_profile":
        profile_text = LucienVoice.format_profile(user_id)
        await callback.message.edit_text(profile_text, reply_markup=Keyboards.profile_menu())
    elif data == "menu_narrative":
        user = users.get(user_id, UserData())
        scene_text = LucienVoice.narrative(user.current_scene)
        await callback.message.edit_text(scene_text, reply_markup=Keyboards.narrative_menu(user_id))
    await callback.answer()

@dp.callback_query(Text(startswith="mission_"))
async def mission_detail(callback: CallbackQuery):
    user_id = callback.from_user.id
    mid = int(callback.data.split("_")[1])
    mission = missions.get(mid)
    user = users.get(user_id, UserData())
    completed = mid in user.missions_completed
    text = (
        f"🎯 Misión: {mission['title']}\n\n"
        f"{mission['description']}\n\n"
        f"Recompensa: {mission['reward']} besitos\n\n"
        f"Estado: {'✅ Completada' if completed else '❌ Pendiente'}"
    )
    kb = InlineKeyboardBuilder()
    if not completed:
        kb.button(text="Marcar como completada", callback_data=f"complete_mission_{mid}")
    kb.button(text="⬅️ Volver a misiones", callback_data="menu_missions")
    kb.adjust(1)
    await callback.message.edit_text(text, reply_markup=kb.as_markup())
    await callback.answer()

@dp.callback_query(Text(startswith="complete_mission_"))
async def complete_mission(callback: CallbackQuery):
    user_id = callback.from_user.id
    mid = int(callback.data.split("_")[2])
    user = users.get(user_id, UserData())
    if mid not in user.missions_completed:
        user.missions_completed.add(mid)
        reward = missions[mid]["reward"]
        user.points += reward
        user.stats["missions_done"] += 1
        if user.points >= user.level * 50:
            user.level += 1
        await callback.answer(f"¡Misión completada! Has ganado {reward} besitos 🎉", show_alert=True)
    else:
        await callback.answer("Ya completaste esta misión.", show_alert=True)
    await callback.message.edit_text("🎯 Misiones disponibles:", reply_markup=Keyboards.missions_menu(user_id))

@dp.callback_query(Text(startswith="narrative_"))
async def narrative_navigation(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = users.get(user_id, UserData())
    if callback.data == "narrative_next":
        if user.current_scene < len(narrative_scenes) - 1:
            user.current_scene += 1
    elif callback.data == "narrative_prev":
        if user.current_scene > 0:
            user.current_scene -= 1
    scene_text = LucienVoice.narrative(user.current_scene)
    await callback.message.edit_text(scene_text, reply_markup=Keyboards.narrative_menu(user_id))
    await callback.answer()

@dp.callback_query(Text(startswith="game_"))
async def games_menu_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = callback.data
    if data == "game_trivia":
        await state.set_state(TriviaStates.in_trivia)
        await state.update_data(question_index=0, score=0)
        q = trivia_questions[0]
        text = f"❓ Trivia: {q['question']}"
        await callback.message.edit_text(text, reply_markup=Keyboards.trivia_question(0))
    elif data == "game_roulette":
        await state.set_state(RouletteStates.in_roulette)
        await callback.message.edit_text("🎡 Ruleta - Presiona girar para jugar.", reply_markup=Keyboards.roulette_menu())
    await callback.answer()
    
@dp.callback_query(Text(startswith="trivia_answer_"), TriviaStates.in_trivia)
async def trivia_answer(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = callback.data.split("_")
    question_index = int(data[2])
    selected_option = int(data[3])
    q = trivia_questions[question_index]
    user = users.get(user_id, UserData())
    state_data = await state.get_data()
    score = state_data.get("score", 0)

    if selected_option == q["answer"]:
        score += 1
        await callback.answer("¡Correcto! 🎉")
    else:
        await callback.answer(f"Incorrecto. La respuesta correcta era: {q['options'][q['answer']]}", show_alert=True)

    question_index += 1
    if question_index < len(trivia_questions):
        await state.update_data(question_index=question_index, score=score)
        q_next = trivia_questions[question_index]
        text = f"❓ Trivia: {q_next['question']}"
        await callback.message.edit_text(text, reply_markup=Keyboards.trivia_question(question_index))
    else:
        user.stats["games_played"] += 1
        if score >= len(trivia_questions) // 2:
            user.stats["trivias_won"] += 1
            reward = 20
            user.points += reward
            text = f"🏆 Trivia finalizada. Puntuación: {score}/{len(trivia_questions)}.\n¡Ganaste {reward} besitos!"
        else:
            text = f"Trivia finalizada. Puntuación: {score}/{len(trivia_questions)}.\nSigue intentando para ganar besitos."
        await state.clear()
        await callback.message.edit_text(text, reply_markup=Keyboards.games_menu())

@dp.callback_query(Text("roulette_spin"), RouletteStates.in_roulette)
async def roulette_spin(callback: CallbackQuery, state: FSMContext):
    import random
    user_id = callback.from_user.id
    user = users.get(user_id, UserData())
    user.stats["games_played"] += 1
    prizes = [0, 5, 10, 20, 50]
    prize = random.choice(prizes)
    user.points += prize
    text = f"🎡 Giraste la ruleta y ganaste {prize} besitos!"
    await callback.message.edit_text(text, reply_markup=Keyboards.roulette_menu())
    await callback.answer()

@dp.callback_query(Text("menu_profile"))
async def profile_menu_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    profile_text = LucienVoice.format_profile(user_id)
    await callback.message.edit_text(profile_text, reply_markup=Keyboards.profile_menu())
    await callback.answer()

@dp.callback_query(Text("menu_narrative"))
async def narrative_menu_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = users.get(user_id, UserData())
    scene_text = LucienVoice.narrative(user.current_scene)
    await callback.message.edit_text(scene_text, reply_markup=Keyboards.narrative_menu(user_id))
    await callback.answer()

@dp.callback_query(Text("menu_missions"))
async def missions_menu_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text("🎯 Misiones disponibles:", reply_markup=Keyboards.missions_menu(user_id))
    await callback.answer()

@dp.callback_query(Text("menu_games"))
async def games_menu_handler2(callback: CallbackQuery):
    await callback.message.edit_text("🎮 Juegos disponibles:", reply_markup=Keyboards.games_menu())
    await callback.answer()

@dp.callback_query(Text("menu_main"))
async def main_menu_handler(callback: CallbackQuery):
    await callback.message.edit_text("Menú Principal:", reply_markup=Keyboards.main_menu())
    await callback.answer()

# --- Jobs Module ---

async def scheduled_tasks():
    while True:
        now = datetime.now()
        for user_id, user in users.items():
            if user.vip_expiry and user.vip_expiry < now:
                user.vip_expiry = None
                try:
                    await bot.send_message(user_id, "⏰ Tu estado VIP ha expirado.")
                except Exception:
                    pass
        await asyncio.sleep(3600)

# --- Main ---

async def main():
    dp.startup.register(startup)
    await dp.start_polling(bot)

async def startup():
    asyncio.create_task(scheduled_tasks())

if __name__ == "__main__":
    asyncio.run(main())
