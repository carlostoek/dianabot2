from aiogram.fsm.state import StatesGroup, State

class AdminMenu(StatesGroup):
    main = State()

class EditingConfigurations(StatesGroup):
    editing = State()

class ManagingUsers(StatesGroup):
    managing = State()

class VipTariff(StatesGroup):
    waiting_for_name = State()
    waiting_for_duration = State()
    waiting_for_cost = State()

class VipToken(StatesGroup):
    waiting_for_tariff_selection = State()
    waiting_for_channel_id = State()