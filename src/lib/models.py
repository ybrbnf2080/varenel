from datetime import date, time, timedelta
from typing import Optional

from pydantic import BaseModel

from src.lib import enums


class Participant(BaseModel):
    id: Optional[int] = None
    number: int
    surname: str  # Ф.и.о
    name: str = None  # ф.И.о
    patronymic: str = None  # ф.и.О
    birthday: date  # Год рождения
    rank: enums.Rank  # Разряд
    city: str  # Город
    team: str  # Команда
    group: enums.Group  # Группа
    couch: str  # Тренер или ответственное лицо Ф.И.О. (обязательно для участников младше 18 лет)

    class Config:
        orm_mode = True


class TryFestival(BaseModel):
    id: Optional[int] = None
    participant_number: int  # number_участникв
    track: int  # трасса
    result: float  # результат
    time: timedelta  # время

    class Config:
        orm_mode = True


class Track(BaseModel):
    number: int  # number_участникв
    color: Optional[str] = None
    group: enums.Group

    class Config:
        orm_mode = True


class ResultParticipant(BaseModel):
    id: Optional[int] = None
    participant_number: int  # number_участникв
    point: float
    total_time: timedelta

    class Config:
        orm_mode = True


class SuperResultParticipant(ResultParticipant):
    participant: Optional[Participant] = None
    order: Optional[int] = None

    class Config:
        orm_mode = True
