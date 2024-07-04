import csv
import json
import os

csv_file_path = 'datasets-test/Cenario_argus1usuario.csv'
json_file_path = 'devices.json'
BROKER_IP = '137.135.83.217'

if __name__ == "__main__":
    devices = []
    device_ids = set()
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        name_counter = 1
        ip_counter = 1

        for row in csv_reader:
            device_id = row['devId']
            if device_id not in device_ids:
                device_info = {
                    "name_iot": row['device'],
                    "devId": row['devId'],
                    "type": row['sensorType'],
                    "productKey": row['productKey'],
                    "space": row['space'],
                    "name": f"h{name_counter}",
                    "ip": f"10.0.0.{ip_counter}",
                    "broker_ip" : BROKER_IP
                }
                
                devices.append(device_info)
                device_ids.add(device_id)
                name_counter += 1
                ip_counter += 1

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(devices, json_file, indent=4)

    print(f"JSON file created at: {os.path.abspath(json_file_path)}")


