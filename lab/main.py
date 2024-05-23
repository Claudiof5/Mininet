from device_connection import Device
from init_devices import initDevices
from mininet.net import Mininet
from mininet.cli import CLI


def init_topology():
    devices = initDevices()
    net = Mininet()

    host_objects = {}
    for device in devices:
        host_name = device["client_name"]
        host_obj = net.addHost(host_name, cls=Device, **device)
        host_objects[host_name] = host_obj
    
    net.start()

    for device in devices:
        host_name = device["client_name"]
        host_obj = host_objects[host_name]
        host_obj.start_connection()
    
    CLI(net)
    
    net.stop()

if __name__ == "__main__":
    init_topology()
