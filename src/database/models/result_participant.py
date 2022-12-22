import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, ReprMixin, TimestampMixin


class ResultParticipantDatabase(TimestampMixin, Base, ReprMixin):
    __tablename__ = "results_participant"

    id: Mapped[int] = mapped_column(
        sa.BigInteger, autoincrement=True, primary_key=True
    )  # id
    participant_number: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("participants.number", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )  # id_участникв
    point: Mapped[float] = mapped_column(sa.Float, nullable=False)
