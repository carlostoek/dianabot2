
from aiogram.fsm.state import StatesGroup, State

class UserOnboarding(StatesGroup):
    onboarding_complete = State()

class ViewingBackpack(StatesGroup):
    viewing = State()

class ChannelJoin(StatesGroup):
    awaiting_token = State()
