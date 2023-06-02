from game.db.models import Player
from game.db.session import s


async def create_player(id: int, name: str, bgc: str) -> Player:
    player = Player(telegram_id=id, name=name, background_emoji=bgc)
    s.session.add(player)

    return player
