
import time
import threading
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi, Station

class SmartDevice(Station):
    def __init__(self, name, **params):
        super(SmartDevice, self).__init__(name, **params)
        self.broker_ip = None
        self.is_on = False
        self.message_interval = 10 

    def link_with_broker(self, broker_ip):
        self.broker_ip = broker_ip
        info(f"{self.name} linked to broker at {self.broker_ip}\n")

    def turn_on(self):
        self.is_on = True
        info(f"{self.name} está ligado\n")
        self.start_sending_messages()

    def turn_off(self):
        self.is_on = False
        info(f"{self.name} está desligado\n")

    def send_message(self, topic, message):
        if self.is_on and self.broker_ip:
            command = f"mosquitto_pub -h {self.broker_ip} -t '{topic}' -m '{message}'"
            retorno = self.cmd(command)
            #info(retorno)


    def start_sending_messages(self):
        def run():
            while self.is_on:
                self.send_message("home", 15 )
                time.sleep(self.message_interval)
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()



class MQTTServer(Station):
    def __init__(self, *args, **kwargs):
        super(MQTTServer, self).__init__(*args, **kwargs)
        self.mqtt_port = 1883  # Default MQTT port for Mosquitto
        #self.mqtt_log = '/tmp/mosquitto.log'  # Log file path
    
    def start_broker(self):
        command = f'mosquitto -p {self.mqtt_port} -d -v'
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
