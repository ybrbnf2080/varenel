from typing import List, Type, TypeVar

from sqlalchemy import Select

from src.database.models import Base
from src.lib.enums import OffsetType


T = TypeVar("T")


def add_pagination(
    query: Select,
    model: Type[Base],
    offset_type: OffsetType,
    offset_id: int,
    limit: int,
) -> Select:
    """Add pagination to query."""
    statement = query.limit(limit)
    model_id = model.id if hasattr(model, "id") else model.number  # type: ignore

    if offset_type == OffsetType.FIRST:
        statement = statement.order_by(model_id)
    if offset_type == OffsetType.PREV:
        statement = statement.where(model_id <= offset_id).order_by(model_id.desc())
    if offset_type == OffsetType.NEXT:
        statement = statement.where(model_id > offset_id).order_by(model_id)
    if offset_type == OffsetType.SPECIFIC:
        statement = statement.offset(offset_id).order_by(model_id)
    if offset_type == OffsetType.LAST:
        statement = statement.where(model_id <= offset_id).order_by(model_id.desc())

    return statement


def normalize_data(data: List[T], offset_type: OffsetType) -> List[T]:
    """Normalize data to always have ORDER BY id ASC."""
    if offset_type == OffsetType.LAST:
        data.reverse()
    if offset_type == OffsetType.PREV:
        data.reverse()
    return data
