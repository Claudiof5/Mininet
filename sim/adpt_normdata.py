import os
import sys
import csv
from datetime import datetime

args = list(sys.argv)
args.pop(0)

def normalize_time(norm):
    if norm == "1/24":
        return 3600 / 86400
    elif norm == "1/1":
        return 1
    elif norm == "1/720":
        return 3600 / 2592000

def convert_to_seconds(time_str):
    time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
    return time.hour * 3600 + time.minute * 60 + time.second

norm_const = normalize_time(args[1])

input_file = args[0]

output_file = 'norm_dataset.csv'
dir = 'datasets-test'
os.makedirs(dir, exist_ok=True)
output_file_path = os.path.join(dir, output_file)
data = []

with open(input_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        row['seconds'] = convert_to_seconds(row['timeStamp'])
        row['normalized'] = row['seconds'] * norm_const
        data.append(row)

sleep_list = []
for i in range(len(data)):
    if i + 1 <= len(data) - 1:
        sleep_value = abs(data[i + 1]['normalized'] - data[i]['normalized'])
        sleep_list.append(sleep_value)
    else:
        sleep_list.append(0)  

for i in range(len(data)):
    data[i]['sleep'] = sleep_list[i]

fieldnames = list(data[0].keys())
with open(output_file_path, mode='w', newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(data)
