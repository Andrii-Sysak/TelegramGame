from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CellType:
    slug: str
    emoji: str
    passable: bool = False
    transparent: bool = False
