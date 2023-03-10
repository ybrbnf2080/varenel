import datetime

from src.lib.models import Participant, TryFestival


def participant_from_dict(id: int, data: dict[str, str]) -> Participant:
    names = data["Ф.И.О."].split(" ")
    return Participant(
        number=id,
        surname=names[0],
        name=names[1] if 1 < len(names) else "",
        patronymic=names[2] if 2 < len(names) else "",
        birthday=datetime.date.fromisoformat(data["Год рождения"]),
        rank=data["Разряд"],
        city=data["Город"],
        team=data["Команда"],
        group=data["Группа"],
        couch=data[
            "Тренер или ответственное лицо Ф.И.О. (обязательно для участников младше 18 лет)"
        ],
    )


def try_festival_from_dict(id: int, data: dict[str, str]) -> TryFestival:
    return TryFestival(
        participant_number=data["number_участникв"],
        track=data["трасса"],
        result=data["результат"],
        time=data["время"],
    )
