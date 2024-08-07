import json
import os

input_path = 'datasets-test/messages_published.json'
output_path = 'devices.json'
BROKER_IP = '137.135.83.217'

if __name__ == "__main__":
    devices = []
    device_ids = set()

    with open(input_path, mode='r', encoding='utf-8') as json_file:
        name_counter = 1
        ip_counter = 1
        for data in json_file:
            row = json.loads(data.strip())
            device_id = row['devId']
            if device_id not in device_ids:
                device_info = {
                    "environment": row['environment'],
                    "device": row['device'],
                    "devId": row['devId'],
                    "productKey": row['productKey'],
                    "message": row['message'],
                    "sensorType": row['sensorType'],
                    "timeStamp": row['timeStamp'],
                    "name": f"h{name_counter}",
                    "ip": f"10.0.0.{ip_counter}",
                    "broker_ip" : BROKER_IP
                }

                devices.append(device_info)
                device_ids.add(device_id)
                name_counter += 1
                ip_counter += 1

    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(devices, json_file, indent=4)

    print(f"JSON file created at: {os.path.abspath(output_path)}")
