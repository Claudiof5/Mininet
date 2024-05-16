
import time
import threading
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi, Station
import paho.mqtt.client as mqtt


class SmartDevice(Station):

    def __init__(self, name, **params):
        super(SmartDevice, self).__init__(name, **params)
        self.broker_ip = None
        self.is_on = False
        self.message_interval = 10 
        self.mqtt_client = None
        self.connected = False
        
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected with result code {rc}")

    def on_message(mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
        print("Subscribed: " + str(mid) + " " + str(reason_code_list))

    def on_log(mqttc, obj, level, string):
        print(string)

    def connect_with_broker(self, broker_ip):
        self.broker_ip = broker_ip
        
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.on_message   = self.on_message
        self.mqtt_client.on_connect   = self.on_connect
        self.mqtt_client.on_subscribe = self.on_subscribe

        info(f"trying to connect to :{broker_ip}")
        try:

            self.mqtt_client.connect(broker_ip, port=1883, keepalive=60)
            self.mqtt_client.subscribe("commands")
            self.mqtt_client.loop_start()
            info(f"{self.name} linked to broker at {self.broker_ip}\n")
            self.connected = True
            self.listen_to_command_messages()
        except Exception as e:
            info(f"Error connecting to MQTT Broker: {str(e)}\n")
        
    def turn_on(self):
        self.is_on = True
        info(f"{self.name} is on\n")
        self.start_sending_messages()
        #self.listen_to_command_messages()

    def turn_off(self):
        self.is_on = False
        info(f"{self.name} is off\n")
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

    def send_message(self, topic, message):
        if self.is_on and self.broker_ip:
            info(f"sending message to {self.broker_ip}")
            self.mqtt_client.publish(topic, message)

    def start_sending_messages(self):
        def run():
            while self.is_on:
                self.send_message("home", "ON" )
                time.sleep(self.message_interval)
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    def listen_to_command_messages(self):
        self.mqtt_client.subscribe("home/commands")
        self.mqtt_client.on_message = self.on_message

class MQTTServer(Station):
    def __init__(self, name, **params):
        super(MQTTServer, self).__init__(name, **params)
        self.mqtt_port = 1883
    
    def start_broker(self):
        command = f'mosquitto -p {self.mqtt_port} -d -v'
        retorno = self.cmd(command)
        info(f"return : {retorno} \nopen to messagens in {self.IP()}:{self.mqtt_port}\n")

    def stop_broker(self):
        self.cmd('killall mosquitto')



def topology():
    net = Mininet_wifi()

    ap1 = net.addAccessPoint('ap1')
    sta1 :MQTTServer  = net.addStation('sta1', cls=MQTTServer , ip='10.0.0.1')
    sta2 :SmartDevice = net.addStation("sta2", cls=SmartDevice, ip='10.0.0.2')

    net.configureWifiNodes()

    #inicia server mqtt
    

    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)

    sta1.start_broker()
    net.start()
    
    

    sta2.connect_with_broker(sta1.IP())
    #sta2.turn_on()

    CLI(net)

    time.sleep(1)
    sta2.turn_off()
    sta1.stop_broker()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
