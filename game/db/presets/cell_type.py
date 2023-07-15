from game.db.presets.base import CellType

empty = CellType(slug='empty', emoji='⬜', passable=True)
rock = CellType(slug='rock', emoji='🪨')
portal = CellType(slug='portal', emoji='⭕', passable=True)
plains = CellType(slug='plains', emoji='🦗', passable=True, transparent=True)
ice = CellType(slug='ice', emoji='🧊', passable=True)

cells = (empty, rock, portal, plains, ice)
