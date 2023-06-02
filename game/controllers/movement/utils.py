from math import floor

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from game.bl.cell import get_cells_around
from game.db.models import Player, Cell
from game.db.session import s


async def render_map(player_id: int,):
    player = await s.session.get(Player, player_id)
    border = floor(player.region.size / 2) - player.view

    x_shift = (
        (abs(player.x) % border or border)
        * (abs(player.x) // player.x)
        if abs(player.x) > border else 0
    )
    y_shift = (
        (abs(player.y) % border or border)
        * (abs(player.y) // player.y)
        if abs(player.y) > border else 0
    )

    _cells = await get_cells_around(
        player.region_id,
        player.x - x_shift,
        player.y - y_shift,
        player.view
    )
    _cells[
        floor(len(_cells) / 2)
        + x_shift
        - y_shift * (player.view * 2 + 1)
    ] = player

    cells = ''.join(
        cell.emoji
        if (
            isinstance(cell, Cell) and cell.type.slug != 'empty'
            or isinstance(cell, Player)
        )
        else player.background_emoji
        for cell in _cells
    )

    chunk = len(cells)
    chunk_size = chunk // (player.view * 2 + 1)

    return '\n'.join(
        cells[i:i + chunk_size] for i in range(0, chunk, chunk_size)
    )


directions = {
    '↖️': (-1, 1),
    '⬆️': (0, 1),
    '↗️': (1, 1),
    '⬅️': (-1, 0),
    '➡️': (1, 0),
    '↙️': (-1, -1),
    '⬇️': (0, -1),
    '↘️': (1, -1),
}
mov_keyboard = ReplyKeyboardBuilder()

for dir in directions.keys():
    mov_keyboard.button(text=dir)
mov_keyboard.adjust(3, 2, 3)
