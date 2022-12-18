import csv
from src.mapper import participant_from_dict

data_array = []
with open('names.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        data_array.append(participant_from_dict(id=i, data=row ))

print(data_array)