import json
import csv
import os
from datetime import datetime


def process_device_file(input_json_file_path, output_csv_file_path, time_format, max_period, real_time: bool = False):
    with open(input_json_file_path, mode='r', encoding='utf-8') as json_file:
        rows = [json.loads(line.strip()) for line in json_file]

    rows.sort(key=lambda row: datetime.strptime(row['timeStamp'], time_format))

    timestamps = [datetime.strptime(row['timeStamp'], time_format) for row in rows]

    differences = [(timestamps[i] - timestamps[i - 1]).total_seconds() for i in range(1, len(timestamps))]

    max_difference = max(differences) if differences else 0

    if real_time:
        periods = differences
    else:
        periods = [diff / max_difference * max_period for diff in differences]
    periods.append(0)

    with open(output_csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = list(rows[0].keys()) + ['sim_period']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for row, period in zip(rows, periods):
            row['sim_period'] = period
            csv_writer.writerow(row)


file_name = 'messages_published.json'
output_file = 'trafego.csv'
dir = 'datasets-test'
real_time = True
os.makedirs(dir, exist_ok=True)
file_path = os.path.join(dir, file_name)
output_file_path = os.path.join(dir, output_file)
time_format = '%Y-%m-%d %H:%M:%S.%f'
max_period = 3600
process_device_file(file_path, output_file_path, time_format, max_period, real_time)
print(f"Periods added in: {os.path.abspath(output_file_path)}")
