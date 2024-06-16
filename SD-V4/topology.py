import time
from mininet.log import lg, info
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.topolib import TreeNet
#from networking import connectToInternet, stopNAT
import paho.mqtt.client as mqtt

from broker import MQTTServer
from smart_device import SmartDevice

def init_sensors(net):

    for host in net.hosts():
        pass



def topology():
    #h1.cmdPrint( "python3 smart_device.py --name h1 --ip 10.0.0.1 --broker 192.168.56.4")
    #h2.cmdPrint( "python3 broker.py --name h1 --ip 10.0.0.1 --broker 192.168.56.4 --port 1883")
    #inicia server mqtt
    


    
    net = TreeNet(depth=1, fanout=4)
    net.addNAT().configDefault()
    net.start()
    
    
    for host in net.hosts:
        host.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')
        host.cmd('echo "nameserver 8.8.4.4" >> /etc/resolv.conf') 
        
    CLI(net)
    
    net.stop()

if __name__ == '__main__':
    lg.setLogLevel("info")
    topology()

