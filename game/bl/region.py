from math import sqrt, floor
import re

from game.db.models import Cell, CellType, Region
from game.db.models.cell import CellType
from game.db.session import s
from sqlalchemy import select, or_

# async def fill_from_emoji_map(region: Region, emoji_map: str) -> list[Cell]:
#     emojis = {
#         cell.emoji: cell
#         for cell in
#         (await s.session.scalars(
#             select(CellType).where(CellType.emoji.in_(set(emoji_map)))
#         )).all()
#     }
#     emoji_map = emoji_map.replace('\n', '')
#     size = int(sqrt(len(emoji_map)))
#     cell_map = []
#     for index, emoji in enumerate(emoji_map):
#         y = floor(size / 2) - index // size
#         x = -floor(size / 2) + index % size
#         cell_map.append(Cell(
#             region_id=1,
#             x=x,
#             y=y,
#             cell_type_slug=emojis[emoji].slug
#         ))
#
#     region.map = cell_map
#     region.size = size
#     await s.session.flush()
#
#     return cell_map


async def fill_from_emoji_map(region: Region, emoji_map: str) -> list[Cell]:
    emoji_map_list = made_list_map_from_string(emoji_map)

    condition_emoji = CellType.emoji.in_(set(emoji_map_list))
    condition_slug = CellType.slug.in_(set(emoji_map_list))

    query = select(CellType).where(or_(
        condition_emoji,
        condition_slug
    ))

    results = await s.session.execute(query)
    slugs = {cell.slug: cell for cell in results.scalars().all()}
    print('------------------------------------', slugs)

    map_list = convert_emoji_to_slug_map(emoji_map_list, slugs)

    size = int(sqrt(len(emoji_map_list)))
    cell_map = []


    print('----------------------------------\n', set(emoji_map_list), set(map_list), '\n-----------------------------')
    for index, slug in enumerate(map_list):
        y = floor(size / 2) - index // size
        x = -floor(size / 2) + index % size
        cell_map.append(Cell(
            region_id=1,
            x=x,
            y=y,
            cell_type_slug=slug
        ))

    region.map = cell_map
    region.size = size
    await s.session.flush()

    return cell_map


def made_list_map_from_string(emoji_map: str) -> list[str]:
    pattern = r"\[([^\]]+)\]|(\S)"
    matches = re.findall(pattern, emoji_map)
    result = [match[0] if match[0] else match[1] for match in matches]
    return result


def convert_emoji_to_slug_map(emoji_map_list: list, slugs: dict) -> list[str]:
    cell_slugs = {}
    for cell in slugs.values():
        cell_slugs[cell.emoji] = cell.slug

    result = []
    for cell in emoji_map_list:
        if len(cell) == 1:
            result.append(cell_slugs[cell])
        else:
            result.append(cell)

    return result
