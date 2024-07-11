import logging
import paho.mqtt.client as mqtt
import argparse
from time import time, sleep
from pandas import DataFrame

parser = argparse.ArgumentParser(description='Params sensors')

parser.add_argument('--broker'  , default='192.168.56.105')
parser.add_argument('--port'    , type=int, default=1883)
parser.add_argument('--nmensagens', type=int, default=1000)
parser.add_argument('--frequencia', type=int, default=4)

args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()

topico_devices = "env1234541/devices"

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(topico_devices)
    
    if userdata["logging"]:
        logger.info(f"Topic device subscribed: {topico_devices}")
    message = f"STARTSRT {args.nmensagens} {args.frequencia}"
    userdata["start_time"] = publish_message(client, topico_devices, message)

def on_message(client, userdata, message):
   
    payload_list = message.payload.decode('utf-8').split(" ")
    

    if payload_list[0] == "SRT":
       publish_message(client, topico_devices, f"SRTR {payload_list[1]}")
       userdata["counter"] += 1
       
    if userdata["counter"] == args.nmensagens:
        client.disconnect()

def on_publish(client, userdata, mid, reason_code, properties):
    pass

def publish_message(client, topic, message):
    result = client.publish(topic, message)
    if result.rc != mqtt.MQTT_ERR_SUCCESS and userdata["logging"]:
        print(f"Failed to publish message to {topic}: {mqtt.error_string(result.rc)}")


def server_response_test(logging: bool):
    data = {
        "mqttBroker": args.broker,
        "mqttPort": args.port,
        "logging": False,
        "counter": 0
    }

    mqttBroker = args.broker
    mqttPort = data["mqttPort"]
    mqttUsername = ""
    mqttPassword = ""

    sub_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    sub_client.username_pw_set(mqttUsername, mqttPassword)
    sub_client.user_data_set(data)
    sub_client.on_connect = on_connect
    sub_client.on_message = on_message
    sub_client.on_publish = on_publish

    try:
        sub_client.connect(mqttBroker, mqttPort, 60)
        sub_client.loop_forever()
    except Exception as e:
        logger.error(f"Broker unreachable on {mqttBroker} URL! Exception: {e}")

    
if __name__ == "__main__":

    server_response_test(False)
