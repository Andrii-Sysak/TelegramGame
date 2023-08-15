from dataclasses import dataclass
from typing import Any

@dataclass(slots=True, frozen=True)
class CellType:
    slug: str
    emoji: str
    permeability: int = 50
    transparent: bool = False


@dataclass(slots=True, frozen=True)
class UniqueCell:
    slug: str
    properties: dict[str, Any]
