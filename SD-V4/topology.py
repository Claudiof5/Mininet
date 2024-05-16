import time
import threading
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
import paho.mqtt.client as mqtt

from broker import MQTTServer
from smart_device import SmartDevice

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
