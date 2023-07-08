from sqlalchemy import select, and_

from game.db.models.cell import Cell, CellType
from game.db.session import s


async def create_cell_type(slug: str, emoji: str, passable: bool) -> CellType:
    cell = CellType(slug=slug, emoji=emoji, passable=passable)
    s.session.add(cell)

    return cell


async def get_cells_around(
    reg_id: int,
    x: int,
    y: int,
    range: int
) -> list[Cell]:
    res = await s.session.scalars(
        select(Cell)
        .where(Cell.region_id == reg_id)
        .where(and_(Cell.x <= x + range, Cell.x >= x - range))
        .where(and_(Cell.y <= y + range, Cell.y >= y - range))
        .order_by(Cell.y.desc(), Cell.x.asc())
    )

    return res.all()
