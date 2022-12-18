import datetime
import hashlib

from src.models import Participant


def participant_from_dict(id: int, data: dict[str, str]) -> Participant:
    names = data["Ф.И.О."].split(" ")
    return Participant(
        id=id,
        surname=names[0],
        name=names[1],
        patronymic=names[2],
        birthday=datetime.date.fromisoformat(data["Год рождения"]),
        rank=data["Разряд"],
        city=data["Город"],
        team=data["Команда"],
        group=data["Группа"],
        couch=data[
            "Тренер или ответственное лицо Ф.И.О. (обязательно для участников младше 18 лет)"
        ],
    )
