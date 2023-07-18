import os
import logging

import yaml

from game.bl.mob import create_mob
from game.config import (
    Config,
    Settings
)
from game.bl.cell import create_cell_type
from game.db.base import Base
from game.bl.region import fill_from_emoji_map
from game.db.models import Region, Continent, Planet
from game.db.session import (
    s,
    eng,
    session
)
from game.presets.test_region import (
    emoji_map,
    ice_emoji_map
)
from game.db.presets.cell_type import cells


@session
async def init_db() -> None:
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    db_cells = [
        await create_cell_type(
            cell.slug, cell.emoji, cell.passable, cell.transparent
        )
        for cell in cells
    ]
    mobs = [
        await create_mob('wolf', '🐺', {db_cells[0]: 10, db_cells[1]: 90}),
        await create_mob('bear', '🐻', {db_cells[0]: 50, db_cells[1]: 10})
    ]
    s.session.add_all(db_cells)
    s.session.add_all(mobs)

    planet = Planet(name='Bandershtat')
    s.session.add(planet)

    continent = Continent(name='def_cont', planet=planet)
    s.session.add(continent)

    test_region = Region(name='def_reg', x=1, y=1, continent=continent)
    await fill_from_emoji_map(test_region, emoji_map)
    s.session.add(test_region)
    ice_region = Region(name='ice_reg', x=1, y=2, continent=continent)
    await fill_from_emoji_map(ice_region, ice_emoji_map)
    s.session.add(ice_region)

    await s.session.flush()

    print('succ')


def configure_logging() -> None:
    root = logging.getLogger()
    fmt = '%(asctime)s %(name)s %(levelname)s: %(message)s'
    try:
        import coloredlogs
        coloredlogs.install(
            level='INFO',
            logger=root,
            fmt=fmt,
        )
    except ModuleNotFoundError:
        pass

    logging.basicConfig(
        level='INFO',
        format=fmt,
        datefmt='%H:%M:%S',
    )


def init_config() -> None:
    config_path = os.environ.get('CONFIG')

    if not config_path:
        raise Exception('Config required')

    with open(config_path) as stream:
        config_content = yaml.safe_load(stream)

    Config.c = Settings.parse_obj(config_content)

    assert Config is not None
