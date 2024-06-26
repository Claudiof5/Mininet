import csv
import json
import os
import re

file_path = '../datasets-test/data.txt'
json_file_path = 'devices.json'
BROKER_IP = '137.135.83.217'

if __name__ == "__main__":
    moteid_limit = 54
    devices = []
    device_ids = set()
    with open(file_path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()

        name_counter = 1
        ip_counter = 1

        for line in lines:
            parts = re.split(r'\s+', line.strip())
            if len(parts) < 8:
                parts += [None] * (8 - len(parts))
            moteid = int(parts[3]) if parts[3] is not None else None

            if moteid is None or moteid > moteid_limit: 
                continue
            
            if moteid not in device_ids:
                device_info = {
                    "name_iot": f'sc{name_counter:02d}',
                    "type": 'sensor',
                    "name": f"h{name_counter}",
                    "ip": f"10.0.0.{ip_counter}",
                    "broker_ip" : BROKER_IP
                }
                
                devices.append(device_info)
                device_ids.add(moteid)
                name_counter += 1
                ip_counter += 1

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(devices, json_file, indent=4)

    print(f"JSON file created at: {os.path.abspath(json_file_path)}")
