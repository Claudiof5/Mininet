
import time
import threading
from mininet.log import info
from mn_wifi.net import Station
import paho.mqtt.client as mqtt
from VARIAVEIS import *

class SmartDevice(Station):

    def __init__(self, name, publishing_interval, **params):
        super(SmartDevice, self).__init__(name, **params)
        

        self.is_on = False
        self.is_connected = False
        
        self.mqtt_client = None
        self.broker_ip = None

        self.publishing_interval = publishing_interval
        self.publishing_topic = TOPICO_DE_CONFIGURAR_PADRAO
        self.command_topic = self.publishing_topic + SULFIXO_DE_COMANDO
        
        self.device_type  = "Standart"
        self.info_to_send = ""

        self.start_mqtt_client()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected with result code {rc}")

    def on_message(self, mqttc, obj, msg: mqtt.MQTTMessage):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

        if msg.topic == self.command_topic:
            self.translate_command(msg.payload)

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


    def translate_command(self, msg:str):
        msglist = msg.split(" ")
        name = msglist[COMMAND_STRUCTURE.device_name_index]
        command = msglist[COMMAND_STRUCTURE.command_index]
        params = msglist[:COMMAND_STRUCTURE.params_start_index]
        
        if name == self.name or name == ADRESS.address_all_devices: 
            self.execute_command( command, params)
    
    def execute_command(self, command, params):

        if command == COMMANDS.turn_off["code"]:
            self.turn_off( *params[:COMMANDS.turn_off["n_params"]])

        elif command == COMMANDS.turn_on["code"]:
            self.turn_on( *params[:COMMANDS.turn_off["n_params"]])

        elif command == COMMANDS.modify_publishing_interval["code"]:
            self.modify_publishing_interval( *params[:COMMANDS.turn_off["n_params"]] )

        elif command == COMMANDS.modify_publishing_topic["code"]:
            self.modify_publishing_topic( *params[:COMMANDS.turn_off["n_params"]] )
        
        elif command == COMMANDS.modify_command_topic["code"]:
            self.modify_publishing_topic( *params[:COMMANDS.turn_off["n_params"]] )

        elif command == COMMANDS.disconnect_from_broker["code"]:
            self.disconnect_from_broker( *params[:COMMANDS.turn_off["n_params"]])

    def modify_publishing_interval(self, new_interval):
        self.publishing_interval = new_interval
    
    def modify_publishing_topic(self, new_topic):
        self.publishing_topic = new_topic

    def modify_command_topic(self, new_command_topic):
        self.command_topic = new_command_topic


    def connect_with_broker(self, broker_ip):
        self.broker_ip = broker_ip
        
        
        info(f"trying to connect to :{broker_ip}")
        try:
            self.mqtt_client.connect(broker_ip, port=1883, keepalive=60)

            self.mqtt_client.loop_start()
            

            info(f"{self.name} linked to broker at {self.broker_ip}\n")
            self.is_connected = True
            self.listen_to_command_messages()
            
            message = f"{self.name} {MESSAGES.first_connection} {self.device_type}"
            self.send_message(self.publishing_topic)
            #self.start_sending_status_messages()
        except Exception as e:
            info(f"Error connecting to MQTT Broker: {str(e)}\n")
        
    def turn_on(self):
        self.is_on = True
        info(f"{self.name} is on\n")
        self.start_sending_messages()

    def turn_off(self):
        self.is_on = False
        info(f"{self.name} is off\n")       

    def disconnect_from_broker(self):
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

    def send_message(self, topic, message):
        if self.is_connected and self.broker_ip:
            try:
                info(f"sending message to {self.broker_ip}")
                self.mqtt_client.publish(topic, message)
            except Exception as e:
                info(f"Error sending message to {self.topic}: {str(e)}\n")

    def start_sending_status_messages(self):

        def run():
            while self.is_connected and self.broker_ip:
                info = self.info
                status = "ON {info}" if self.is_on else "OFF"
                message = f"{self.name} {MESSAGES.status_n} {status}"
                self.send_message(self.publishing_topic, message)
                time.sleep(self.publishing_interval)

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    def listen_to_command_messages(self):
        try:
            self.mqtt_client.subscribe(self.command_topic)
        except Exception as e:
            info(f"Error subscribing to {self.command_topic}: {str(e)}\n")

