import csv
import json

csv_file = 'test_TCA.csv'
csv_data = {}
with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        csv_data[row['reaction']] = float(row['value'])


related_data_file = 'all_csv_data.json'
with open(related_data_file, mode='w') as file:
    json.dump([csv_data], file, indent=4)

