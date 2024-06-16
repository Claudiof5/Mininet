import time
import threading
from mininet.log import info
import paho.mqtt.client as mqtt
from VARIAVEIS import *
from typing import Dict, List

class MQTTServer:
    def __init__(self, name, ip, broker_ip, broker_port, topics = []):
        
        
        self.name = name
        self.ip = ip
        self.broker_ip = broker_ip
        self.mqtt_port = broker_port

        self.config_topic = TOPICO_DE_CONFIGURAR_PADRAO
        self.standard_topic = TOPICO_PADRAO
        self.command_sulfix = SULFIXO_DE_COMANDO

        self.all_topics = [self.config_topic, self.standard_topic]
        self.all_topics.extend(topics)
        self.connected_devices: Dict[str, List[Dict[str, str]]] = {}
        self.mqtt_client = None
        

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected with result code {rc}")

    def on_message(self, mqttc, obj, msg: mqtt.MQTTMessage):
        
        payload_str = msg.payload.decode('utf-8')
        print(msg.topic + " " + str(msg.qos) + " " + str(payload_str))

        if msg.topic == self.config_topic:
            self.handle_new_connection(payload_str)
        else:
            self.log_message(payload_str)

    def on_subscribe(self, mqttc, obj, mid, reason_code_list, properties):
        print("Subscribed: " + str(mid) + " " + str(reason_code_list))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def start_mqtt_client(self):
        self.mqtt_client               = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.on_message    = self.on_message
        self.mqtt_client.on_connect    = self.on_connect
        self.mqtt_client.on_subscribe  = self.on_subscribe
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_log        = self.on_log

        self.mqtt_client.connect( self.broker_ip, self.mqtt_port)
        print(self.all_topics)
        for topic in self.all_topics:
            
            self.subscribe_to_topic(topic)
            
    def subscribe_to_topic(self, topic):
        try:
            self.mqtt_client.subscribe(topic)
        except Exception as e:
            print(f"Error subscribing to {topic}: {str(e)}\n")

    def handle_new_connection(self, msg:str):
        msg_list = msg.split(" ")

        msg_sender_name = msg_list[MESSAGE_STRUCTURE.src_device_index]
        msg_type        = msg_list[MESSAGE_STRUCTURE.msg_type_index]
        msg_params      = msg_list[MESSAGE_STRUCTURE.msg_params_start_index]

        if msg_type == MESSAGES.first_connection.code:
            device_type = msg_params[0]
            if device_type not in self.connected_devices.keys():
                self.connected_devices[device_type] = [f"{device_type}-0"]
            else:
                n_devices = len(self.connected_devices[device_type])
                
                nome = f"{device_type}-{str(n_devices)}"
                topico = self.standard_topic
                self.connected_devices[device_type][nome] = topico
                command_topic =  self.config_topic + self.command_sulfix

                self.send_command_chage_device_name( command_topic, msg_sender_name, nome)
                time.sleep(1)
                self.send_command_change_device_pub_topic( command_topic, nome, self.standard_topic)
                time.sleep(1)
                self.send_command_change_device_comm_topic( command_topic, nome, self.standard_topic+self.command_sulfix)
                time.sleep(1)


    def change_device_name(self, device:str, new_name ):
        
        device_list = device.split("-")
        device_type = device_list[0]
        device_name = device_list[1]

        new_name = f"{device_type}-{new_name}"

        topic = self.connected_devices[device_type][device_name]
        self.connected_devices[device_type][new_name] = topic

        del self.connected_devices[device_type][device]

        self.send_command_chage_device_name( topic, device, new_name)


    def change_device_topic(self, device, new_topic):
        
        device_list = device.split("-")
        device_type = device_list[0]
        device_name = device_list[1]

        topic = self.connected_devices[device_type][device_name]
        self.connected_devices[device_type][device] = new_topic
        
        new_command_topic = new_topic + self.command_sulfix

        self.send_command_change_device_pub_topic( topic, device, new_topic)
        self.send_command_change_device_comm_topic( topic, device, new_command_topic)




    def send_command_chage_device_name( self, topic, device, device_new_name):
        command_modify_name  = f"{device} {COMMANDS.change_name.code} {device_new_name}"
        self.send_message( topic, command_modify_name )

    def send_command_change_device_pub_topic( self, topic, device, new_topic):
        command_modify_pub_topic  = f"{device} {COMMANDS.modify_publishing_topic.code} {new_topic}"
        self.send_message( topic, command_modify_pub_topic )

    
    def send_command_change_device_comm_topic( self, topic, device, new_topic):
        command_modify_comm_topic  = f"{device} {COMMANDS.modify_command_topic.code} {new_topic}"
        self.send_message( topic, command_modify_comm_topic )


    def send_message(self, topic, message):
        try:
            info(f"sending messages on topic {topic}")
            self.mqtt_client.publish(topic, message)
        except Exception as e:
            info(f"Error sending message to {topic}: {str(e)}\n")


    def subscribe_to_topics(self):
        for topic in self.all_topics:
            try:
                self.mqtt_client.subscribe(topic)
            except Exception as e:
                info(f"Error subscribing to {topic}: {str(e)}\n")



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description = 'Params sensors')
    parser.add_argument('--name'  , action = 'store', dest = 'name'  , required = True)
    parser.add_argument('--ip'    , action = 'store', dest = 'ip'    , required = True)
    parser.add_argument('--broker', action = 'store', dest = 'broker', required = True)
    parser.add_argument('--port'  , action = 'store', dest = 'port'  , required = True)

    args = parser.parse_args()

    server = MQTTServer(args.name, str(args.ip), str(args.broker), int(args.port))
    server.start_mqtt_client()
    
    i = input("press enter to kill")
    if i:
        del server
    
