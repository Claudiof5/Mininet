import paho.mqtt.client as mqtt
import argparse
import json

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def publish_message(broker, port, topic, message):
    client = mqtt.Client()
    client.connect(broker, port, 60)
    client.publish(topic, message)
    client.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MQTT Publisher')
    parser.add_argument('--broker', type=str, required=True, help='MQTT broker address')
    parser.add_argument('--port', type=int, required=True, help='MQTT broker port')
    parser.add_argument('--topic', type=str, required=True, help='MQTT topic')
    parser.add_argument('--method', type=str, required=True, help='Method for the message')
    parser.add_argument('--sensor', type=str, required=True, help='Sensor type for the message')
    parser.add_argument('--collect', type=int, required=True, help='Collect time')
    parser.add_argument('--publish', type=int, required=True, help='Publish time')

    args = parser.parse_args()

    message = {
        "method": args.method,
        "sensor": args.sensor,
        "time": {
            "collect": args.collect,
            "publish": args.publish
        }
    }

    publish_message(args.broker, args.port, args.topic, json.dumps(message))
