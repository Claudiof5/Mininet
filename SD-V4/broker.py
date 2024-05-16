import time
import threading
from mininet.log import info
from mn_wifi.net import Station
import paho.mqtt.client as mqtt
from VARIAVEIS import *
from typing import Dict, List

class MQTTServer(Station):
    def __init__(self, name, topics = [], **params):
        super(MQTTServer, self).__init__(name, **params)
        self.mqtt_port = 1883
        self.ip = self.IP()

        self.config_topic = TOPICO_DE_CONFIGURAR_PADRAO
        self.standard_topic = self.standard_topic
        self.command_sulfix = SULFIXO_DE_COMANDO

        self.all_topics = [self.config_topic, self.standard_topic].append(topics)

        self.connected_devices: Dict[str, List[Dict[str, str]]] = {}
        self.mqtt_client = None
        
    def start_broker(self):
        command = f'mosquitto -p {self.mqtt_port} -d -v'
        self.cmd(command)
        info(f"\nopen to messagens in {self.ip}:{self.mqtt_port}\n")
        self.start_mqtt_client()

    def stop_broker(self):
        self.cmd('killall mosquitto')

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected with result code {rc}")

    def on_message(self, mqttc, obj, msg: mqtt.MQTTMessage):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

        if msg.topic == self.config_topic:
            self.handle_new_connection(msg.payload)
        else:
            self.log_message(msg.payload)

    def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
        print("Subscribed: " + str(mid) + " " + str(reason_code_list))

    def on_log(mqttc, obj, level, string):
        print(string)

    def start_mqtt_client(self):
        self.mqtt_client               = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.on_message    = self.on_message
        self.mqtt_client.on_connect    = self.on_connect
        self.mqtt_client.on_subscribe  = self.on_subscribe
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_log        = self.on_log

        self.mqtt_client.connect( self.ip(), self.mqtt_port)


    def handle_new_connection(self, msg:str):
        msg_list = msg.split(" ")

        msg_sender_name = msg_list[MESSAGE_STRUCTURE.src_device_index]
        msg_type        = msg_list[MESSAGE_STRUCTURE.msg_type_index]
        msg_params      = msg_list[MESSAGE_STRUCTURE.msg_params_start_index]

        if msg_type == MESSAGES.first_connection:
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
                self.send_command_change_device_pub_topic( command_topic, nome, self.standard_topic)
                self.send_command_change_device_comm_topic( command_topic, nome, self.standard_topic+self.command_sulfix)


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
        command_modify_name  = f"{device} {COMMANDS.change_name} {device_new_name}"
        self.send_message( topic, command_modify_name )

    def send_command_change_device_pub_topic( self, topic, device, new_topic):
        command_modify_pub_topic  = f"{device} {COMMANDS.modify_publishing_topic} {new_topic}"
        self.send_message( topic, command_modify_pub_topic )

    
    def send_command_change_device_comm_topic( self, topic, device, new_topic):
        command_modify_comm_topic  = f"{device} {COMMANDS.modify_command_topic} {new_topic}"
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