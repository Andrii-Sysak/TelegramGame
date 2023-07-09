from random import randint

from sqlalchemy import select

from game.db.models import CellType
from game.db.models.mob import (
    Mob,
    Mob2CellType,
)
from game.db.session import s


async def create_mob(name: str, emoji: str, cells: dict[CellType, int]) -> Mob:
    mob = Mob(name=name, emoji=emoji)
    s.session.add(mob)
    for cell, rate in cells.items():
        s.session.add(Mob2CellType(cell_type=cell, rate=rate, mob=mob))

    await s.session.flush()

    return mob


async def generate_mob(cell: CellType) -> Mob | None:
    mobs = (await s.session.scalars(
        select(Mob, Mob2CellType.rate)
        .where(Mob.cells.contains(cell))
        .order_by(Mob2CellType.rate)
    )).all()

    chance = randint(0, 100)
    for mob, rate in mobs:
        if rate >= chance:
            return  mob
    return None
