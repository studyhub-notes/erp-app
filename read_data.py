import csv

def read_data():
    data = []
    with open('mess_data.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

