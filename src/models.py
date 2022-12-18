from datetime import date

from pydantic import BaseModel

from src import enums


class Participant(BaseModel):
    id: int
    surname: str  # Ф.и.о
    name: str = None  # ф.И.о
    patronymic: str = None  # ф.и.О
    birthday: date  # Год рождения
    rank: enums.Rank  # Разряд
    city: str
    team: str  # Команда
    group: str  # Группа
    couch: str  # Тренер или ответственное лицо Ф.И.О. (обязательно для участников младше 18 лет)
