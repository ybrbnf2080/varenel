import typing as tp
from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.lib import enums

from .base import Base, ReprMixin, TimestampMixin


if tp.TYPE_CHECKING:
    from .result_participant import (
        ResultParticipantDatabase,
    )


class TrackDatabase(TimestampMixin, Base, ReprMixin):
    __tablename__ = "tracks"

    # id: Mapped[int] = mapped_column(
    #     sa.BigInteger, autoincrement=False, primary_key=True
    # )  # tg_id
    number: Mapped[int] = mapped_column(
        sa.Integer, primary_key=True, autoincrement=False, nullable=False
    )
    color: Mapped[str] = mapped_column(sa.String, nullable=True)  # ф.И.о
    group: Mapped[enums.Group] = mapped_column(sa.Enum(enums.Group), nullable=False)
    # rank: Mapped[enums.Rank] = mapped_column( TODO add category track
    #     sa.Enum(enums.Rank), nullable=True
    # )  # Разряд
