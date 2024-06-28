import csv


def csv_to_dict(file_path):
    data_dict = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data_dict[row['Id']] = row['Link']
    return data_dict