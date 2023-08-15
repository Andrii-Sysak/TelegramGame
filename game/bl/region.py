import re
from math import (
    sqrt,
    floor
)

from sqlalchemy import (
    or_,
    select
)

from game.db.models import (
    Cell,
    Region,
    CellType
)
from game.db.session import s
from game.db.presets.unique_cell import unique_cells

async def fill_from_emoji_map(region: Region, emoji_map: str) -> list[Cell]:
    emoji_map_list = made_list_map_from_string(emoji_map)

    condition_emoji = CellType.emoji.in_(set(emoji_map_list))
    condition_slug = CellType.slug.in_(set(emoji_map_list))

    results = (await s.session.scalars(
        select(CellType)
        .where(or_(
            condition_emoji,
            condition_slug
        ))
    )).all()

    slugs = {cell.slug: cell for cell in results}

    emoji_map_slugs = convert_emoji_to_slug_map(emoji_map_list, slugs)
    size = int(sqrt(len(emoji_map_slugs)))
    cell_map = []
    for index, slug in enumerate(emoji_map_slugs):
        y = floor(size / 2) - index // size
        x = -floor(size / 2) + index % size

        properties = {}
        if slug in unique_cells:
            properties = unique_cells[slug].properties
            slug = unique_cells[slug].slug

        cell_map.append(Cell(
            region_id=Region.id,
            x=x,
            y=y,
            cell_type_slug=slug,
            properties=properties
        ))

    region.map = cell_map
    region.size = size
    await s.session.flush()

    return cell_map


EMOJI_MAP_SLUG_PATTERN = r"\[([^\]]+)\]|(\S)"


def made_list_map_from_string(emoji_map: str) -> list[str]:
    matches = re.findall(EMOJI_MAP_SLUG_PATTERN, emoji_map)
    emoji_map_list = [match[0] if match[0] else match[1] for match in matches]
    return emoji_map_list


def convert_emoji_to_slug_map(emoji_map_list: list, slugs: dict) -> list[str]:
    cell_slugs = {cell.emoji: cell.slug for cell in slugs.values()}
    emoji_map_slugs = []
    for cell in emoji_map_list:
        if cell not in unique_cells:
            emoji_map_slugs.append(cell_slugs[cell] if not cell.isalpha() else cell)
            continue
        emoji_map_slugs.append(cell)

    return emoji_map_slugs
