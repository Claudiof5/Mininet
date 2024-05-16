import time
import threading
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi, Station
import paho.mqtt.client as mqtt


class SmartDevice:

    def __init__(self, name, **params):
        super(SmartDevice, self).__init__(name, **params)
        self.broker_ip = None
        self.is_on = False
        self.message_interval = 10
        self.mqtt_client = mqtt.Client()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            info(f"{self.name} connected to MQTT Broker!")
        else:
            info(f"{self.name} failed to connect, return code {rc}\n")

    def link_with_broker(self, broker_ip, broker_port=1883):
        self.broker_ip = broker_ip
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.connect(broker_ip, broker_port, 60)
        self.mqtt_client.loop_start()
        info(f"{self.name} linked to broker at {self.broker_ip}\n")

    def turn_on(self):
        self.is_on = True
        info(f"{self.name} is on\n")
        self.start_sending_messages()
        self.listen_to_command_messages()

    def turn_off(self):
        self.is_on = False
        info(f"{self.name} is off\n")
        self.mqtt_client.loop_stop()

    def send_message(self, topic, message):
        if self.is_on and self.broker_ip:
            self.mqtt_client.publish(topic, message)

    def start_sending_messages(self):
        def run():
            while self.is_on:
                self.send_message("home/status", "ON")
                time.sleep(self.message_interval)
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    def on_message(client, userdata, message):
            info(f"Received command: {message.payload.decode()}")

    def listen_to_command_messages(self):
        self.mqtt_client.subscribe("home/commands")
        self.mqtt_client.on_message = self.on_message



class MQTTServer(Station):
    def __init__(self, *args, **kwargs):
        super(MQTTServer, self).__init__(*args, **kwargs)
        self.mqtt_port = 1883  # Default MQTT port for Mosquitto
        self.mqtt_log = '/tmp/mosquitto.log'  # Log file path
    
    def start_broker(self):
        command = f'mosquitto -p {self.mqtt_port} -d -v > {self.mqtt_log} 2>&1'
        self.cmd(command)
    
    def stop_broker(self):
        self.cmd('killall mosquitto')

def topology():
    net = Mininet_wifi()

    ap1 = net.addAccessPoint('ap1')
    sta1 :MQTTServer  = net.addStation('sta1', cls=MQTTServer , ip='10.0.0.1')
    sta2 :SmartDevice = net.addStation("sta2", cls=SmartDevice, ip='10.0.0.2')

    net.configureWifiNodes()

    #inicia server mqtt
    sta1.start_broker()

    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)

    net.start()

    sta2.link_with_broker(sta1.IP())
    sta2.turn_on()

    CLI(net)

    time.sleep(1)
    sta2.turn_off()
    sta1.stop_broker()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()