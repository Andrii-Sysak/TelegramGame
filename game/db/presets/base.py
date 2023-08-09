from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CellType:
    slug: str
    emoji: str
    permeability: int = 50
    transparent: bool = False
