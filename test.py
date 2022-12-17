import csv
with open('names.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if "мальчики" in row["Группа"]:
            print(row['Ф.И.О.'])


