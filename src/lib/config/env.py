import datetime
import decimal
import enum
import fractions
import ipaddress
import os
import pathlib
import re
import uuid
from typing import (
    FrozenSet,
    List,
    Set,
    Tuple,
    Type,
    TypeVar,
)


E = TypeVar("E", bound=Type[enum.Enum])
T = TypeVar("T")


def int_(key: str) -> int:
    return int(os.environ[key])


def float_(key: str) -> float:
    return float(os.environ[key])


def decimal_(key: str) -> decimal.Decimal:
    return decimal.Decimal(os.environ[key])


def complex_(key: str) -> complex:
    return complex(os.environ[key])


def fraction_(key: str) -> fractions.Fraction:
    return fractions.Fraction(os.environ[key])


def bool_(key: str) -> bool:
    if os.environ[key] in {"True", "true", "1"}:
        return True
    elif os.environ[key] in {"False", "false", "0"}:
        return False
    raise ValueError(f"'{key}' is not a valid boolean")


def str_(key: str) -> str:
    return str(os.environ[key])


def bytes_(key: str) -> bytes:
    return bytes(os.environ[key], encoding="utf-8")


def bytearray_(key: str) -> bytearray:
    return bytearray(os.environ[key], encoding="utf-8")


def memoryview_(key: str) -> memoryview:
    return memoryview(os.environ[key])


def list_(key: str, cast: Type[T]) -> List[T]:
    return [cast(v) for v in re.split(r"[, ]", string=os.environ[key]) if v]


def tuple_(key: str, cast: Type[T]) -> Tuple[T, ...]:
    return tuple([cast(v) for v in re.split(r"[, ]", string=os.environ[key]) if v])


def set_(key: str, cast: Type[T]) -> Set[T]:
    return set([cast(v) for v in re.split(r"[, ]", string=os.environ[key]) if v])


def frozenset_(key: str, cast: Type[T]) -> FrozenSet[T]:
    return frozenset([cast(v) for v in re.split(r"[, ]", string=os.environ[key]) if v])


def path_(key: str) -> pathlib.Path:
    return pathlib.Path(os.environ[key])


def datetime_(key: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(os.environ[key])


def uuid_(key: str) -> uuid.UUID:
    return uuid.UUID(os.environ[key])


def ipv4address_(key: str) -> ipaddress.IPv4Address:
    return ipaddress.IPv4Address(os.environ[key])


def ipv6address_(key: str) -> ipaddress.IPv6Address:
    return ipaddress.IPv6Address(os.environ[key])


def enum_(key: str, cast: Type[E]) -> E:
    return cast(os.environ[key])


def value(key: str, cast: Type[T]) -> T:
    if cast == bool:
        return bool_(key)
    return cast(os.environ[key])


def container_value(key: str, container_type, item_type):
    return container_type(
        [item_type(v) for v in re.split(r"[, ]", string=os.environ[key]) if v]
    )
