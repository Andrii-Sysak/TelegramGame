from game.db.models import (
    Soul,
    Player
)
from game.db.session import s
from game.db.models.soul import BackgroundCells


async def create_player(id: int, name: str, bgc: BackgroundCells) -> Player:
    soul = Soul(id=id, background_emoji=bgc)
    player = Player(soul=soul, name=name)
    s.session.add(player)

    return player


async def move_player(player: Player, x: int, y: int, region_id: int) -> Player:
    player.x = x
    player.y = y
    player.region_id = region_id
    await s.session.flush()

    return player
