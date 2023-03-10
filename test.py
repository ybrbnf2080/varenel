import asyncio
import csv
import random
from typing import List

import aiohttp
from src.database.repo.track import TrackRepository

from src.database.repo.partipicant import (
    ParticipantRepository,
)
from src.database.repo.result_participant import (
    ResultParticipantRepository,
)
from src.database.repo.try_festival import (
    TryFestivalRepository,
)
from src.lib import enums
from src.lib.config.parser import parse_config
from src.lib.db import session_factory_from_url
from src.lib.mapper import (
    participant_from_dict,
    try_festival_from_dict,
)
from src.lib.models import Participant, Track
from src.service.result_calc import RelsultCalcService


def get_user_from_csv() -> List[Participant]:
    data_array = []
    with open("man.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            data_array.append(participant_from_dict(id=i + 1, data=row))
    print(data_array)
    return data_array


def get_try_from_csv() -> List[Participant]:
    data_array = []
    with open("trys.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            data_array.append(try_festival_from_dict(id=i + 1, data=row))
    print(data_array)
    return data_array


async def create_user_from_csv() -> None:

    config = parse_config()
    session_factory = session_factory_from_url(
        user=config.postgres.user,
        password=config.postgres.password,
        host=config.postgres.host,
        port=config.postgres.port,
        db=config.postgres.db,
    )

    data_users = get_user_from_csv()

    async with session_factory() as session:
        user_service = ParticipantRepository(
            session=session,
        )
        track_service = TrackRepository(
            session=session,
        )
        for data_user in data_users:
            user = await user_service.create(data_user)
        i = 1
        for group in enums.Group:
            for o in range(1, 5):
                await track_service.create(dto=Track(
                    number=i,
                    group=group
                ))
                i += 1


        print("patticlatn created")

        users = await user_service.get_all(offset_type=enums.OffsetType.FIRST)

        # print(users)


DATA_TRY_RESULT = [
    {
        "participant_number": random.randint(1, 13),
        "track": random.randint(1, 5),
        "result": random.randint(1, 35),
        "time": f"00:{random.randint(1, 6)}:00",
    }
    for i in range(0, 200)
]
HOST = "http://localhost:8000"


async def test_web_application() -> None:
    con = aiohttp.ClientSession()

    for data_i in DATA_TRY_RESULT:
        resp = await con.post(
            url=HOST + "/api/v1/try_festivals/",
            json=data_i,
            headers={"Content-Type": "application/json", "X-API-Key": "SosiBibu"},
        )
        # await asyncio.sleep(1)
        print(await resp.json())

    print("\nfestivals GET_ALL\n")
    resp = await con.get(
        url=HOST + "/api/v1/try_festivals/?offset_type=first&offset_id=0&limit=10"
    )
    if resp.ok:
        print("!!!   CONFIM!! ")
    else:
        print(await resp.json())

    print("\nfestivals GET\n")
    resp = await con.get(url=HOST + "/api/v1/try_festivals/13")
    if resp.ok:
        print("!!!   CONFIM!! ")
    else:
        print(await resp.json())
    print("\nfestivals POST\n")
    resp = await con.post(
        url=HOST + "/api/v1/try_festivals/",
        json={"participant_number": 18, "track": 4, "result": 14, "time": "00:8:00"},
        headers={"Content-Type": "application/json", "X-API-Key": "SosiBibu"},
    )
    if resp.ok:
        print("!!!   CONFIM!! ")
    else:
        print(await resp.json())

    print("\nfestivals DELETE\n")
    resp = await con.delete(
        url=HOST + "/api/v1/try_festivals/666",
    )
    if resp.ok:
        print("!!!   CONFIM!! ")
    else:
        print(await resp.json())

    print("\nparticipants GET\n")
    resp = await con.get(
        url=HOST + "/api/v1/participants/?offset_type=first&offset_id=0&limit=888",
    )
    if resp.ok:
        print("!!!   CONFIM!! ")
    else:
        print(await resp.json())

    print("\nParticipant POST\n")
    resp = await con.post(
        url=HOST + "/api/v1/participants/",
        json={
            "id": 0,
            "number": 0,
            "surname": "string",
            "name": "string",
            "patronymic": "string",
            "birthday": "2022-12-22",
            "rank": "?????? ??????????????",
            "city": "string",
            "team": "string",
            "group": "???????????????? 2007-2008 (14,15 ??????)",
            "couch": "string",
        },
        headers={"Content-Type": "application/json", "X-API-Key": "SosiBibu"},
    )
    if resp.ok:
        print("!!!   CONFIM!! ")
    else:
        print(await resp.json())

    print("\nParipicant GET\n")
    resp = await con.get(
        url=HOST + "/api/v1/participants/14",
        headers={"Content-Type": "application/json", "X-API-Key": "SosiBibu"},
    )
    if resp.ok:
        print("!!!   CONFIM!! ")
    else:
        print(await resp.json())

    print("\nresult Participant GET\n")
    resp = await con.get(
        url=HOST
        + "/api/v1/result_participants/?offset_type=first&offset_id=0&limit=10",
        headers={"Content-Type": "application/json", "X-API-Key": "SosiBibu"},
    )
    if resp.ok:
        print("!!!   CONFIM!! ")
    else:
        print(await resp.json())

    print("\nresult Participant GET\n")
    resp = await con.get(
        url=HOST + "/api/v1/result_participants/14",
        headers={"Content-Type": "application/json", "X-API-Key": "SosiBibu"},
    )
    if resp.ok:
        print("!!!   CONFIM!! ")
    else:
        print(await resp.json())

    print("\nResult_participants POST\n")
    resp = await con.post(
        url=HOST + "/api/v1/result_participants/14",
        json={"id": 0, "participant_number": 0, "point": 0},
        headers={"Content-Type": "application/json", "X-API-Key": "SosiBibu"},
    )
    if resp.ok:
        print("!!!   CONFIM!! ")
    else:
        print(await resp.json())

    con.close()


async def test_logic() -> None:

    config = parse_config()
    session_factory = session_factory_from_url(
        user=config.postgres.user,
        password=config.postgres.password,
        host=config.postgres.host,
        port=config.postgres.port,
        db=config.postgres.db,
    )

    async with session_factory() as session:
        participant_repo = ParticipantRepository(
            session=session,
        )
        result_participant_repo = ResultParticipantRepository(
            session=session,
        )
        try_festival_repo = TryFestivalRepository(
            session=session,
        )

        calc_service = RelsultCalcService(
            participant_repo=participant_repo,
            result_participant_repo=result_participant_repo,
            try_festival_repo=try_festival_repo,
        )
        for i in enums.Group:
            result = await calc_service.festival_result_calc(i)
            print(result)


async def test_view() -> None:
    config = parse_config()
    session_factory = session_factory_from_url(
        user=config.postgres.user,
        password=config.postgres.password,
        host=config.postgres.host,
        port=config.postgres.port,
        db=config.postgres.db,
    )

    async with session_factory() as session:
        participant_repo = ParticipantRepository(
            session=session,
        )
        result_participant_repo = ResultParticipantRepository(
            session=session,
        )
        try_festival_repo = TryFestivalRepository(
            session=session,
        )

        calc_service = RelsultCalcService(
            participant_repo=participant_repo,
            result_participant_repo=result_participant_repo,
            try_festival_repo=try_festival_repo,
        )

        for i in enums.Group:
            results = await calc_service.get_result_by_group(i)
            print(f"\n{i.value.upper()}\n")
            print_results(results)


def print_results(results):
    for i in results:

        print(
            f"  {i.order}. [{i.participant_number}] {i.participant.name} {i.participant.surname}  {i.point} {i.total_time}"
        )


async def test():
    # await create_user_from_csv()
    # await test_web_application()
    await test_logic()
    await test_view()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
