import asyncio
from datetime import datetime

from aiogram import (
    Router,
    Bot,
)
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton
from sqlalchemy import select

from game.bl.player import move_player
from game.config import Config
from game.controllers.handlers.map.filters import (
    movement,
    in_action,
    teleporting,
)
from game.controllers.handlers.map.utils import (
    render_map,
    mov_keyboard,
    teleportation,
    regions_list,
    arrival_to_the_cell
)

from game.db.models import Player, Cell, Region
from game.db.models.action import Action
from game.db.session import s
from game.utils.delay import delay

movement_router = Router()


@movement_router.message(in_action)
async def cannot_move(message: Message, action: Action) -> None:
    await message.answer(
        f'І шо ти тута хочеш зробити? Чекай! Ти все ще в дорозі. '
        f'Ще цілих {action.end_date - datetime.utcnow()}'
    )


@movement_router.message(teleporting)
async def teleport(message: Message, player: Player, portal: Cell, bot: Bot) -> None:
    await message.answer(
            f'Через 5 секунд вас відправлено в новий регіон',
        )
    await move_player(player, 0, 0, 2)

    map = await render_map(player)
    asyncio.create_task(delay(
        message.answer(map, reply_markup=mov_keyboard.as_markup()),
        Config.c.durations.movement
    ))


@movement_router.message(movement)
async def move(message: Message, player: Player, dest: Cell, bot: Bot) -> None:
    if not dest.type.passable:
        await message.answer(
            'ВИБАЧ, ТУДА НЕ МОНА.',
            reply_markup=mov_keyboard.as_markup()
        )
        return

    await move_player(player, dest.x, dest.y, player.region_id)
    await message.answer(
        f'Чудово! Через {Config.c.durations.movement} секунд будеш на місці'
    )

    await asyncio.create_task(delay(
        arrival_to_the_cell(player, dest, message),
        Config.c.durations.movement
    ))


@movement_router.message(Command(commands=['map']))
async def show_map(message: Message, player: Player) -> None:
    msg = await render_map(player)

    await message.answer(msg, reply_markup=mov_keyboard.as_markup())


@movement_router.message(Command(commands=['around']))
async def show_players_around(message: Message, player: Player) -> None:
    players_around = (await s.session.scalars(
        select(Player).where(Player.id != player.id)
        .where(player.x - 3 <= Player.x).where(Player.x <= player.x + 3)
        .where(player.y - 3 <= Player.y).where(Player.y <= player.y + 3)
    )).all()

    await message.answer(
        'Around you:\n' +
        (
            '\n'.join([f'{p.name} {p.x} {p.y}' for p in players_around])
            if players_around else 'No one'
        ),
        reply_markup=mov_keyboard.as_markup()
    )


@movement_router.message(Command(commands=['profile']))
async def show_player_profile_info(message: Message, player: Player) -> None:
    await message.answer(
        "Info about you: "
        f'{player.emoji} {player.name}\n'
        f'x-{player.x} y-{player.y}\n'
        f'🗺 - {player.region_id}\n'
        f'❤️ - {player.health}\n'
        f'🗡 - {player.base_damage}\n'
        'Elements: \n'
        f'🔥 - {player.soul.fire_element}\n'
        f'💧 - {player.soul.water_element}\n'
        f'🌳 - {player.soul.tree_element}\n'
        f'🔩 - {player.soul.metal_element}\n'
        f'⛰ - {player.soul.earth_element}\n'
    )
