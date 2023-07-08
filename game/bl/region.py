from math import sqrt, floor

from game.db.models import Cell, CellType, Region
from game.db.models.cell import CellType
from game.db.session import s


async def fill_from_emoji_map(region: Region, emoji_map: str) -> list[Cell]:
    rock = await s.session.get(CellType, 2)
    void = await s.session.get(CellType, 1)
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
            cell_type_id=(
                rock.id
                if emoji == '🪨'
                else void.id
            )
        ))

    region.map = cell_map
    region.size = size
    await s.session.flush()

    return cell_map

