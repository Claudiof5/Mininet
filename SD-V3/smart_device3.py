import time
import asyncio
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi, Station
from gmqtt import Client as MQTTClient

class SmartDevice(Station):
    def __init__(self, name, message_interval=10, **params):
        super(SmartDevice, self).__init__(name, **params)
        self.message_interval = message_interval
        self.is_on = False
        self.client = MQTTClient(self.name)

    def on_connect(self, client, flags, rc, properties):
        print(f"{self.name} connected with result code {rc}")
        self.connected = True
        self.client.subscribe('commands')

    def on_disconnect(self, client, packet, exc=None):
        print(f"{self.name} disconnected")
        self.connected = False

    def on_message(self, client, topic, payload, qos, properties):
        message = payload.decode()
        print(f"Received message '{message}' on topic '{topic}'")

    async def connect_with_broker(self, broker_ip):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        await self.client.connect(broker_ip)

    async def turn_on(self):
        self.is_on = True
        print(f"{self.name} is on")
        asyncio.create_task(self.start_sending_messages())

    async def turn_off(self):
        self.is_on = False
        print(f"{self.name} is off")
        if self.client.is_connected:
            await self.client.disconnect()

    async def start_sending_messages(self):
        while self.is_on:
            if self.connected:
                print(f"{self.name} sending message")
                self.client.publish("home", "ON", qos=1)
            await asyncio.sleep(self.message_interval)

class MQTTServer(Station):
    def __init__(self, name, **params):
        super(MQTTServer, self).__init__(name, **params)
        self.mqtt_port = 1883

    def start_broker(self):
        command = f'mosquitto -p {self.mqtt_port} -d -v'
        retorno = self.cmd(command)
        info(f"\nopen to messages in {self.IP()}:{self.mqtt_port}\n")

    def stop_broker(self):
        self.cmd('killall mosquitto')

async def async_topology():
    net = Mininet_wifi()

    ap1 = net.addAccessPoint('ap1')
    sta1 = net.addStation('sta1', cls=MQTTServer, ip='10.0.0.1')
    sta2 = net.addStation('sta2', cls=SmartDevice, ip='10.0.0.2')

    net.configureWifiNodes()
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)

    sta1.start_broker()
    net.start()

    await sta2.connect_with_broker(sta1.IP())
    await sta2.turn_on()

    CLI(net)

    await sta2.turn_off()
    sta1.stop_broker()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    asyncio.run(async_topology())
