import asyncio
import csv
from typing import List

from src.lib import enums
from src.database.repo.partipicant import ParticipantRepository
from src.lib.config.parser import parse_config
from src.lib.db import session_factory_from_url
from src.lib.mapper import participant_from_dict
from src.lib.models import Participant

def get_user_from_csv() -> List[Participant]:
    data_array = []
    with open('names.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            data_array.append(participant_from_dict(id=i+1, data=row ))
    print(data_array)
    return data_array

async def create_user_from_csv()-> None:

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
        for data_user in data_users :
            user = await user_service.create(data_user)

        print("patticlatn created")

        users = await user_service.get_all(offset_type=enums.OffsetType.FIRST)
        
        # print(users)



async def test():
    await create_user_from_csv()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
