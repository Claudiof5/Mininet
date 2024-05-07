from device_connection import Device
from time import time
from init_devices import init_devices
from mininet import Mininet
from mininet import CLI



def start(device):
    device.start_connection()
    while True: time.sleep(0.001)

def init_topology():
    devices = init_devices()
    net = Mininet()
    for i in range(len(devices)):
        net.addHost(cls=Device, **devices[i])
    s1 = net.addSwitch( 's1' )
    c0 = net.addController( 'c0' )
    net.start()
    CLI( net )
    net.stop()

if __name__ == "__main__":
    init_topology()