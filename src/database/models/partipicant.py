import typing as tp
from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.lib import enums

from .base import Base, ReprMixin, TimestampMixin


class ParticipantDatabase(TimestampMixin, Base, ReprMixin):
    __tablename__ = "participants"

    # id: Mapped[int] = mapped_column(
    #     sa.BigInteger, autoincrement=False, primary_key=True
    # )  # tg_id
    number: Mapped[int] = mapped_column(
        sa.Integer, primary_key=True, autoincrement=False, nullable=False
    )
    surname: Mapped[str] = mapped_column(sa.String, nullable=False)  # Ф.и.о
    name: Mapped[str] = mapped_column(sa.String, nullable=True)  # ф.И.о
    patronymic: Mapped[str] = mapped_column(sa.String, nullable=True)  # ф.И.о
    birthday: Mapped[date] = mapped_column(sa.Date, nullable=False)  # Год рождения
    rank: Mapped[enums.Rank] = mapped_column(
        sa.Enum(enums.Rank), nullable=False
    )  # Разряд
    city: Mapped[str] = mapped_column(sa.String, nullable=False)
    team: Mapped[str] = mapped_column(sa.String, nullable=False)  # Команда
    group: Mapped[enums.Group] = mapped_column(
        sa.Enum(enums.Group), nullable=False
    )  # Группа
    couch: Mapped[str] = mapped_column(sa.String, nullable=False)  # Тренер
