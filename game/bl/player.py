import asyncio
from datetime import (
    datetime,
    timedelta,
)

from sqlalchemy import delete

from game.config import Config
from game.db.models import (
    Player,
    Soul,
)
from game.db.models.action import Action
from game.db.session import s
from game.utils.delay import delay


async def create_player(id: int, name: str, bgc: str) -> Player:
    soul = Soul(id=id, background_emoji=bgc)
    player = Player(soul=soul, name=name)
    s.session.add(player)

    return player


async def move_player(player: Player, x: int, y: int, region_id: int) -> Player:
    action = Action(
        player_id=player.id,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(
            seconds=Config.c.durations.movement
        )
    )
    s.session.add(action)
    player.x = x
    player.y = y
    player.region_id = region_id
    await s.session.flush()

    t = asyncio.create_task(delay(
        s.session.execute(delete(Action).where(Action.id == action.id)),
        Config.c.durations.movement
    ))

    return player
