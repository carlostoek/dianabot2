
from aiogram.fsm.state import StatesGroup, State

class AdminMenu(StatesGroup):
    main = State()

class EditingConfigurations(StatesGroup):
    editing = State()

class ManagingUsers(StatesGroup):
    managing = State()
