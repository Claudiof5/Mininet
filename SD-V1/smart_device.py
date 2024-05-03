
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

    def send_message(self):
        if self.is_on and self.broker_ip:
            
            response = self.cmd(f'ping -c 1 {self.broker_ip}')
            info(f"sending message to {self.broker_ip}\n")


    def start_sending_messages(self):
        def run():
            while self.is_on:
                self.send_message()
                time.sleep(self.message_interval)
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

def topology():
    net = Mininet_wifi()

    ap1 = net.addAccessPoint('ap1')
    sta1 = net.addStation('sta1', ip='10.0.0.100')
    sta2 :SmartDevice = net.addStation("sta2", cls=SmartDevice, ip='10.0.0.101')

    net.configureWifiNodes()
    
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)

    net.start()

    sta2.link_with_broker(sta1.IP())
    sta2.turn_on()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
