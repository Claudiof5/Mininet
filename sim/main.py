import logging
import paho.mqtt.client as mqtt
import argparse
from time import sleep

parser = argparse.ArgumentParser(description='Params sensors')
parser.add_argument('--name', default='SALA_AR_CONDICIONADO-002')
parser.add_argument('--space', default='SALA')
parser.add_argument('--broker', default='137.135.83.217')
parser.add_argument('--port', default=1883)

args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()

def on_connect(client, userdata, flags, reason_code, properties):
    topic = '/dev/' + userdata["space"] + "/" + userdata["deviceName"]
    client.subscribe(topic)
    logger.info(f"Topic device subscribed: {topic}")

def on_message(client, userdata, message):
    logger.info(message.topic)
    logger.info(message.payload)

def on_disconnect(client, userdata, reason_code, properties):
    logger.info("disconnected!")
    exit()

while True:
    data = {
        "deviceName": args.name,
        "mqttBroker": args.broker,
        "mqttPort": args.port,
        "space": args.space
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
    sub_client.on_disconnect = on_disconnect

    try:
        sub_client.connect(mqttBroker, mqttPort, 60)
        sub_client.loop_forever()
    except Exception as e:
        logger.error(f"Broker unreachable on {mqttBroker} URL! Exception: {e}")
        sleep(5)
