from datetime import date, timedelta

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, ReprMixin, TimestampMixin


class TryFestivalDatabase(TimestampMixin, Base, ReprMixin):
    __tablename__ = "trys_festival"

    id: Mapped[int] = mapped_column(
        sa.BigInteger, autoincrement=True, primary_key=True
    )  # id
    participant_number: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("participants.number", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )  # id_участникв
    track: Mapped[int] = mapped_column(sa.Integer, nullable=False)  # трасса
    result: Mapped[float] = mapped_column(sa.Float, nullable=False)  # результат
    time: Mapped[timedelta] = mapped_column(sa.Interval, nullable=False)  # время
