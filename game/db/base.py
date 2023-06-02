from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from game.db.types import str50


class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        str50: String(50)
    }
