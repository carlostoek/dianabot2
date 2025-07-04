from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    admin_menu = State()
    editing_configurations = State()
    managing_users = State()
