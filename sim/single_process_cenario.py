import json
import csv
import os
from datetime import datetime


def process_json_file(input_json_file_path, output_csv_file_path, time_format):
    with open(input_json_file_path, mode='r', encoding='utf-8') as json_file:
        rows = [json.loads(line.strip()) for line in json_file]

    rows.sort(key=lambda row: datetime.strptime(row['timeStamp'], time_format))

    with open(output_csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = list(rows[0].keys())
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for row in rows:
            csv_writer.writerow(row)   

file_name = 'messages_published.json'
output_file = 'trafego.csv'
dir = 'datasets-test'
os.makedirs(dir, exist_ok=True)
file_path = os.path.join(dir, file_name)
output_file_path = os.path.join(dir, output_file)
time_format = '%Y-%m-%d %H:%M:%S.%f'
process_json_file(file_path, output_file_path, time_format)
print(f"File created in: {os.path.abspath(output_file_path)}")
