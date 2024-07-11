import logging
import paho.mqtt.client as mqtt
import argparse
from time import time, sleep
from random import expovariate
import csv
import threading

parser = argparse.ArgumentParser(description='Params sensors')
parser.add_argument('--name', default='SALA_AR_CONDICIONADO-002')
parser.add_argument('--space', default='SALA')
parser.add_argument('--broker', default='137.135.83.217')
parser.add_argument('--port', default=1883)

args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()

topico_devices = "env1234541/devices"
sent_and_arrival_time = {}
def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(topico_devices)
    logger.info(f"Topic device subscribed: {topico_devices}")

def on_message(client, userdata, message):
    
    payload_list = message.payload.decode('utf-8').split(" ")
    
    if payload_list[0] == "PING" and len(payload_list) == 1:
    	publish_message(client, topico_devices, userdata["deviceName"]+" PING")
    elif payload_list[0] == "SRTR":
        logger.info(payload_list)
        
        capture_response_time(payload_list[1])
        
        
    elif payload_list[0] == "STARTSRT":
        start_server_response_time_test(client, int(payload_list[1]), int(payload_list[2]))
 

def on_disconnect(client, userdata, reason_code, properties):
    logger.info("disconnected!")
    exit()

def on_publish(client, userdata, mid, reason_code, properties):
    pass
    
def publish_message(client, topic, message):
    result = client.publish(topic, message)
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Failed to publish message to {topic}: {mqtt.error_string(result.rc)}")
        
def start_server_response_time_test(client, nMessages, messages_per_second):
    global sent_and_arrival_time
    def run():
        for i in range(nMessages):
            start_time = time()
            publish_message(client, topico_devices, f"SRT {i}")
            sent_and_arrival_time[i] = { "start_time":start_time }
            sleep(expovariate(messages_per_second))
        while "arrival_time" not in sent_and_arrival_time[nMessages-1]:
            sleep(1)
        
        #df = DataFrame.from_dict(sent_and_arrival_time, orient="index")
        #filename = f"response_time_result_{messages_per_second}messages/s_{nMessages}messages.csv"
        #df.to_csv(filename, index=True)
        
        header = set()
        for subdict in sent_and_arrival_time.values():
            header.update(subdict.keys())
        header = sorted(header)
        
        with open( filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["key"] + header)
            
        for key, subdict in sent_and_arrival_time.items():
            row = [key] + [subdict.get(col, " ") for col in header]
            writer.writerow(row)
        
    thread = threading.Thread(target=(run))
    thread.start()
    
def capture_response_time(index):
    global sent_and_arrival_time
    arrival_time = time()
    sent_and_arrival_time[index]["arrival_time"] = arrival_time
    
    logger.info(f"index : {sent_and_arrival_time[index]}")

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
    sub_client.on_publish = on_publish
    sub_client.on_disconnect = on_disconnect

    try:
        sub_client.connect(mqttBroker, mqttPort, 60)
        sub_client.loop_forever()
    except Exception as e:
        logger.error(f"Broker unreachable on {mqttBroker} URL! Exception: {e}")
        sleep(5)
