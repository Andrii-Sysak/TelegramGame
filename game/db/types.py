from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column


str50 = Annotated[str, 50]


int_pk = Annotated[int, mapped_column(primary_key=True, init=False)]

region_fk = Annotated[int, mapped_column(
    ForeignKey('region.id', ondelete='CASCADE')
)]
cell_type_fk = Annotated[int, mapped_column(
    ForeignKey('cell_type.slug', ondelete='CASCADE')
)]
soul_fk = Annotated[int, mapped_column(
    ForeignKey('soul.id', ondelete='CASCADE')
)]
player_fk = Annotated[int, mapped_column(
    ForeignKey('player.id', ondelete='CASCADE')
)]
mob_fk = Annotated[int, mapped_column(
    ForeignKey('mob.id', ondelete='CASCADE')
)]
