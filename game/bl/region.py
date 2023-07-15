from math import (
    sqrt,
    floor
)

from sqlalchemy import select

from game.db.models import (
    Cell,
    Region,
    CellType
)
from game.db.session import s


async def fill_from_emoji_map(region: Region, emoji_map: str) -> list[Cell]:
    emojis = {
        cell.emoji: cell
        for cell in
        (await s.session.scalars(
            select(CellType).where(CellType.emoji.in_(set(emoji_map)))
        )).all()
    }
    emoji_map = emoji_map.replace('\n', '')
    size = int(sqrt(len(emoji_map)))
    cell_map = []
    for index, emoji in enumerate(emoji_map):
        y = floor(size / 2) - index // size
        x = -floor(size / 2) + index % size
        cell_map.append(Cell(
            region_id=1,
            x=x,
            y=y,
            cell_type_id=emojis[emoji].id
        ))

    region.map = cell_map
    region.size = size
    await s.session.flush()

    return cell_map
