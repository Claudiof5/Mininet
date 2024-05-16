from device_connection import Device
import time
from init_devices import initDevices
from mininet.net import Mininet
from mininet.cli import CLI



def start(device):
    device.start_connection()
    while True: time.sleep(0.001)

def init_topology():
    devices = initDevices()
    net = Mininet()

    host_objects = {}
    for device in devices:
        print(device)
        host_name = device["client_name"]
        host_obj = net.addHost(host_name, cls=Device, **device)
        host_objects[host_name] = host_obj
    
    net.start()

    for device in devices:
        host_name = device["client_name"]
        host_obj = host_objects[host_name]
        start(host_obj)
    
    CLI(net)
    
    net.stop()

if __name__ == "__main__":
    init_topology()
