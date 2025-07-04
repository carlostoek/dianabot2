from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    user_onboarding = State()
    viewing_backpack = State()
