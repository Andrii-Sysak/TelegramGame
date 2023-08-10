from game.db.presets.base import CellType

empty = CellType(slug='empty', emoji='⬜', permeability=5)
rock = CellType(slug='rock', emoji='🪨', permeability=100)
portal = CellType(slug='portal', emoji='⭕', permeability=50)
plains = CellType(slug='plains', emoji='🦗', permeability=30, transparent=True)
ice = CellType(slug='ice', emoji='🧊', permeability=100)

cells = (empty, rock, portal, plains, ice)
