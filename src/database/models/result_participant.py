import typing as tp

import sqlalchemy as sa
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base, ReprMixin, TimestampMixin


if tp.TYPE_CHECKING:
    from .partipicant import ParticipantDatabase


class ResultParticipantDatabase(TimestampMixin, Base, ReprMixin):
    __tablename__ = "results_participant"

    id: Mapped[int] = mapped_column(
        sa.BigInteger, autoincrement=True, primary_key=True
    )  # id
    participant_number: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("participants.number", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )  # id_участникв
    point: Mapped[float] = mapped_column(sa.Float, nullable=False)

    # M2O relationship
    participant: Mapped[tp.Optional["ParticipantDatabase"]] = relationship(
        argument="ParticipantDatabase",
        back_populates="results",
        uselist=False,
    )
