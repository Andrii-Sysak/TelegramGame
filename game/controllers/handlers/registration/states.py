from aiogram.fsm.state import (
    State,
    StatesGroup
)


class Reg(StatesGroup):
    unregistered = State()
    name = State()
    name2 = State()
    background_emoji = State()
