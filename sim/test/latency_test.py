import logging
import paho.mqtt.client as mqtt
import argparse
from time import time, sleep
from pandas import DataFrame

parser = argparse.ArgumentParser(description='Params sensors')

parser.add_argument('--broker'  , default='192.168.56.105')
parser.add_argument('--port'    , type=int, default=1883)
parser.add_argument('--ndevices', type=int, default=6)
parser.add_argument('--ntest', type=int, default=100)

args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()

topico_devices = "env1234541/devices"

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(topico_devices)
    
    if userdata["logging"]:
        logger.info(f"Topic device subscribed: {topico_devices}")

    userdata["start_time"] = publish_message(client, topico_devices, "PING")

def on_message(client, userdata, message):
    arrival_time = time()
    start_time = userdata["start_time"]
    payload_str = message.payload.decode('utf-8')
    
    message_list = payload_str.split(" ")
    
    if  message_list[-1] == "PING" and len(message_list) == 2:
        if userdata["logging"]:
            logger.info(f"{message_list[0]} response time: {arrival_time-start_time}")
        userdata["ping_response"][message_list[0]] = (arrival_time - start_time)
        userdata["counter"] += 1
    
    if userdata["counter"] == userdata["ndevices"]:
        client.disconnect()

def on_publish(client, userdata, mid, reason_code, properties):
    pass

def publish_message(client, topic, message):
    start_time = time()
    result = client.publish(topic, message)
    if result.rc != mqtt.MQTT_ERR_SUCCESS and userdata["logging"]:
        print(f"Failed to publish message to {topic}: {mqtt.error_string(result.rc)}")
    return start_time

def latency_test(logging: bool):
    data = {
        "mqttBroker": args.broker,
        "mqttPort": args.port,
        "ndevices": args.ndevices,
        "ping_response": { f"h{i}": -1 for i in range(1, args.ndevices+1) },
        "counter": 0,
        "start_time": 0,
        "logging": logging
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
        
    return data["ping_response"]
    
if __name__ == "__main__":

    tempos_de_resposta = {f"h{i}":{"lista":[]} for i in range(1, args.ndevices+1)}
    for i in range( args.ntest):
    
        result = latency_test(True)
        for key in result.keys():
            tempos_de_resposta[key]["lista"].append(result[key])
    
    for key in tempos_de_resposta.keys():
        tempos_de_resposta[key]["min"] = min(tempos_de_resposta[key]["lista"])
        tempos_de_resposta[key]["max"] = max(tempos_de_resposta[key]["lista"])
        tempos_de_resposta[key]["mean"] = sum(tempos_de_resposta[key]["lista"])/len(tempos_de_resposta[key]["lista"])
        
    df = DataFrame.from_dict(tempos_de_resposta, orient="index")
    filename = f"result_{args.ndevices}devices_{args.ntest}repeticions.csv"
    df.to_csv(filename, index=True)
