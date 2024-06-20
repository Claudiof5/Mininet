import paho.mqtt.client as mqtt
import json
import tatu
import argparse
from time import sleep

parser = argparse.ArgumentParser(description='Params sensors')
parser.add_argument('--name', action='store', dest='name', default='sc01')
parser.add_argument('--broker', action='store', dest='broker', default='91.121.93.94')
args = parser.parse_args()

# You don't need to change this file. Just change sensors.py and config.json

def on_connect(mqttc, obj, flags, rc):
    topic = obj["topicPrefix"] + 'sub/'+ obj["deviceName"]
    mqttc.subscribe(topic)
    print("Device's sensors:")
    for sensor in obj['sensors']:
        print("\t" + sensor['name'])
    print("Topic device subscribed: " + topic)

def on_message(mqttc, obj, msg):
    print("msg " + msg.topic)
    print(msg)
    if obj["topicPrefix"] in msg.topic:
        tatu.main(obj, msg)

def on_disconnect(mqttc, obj, rc):
    #print(str(obj))
    print("disconnected!")
    exit()

while True:
    with open('config.json') as f:
        data = json.load(f)
    data["deviceName"] = args.name
    data["mqttBroker"] = args.broker
    data["dataset"] = True
    mqttBroker = args.broker
    mqttPort = data["mqttPort"]
    mqttUsername = data["mqttUsername"]
    mqttPassword = data["mqttPassword"]
    deviceName = data["deviceName"]

    sub_client = mqtt.Client()
    sub_client.username_pw_set(mqttUsername, mqttPassword)
    sub_client.user_data_set(data)
    sub_client.on_connect = on_connect
    sub_client.on_message = on_message
    sub_client.on_disconnect = on_disconnect

    try:
        sub_client.connect(mqttBroker, int(mqttPort), 60)
        sub_client.loop_forever()
    except:
        print("Broker unreachable on " + mqttBroker + " URL!")
        sleep(5)
