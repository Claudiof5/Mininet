import time
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.net import Mininet
from networking import connectToInternet, stopNAT
import paho.mqtt.client as mqtt

from broker import MQTTServer
from smart_device import SmartDevice

def init_sensors(net):

    for host in net.hosts():





def topology():
    net = Mininet()

    s1 = net.addSwitch('s1')
    h1 = net.addHost('h1' , ip='10.0.0.1')
    h2 = net.addHost("h2" , ip='10.0.0.2')

    h1.cmdPrint( "python3 smart_device.py --name h1 --ip 10.0.0.1 --broker 192.168.56.4")
    h2.cmdPrint( "python3 broker.py --name h1 --ip 10.0.0.1 --broker 192.168.56.4 --port 1883")
    #inicia server mqtt
    

    net.addLink(s1, h1)
    net.addLink(s1, h2)

    net.build()
    net.start()

    rootnode = connectToInternet( net )
    CLI(net)
    stopNAT( rootnode )
    time.sleep(1)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

