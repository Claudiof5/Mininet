
import time
import threading
from mininet.log import info
import paho.mqtt.client as mqtt
from VARIAVEIS import COMMAND_STRUCTURE, COMMANDS, MESSAGE_STRUCTURE, MESSAGES, ADRESS, SULFIXO_DE_COMANDO, TOPICO_DE_CONFIGURAR_PADRAO, TOPICO_PADRAO

class SmartDevice:

    def __init__(self, name, ip, publishing_interval = 10):
        
        
        self.name = name
        self.ip = ip

        self.is_on = False
        self.is_connected = False
        
        self.mqtt_client = None
        self.broker_ip = None

        self.publishing_interval = publishing_interval
        self.publishing_topic = TOPICO_DE_CONFIGURAR_PADRAO
        self.command_topic = self.publishing_topic + SULFIXO_DE_COMANDO
        
        self.device_type  = "Standart"
        self.info_to_send = "test"

        self.start_mqtt_client()

    def on_connect( self, client, userdata, flags, rc, properties=None):
        print(f"Connected with result code {rc}")

    def on_disconnect( self, client, userdata, rc):
        print(f"Disconnected with result code {rc}")

    def on_message( self, mqttc, obj, msg: mqtt.MQTTMessage):
        payload_str = msg.payload.decode('utf-8')
        print(msg.topic + " " + str(msg.qos) + " " + str(payload_str))

        if msg.topic == self.command_topic:
            self.translate_command(payload_str)

    def on_subscribe( self, mqttc, obj, mid, reason_code_list, properties):
        print("Subscribed: " + str(mid) + " " + str(reason_code_list))

    def on_log( self, mqttc, obj, level, string):
        print(string)

    def start_mqtt_client(self):
        self.mqtt_client               = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.on_message    = self.on_message
        self.mqtt_client.on_connect    = self.on_connect
        self.mqtt_client.on_subscribe  = self.on_subscribe
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_log        = self.on_log


    def translate_command(self, msg:str):
        print("oi"+msg)
        msglist = msg.split(" ")
        name = msglist[COMMAND_STRUCTURE.device_name_index.value]
        command = msglist[COMMAND_STRUCTURE.command_index.value]
        params = msglist[COMMAND_STRUCTURE.params_start_index.value:]
        
        print( f"name:{name}, command:{command}, params:{params}")
        if name == self.name or name == ADRESS.address_all_devices: 
            self.execute_command( command, params)
    
    def execute_command(self, command, params):
        if command == COMMANDS.turn_off.code:
            params = params[:COMMANDS.turn_off.n_params]
            self.turn_off( *params )

        elif command == COMMANDS.turn_on.code:
            params = params[:COMMANDS.turn_on.n_params]
            self.turn_on( *params ) 

        elif command == COMMANDS.modify_publishing_interval.code:
            params = params[:COMMANDS.modify_publishing_interval.n_params]
            self.modify_publishing_interval( *params )

        elif command == COMMANDS.modify_publishing_topic.code:
            params = params[:COMMANDS.modify_publishing_topic.n_params]
            self.modify_publishing_topic( *params )
        
        elif command == COMMANDS.modify_command_topic.code:
            params = params[:COMMANDS.modify_command_topic.n_params]
            self.modify_command_topic( *params)

        elif command == COMMANDS.modify_publishing_topic.code:
            params = params[:COMMANDS.modify_publishing_topic.n_params]
            self.modify_publishing_topic( *params )
            
        elif command == COMMANDS.echo.code:
            params = params[:COMMANDS.echo.n_params]
            self.echo( *params)
            
        elif command == COMMANDS.start_sending_messages.code:
            params = params[:COMMANDS.start_sending_messages.n_params]
            self.start_sending_status_messages( *params)

    def modify_publishing_interval(self, new_interval):
        self.publishing_interval = new_interval
    
    def modify_publishing_topic(self, new_topic):
        self.publishing_topic = new_topic

    def modify_command_topic(self, new_command_topic):
        self.command_topic = new_command_topic

    def echo(self, message):
        self.send_message( self.publishing_topic ,message)
        
    def connect_with_broker(self, broker_ip):
        self.broker_ip = broker_ip
        
        
        print(f"trying to connect to :{broker_ip}")
        try:
            self.mqtt_client.connect(broker_ip, port=1883, keepalive=60)

            self.mqtt_client.loop_start()
            

            print(f"{self.name} linked to broker at {self.broker_ip}\n")
            self.is_connected = True
            self.listen_to_command_messages()
            code = MESSAGES.first_connection.code
            message = f"{self.name} {code} {self.device_type}"
            self.send_message(self.publishing_topic, message)
            #self.start_sending_status_messages()
        except Exception as e:
            print(f"Error connecting to MQTT Broker: {str(e)}\n")
            print(f"Error connecting to MQTT Broker: {str(e)}\n")
        
    def turn_on(self):
        self.is_on = True
        info(f"{self.name} is on\n")
        self.start_sending_status_messages()

    def turn_off(self):
        self.is_on = False
        info(f"{self.name} is off\n")       

    def disconnect_from_broker(self):
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

    def send_message(self, topic, message):
        if self.is_connected and self.broker_ip:
            try:
                print(f"sending message to {self.broker_ip}")
                self.mqtt_client.publish(topic, message)
            except Exception as e:
                print(f"Error sending message to {self.topic}: {str(e)}\n")

    def start_sending_status_messages(self):

        def run():
            while self.is_connected and self.broker_ip:
                info = self.info_to_send
                status = f"ON {info}" if self.is_on else "OFF"
                message = f"{self.name} {MESSAGES.status_n.code} {status}"
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




if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description = 'Params sensors')
    parser.add_argument('--name'  , action = 'store', dest = 'name'  , required = True)
    parser.add_argument('--ip'    , action = 'store', dest = 'ip'    , required = True)
    parser.add_argument('--broker', action = 'store', dest = 'broker', required = True)

    args = parser.parse_args()

    smart_device = SmartDevice(args.name, args.ip)
    time.sleep(1)
    smart_device.connect_with_broker( args.broker )
    
    i = input( "enter to kill")
    if i:
        del smart_device
