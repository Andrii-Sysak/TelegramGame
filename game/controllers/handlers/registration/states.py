from aiogram.fsm.state import StatesGroup, State


class Reg(StatesGroup):
    unregistered = State()
    name = State()
    name2 = State()
    background_emoji = State()
