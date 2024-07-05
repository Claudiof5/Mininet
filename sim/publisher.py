import csv
import os
import time
import paho.mqtt.client as mqtt
import argparse

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Connected with result code {rc}")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid, reason_code, properties):
    pass

def publish_message(client, topic, message):
    result = client.publish(topic, message)
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Failed to publish message to {topic}: {mqtt.error_string(result.rc)}")

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
    parser.add_argument('--df', type=str, default="trafego.csv", help='Dataset de tráfego')
    parser.add_argument('--broker', type=str, default="137.135.83.217", help='MQTT broker address')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')

    args = parser.parse_args()
    csv_file_path = os.path.join('datasets-test', f'{args.df}')

    if not os.path.exists(csv_file_path):
        print(f"CSV file for sensor {csv_file_path} does not exist.")
        exit(1)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.enable_logger()  
    
    if connect_with_retry(client, args.broker, args.port):
        client.loop_start()

        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                message = row['message']
                topic = f"/devices"
                publish_message(client, topic, message)
                sleep_duration = float(row['sim_period'])
                time.sleep(sleep_duration)
                
        client.loop_stop()
        client.disconnect()
    else:
        print("Failed to connect to the MQTT broker after multiple attempts.")
