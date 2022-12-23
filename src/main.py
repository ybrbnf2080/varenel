import csv
from typing import List
from src.lib.mapper import participant_from_dict, try_festival_from_dict
from src.lib.models import Participant


def get_user_from_csv() -> List[Participant]:
    data_array = []
    with open("names.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            data_array.append(participant_from_dict(id=i + 1, data=row))
    print(data_array)
    return data_array

def get_try_festival_from_csv() -> List[Participant]:
    data_array = []
    with open("trys.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            data_array.append(try_festival_from_dict(id=i + 1, data=row))
    print(data_array)
    return data_array


if __name__ == "__main__":
    pass
