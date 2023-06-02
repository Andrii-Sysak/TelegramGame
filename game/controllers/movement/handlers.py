from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from game.controllers.movement.filters import movement
from game.controllers.movement.utils import render_map, mov_keyboard
from game.db.models import Player, Cell

movement_router = Router()


@movement_router.message(movement)
async def move(message: Message, player: Player, dest: Cell) -> None:
    if not dest.type.passable:
        await message.answer(
            'ВИБАЧ, ТУДА НЕ МОНА.',
            reply_markup=mov_keyboard.as_markup()
        )
        return
    player.x = dest.x
    player.y = dest.y

    msg = await render_map(player.telegram_id)
    await message.answer(msg, reply_markup=mov_keyboard.as_markup())


@movement_router.message(Command(commands=['map']))
async def show_map(message: Message, player: Player) -> None:
    msg = await render_map(player.telegram_id)

    await message.answer(msg, reply_markup=mov_keyboard.as_markup())
