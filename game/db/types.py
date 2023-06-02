from typing import Annotated

from sqlalchemy.orm import mapped_column


str50 = Annotated[str, 50]
intpk = Annotated[int, mapped_column(primary_key=True, init=False)]
