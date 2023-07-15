import logging
import os

import yaml

from game.bl.cell import create_cell_type
from game.bl.region import fill_from_emoji_map
from game.config import (
    Config,
    Settings,
)
from game.db.models import Player, Region
from game.db import Base
from game.db.session import eng, session, s
from game.presets.test_region import emoji_map, ice_emoji_map


@session
async def init_db():
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    cells = [
        await create_cell_type('empty', '⬜', True),
        await create_cell_type('rock', '🪨', False),
        await create_cell_type('portal', '⭕', True),
        await create_cell_type('ice', '🧊', False),
        await create_cell_type('sauron_eye', '⭕', False)
    ]
    s.session.add_all(cells)
    await s.session.flush()

    test_region = Region(name='test', x=1, y=1)
    await fill_from_emoji_map(test_region, emoji_map)
    s.session.add(test_region)

    ice_region = Region(name='test', x=1, y=2)
    await fill_from_emoji_map(ice_region, ice_emoji_map)
    s.session.add(ice_region)

    print('succ')


def configure_logging():
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

    with open(config_path) as stream:
        config_content = yaml.safe_load(stream)

    Config.c = Settings.parse_obj(config_content)

    assert Config is not None
