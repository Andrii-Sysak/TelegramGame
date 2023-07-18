import asyncio

from aiogram import Router
from sqlalchemy import select
from aiogram.types import Message
from aiogram.filters import Command

from game.bl.mob import generate_mob
from game.config import Config
from game.bl.action import action
from game.bl.player import move_player
from game.db.models import (
    Cell,
    Player
)
from game.db.session import s
from game.utils.delay import delay
from game.db.models.action import ActionBusynessLevel
from game.db.presets.cell_type import portal
from game.controllers.handlers.map.utils import (
    render_map,
    mov_keyboard
)
from game.controllers.handlers.map.filters import MovementFilter

movement_router = Router()


@movement_router.message(MovementFilter(portal))
@action(ActionBusynessLevel.blocking, lambda: Config.c.durations.movement)
async def handle_movement_portal(message: Message, player: Player) -> None:
    await message.answer(
        f'Через {Config.c.durations.movement} секунд вас буде '
        f'відправлено в новий регіон',
    )
    await move_player(player, 0, 0, 2)

    map = await render_map(player)
    asyncio.create_task(delay(
        message.answer(map, reply_markup=mov_keyboard.as_markup()),
        Config.c.durations.movement
    ))


@movement_router.message(MovementFilter())
@action(ActionBusynessLevel.blocking, lambda: Config.c.durations.movement)
async def handle_movement(message: Message, player: Player, dest: Cell) -> None:
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
    map = await render_map(player)
    mob = await generate_mob(dest.type)
    if mob:
        map += (
            f'\n\nТо пезда, тобі трапився:\n '
            f'{mob.emoji} {mob.name}: ❤️ {mob.health} 🗡  {mob.bade_damage}'
        )

    asyncio.create_task(delay(
        message.answer(map),
        Config.c.durations.movement
    ))


@movement_router.message(Command(commands=['map']))
async def handle_show_map(message: Message, player: Player) -> None:
    msg = await render_map(player)

    await message.answer(msg, reply_markup=mov_keyboard.as_markup())


@movement_router.message(Command(commands=['around']))
async def handle_show_around(message: Message, player: Player) -> None:
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
async def handle_profile(message: Message, player: Player) -> None:
    assert player.soul
    await message.answer(
        "Info about you: "
        f'{player.emoji} {player.name}\n'
        f'x-{player.x} y-{player.y}\n'
        f'🗺 - {player.region_id}\n'
        f'🌁 - {player.region.continent_id}\n'
        f'🪐 - {player.region.continent.planet_id}\n'
        f'❤️ - {player.health}\n'
        f'🗡 - {player.base_damage}\n'
        'Elements: \n'
        f'🔥 - {player.soul.fire_element}\n'
        f'💧 - {player.soul.water_element}\n'
        f'🌳 - {player.soul.tree_element}\n'
        f'🔩 - {player.soul.metal_element}\n'
        f'⛰ - {player.soul.earth_element}\n'
    )
