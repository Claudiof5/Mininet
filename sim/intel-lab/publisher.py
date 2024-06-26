import csv
import os
import time
import paho.mqtt.client as mqtt
import argparse
import json

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Connected with result code {rc}")
    else:
        print(f"Failed to connect, return code {rc}")

def publish_message(client, topic, message):
    client.publish(topic, message)

def connect_with_retry(client, broker, port, retries=5, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            client.connect(broker, port, 60)
            return True
        except Exception as e:
            print(f"Connection attempt {attempt+1}/{retries} failed: {e}")
            time.sleep(delay)
            attempt += 1
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MQTT Publisher')
    parser.add_argument('--name', type=str, default="sc01", help='Sensor name')
    parser.add_argument('--broker', type=str, default="137.135.83.217", help='MQTT broker address')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')
    parser.add_argument('--topic', type=str, default="dev/sc01", help='MQTT topic')
    parser.add_argument('--publish', type=int, default=10, help='Publish time')

    args = parser.parse_args()
    csv_file_path = os.path.join('datasets-test', f'{args.name}.csv')

    if not os.path.exists(csv_file_path):
        print(f"CSV file for sensor {args.name} does not exist.")
        exit(1)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect

    if connect_with_retry(client, args.broker, args.port):
        client.loop_start()

        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                message = {
                    "date_time": row["date_time"],
                    "epoch": row["epoch"],
                    "moteid": row["moteid"],
                    "temperature": row["temperature"],
                    "humidity": row["humidity"],
                    "light": row["light"],
                    "voltage": row["voltage"]
                }
                publish_message(client, args.topic, json.dumps(message))
                time.sleep(args.publish)

        client.loop_stop()
        client.disconnect()
    else:
        print("Failed to connect to the MQTT broker after multiple attempts.")