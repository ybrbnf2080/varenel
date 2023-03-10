import datetime

import sqlalchemy as sa
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_mixin,
    mapped_column,
)


class Base(DeclarativeBase):
    """Declarative base"""

    pass


@declarative_mixin
class TimestampMixin:
    """Timestamp mixin to have `create_at` & `updated_at` columns."""

    created_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("timezone('utc', now())"),
        default=datetime.datetime.now(datetime.timezone.utc),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("timezone('utc', now())"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )


class ReprMixin:
    """Class for automated `__repr__`"""

    def __repr__(self) -> str:
        return "<{}({})>".format(
            self.__class__.__name__,
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in filter(lambda x: not x.startswith("_"), self.__dict__)
            ),
        )
