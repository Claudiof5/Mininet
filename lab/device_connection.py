import time
import paho.mqtt.client as mqtt
from mininet.node import Host
from device_types import DeviceTypes

class Device(Host):
    def __init__(self, name: str, broker_ip: str, port: int, client_name: str,  topics: DeviceTypes, keepalive=60, **kwargs):
        super(Device, self).__init__(client_name, **kwargs)
        self.__broker_ip = broker_ip
        self.__port = port
        self.__client_name = client_name
        self.__keepalive = keepalive
        self.__mqtt_client = None
        self.__topic_subscription = topics.value[0][1]
        self.__topic_to_publish = topics.value[0][1]

    def start_connection(self):
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, self.__client_name)
        mqtt_client.user_data_set({'topic_subscription': self.__topic_subscription})
        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_subscribe = self.on_subscribe
        mqtt_client.on_message = self.on_message

        mqtt_client.connect(host=self.__broker_ip, port=self.__port, keepalive=self.__keepalive)
        self.__mqtt_client = mqtt_client
        self.__mqtt_client.loop_start()
        while True:
            message = "Code 5"
            self.publish(message)
            time.sleep(5)

    def on_connect(name, client, userdata, flags, rc, props):
        if rc == 0:
            print(f'Succesfully connected: {client}')
            topic_subscription = userdata['topic_subscription']
            client.subscribe(topic_subscription)
        else:
            print("Cliente", client)
            print("Flags", flags) 
            print("userData", userdata)
            print("prop", props)
            print(f'Failed Connection! code={rc}')

    def on_subscribe(name, client, userdata, mid, granted_qos, prop):
        print(f'Cliente Subscribed')
        print(f'QOS: {granted_qos}')

    def on_message(name, client, userdata, message):
        print('Message Received!')
        print(client)
        print(message.payload)

    def publish(self, message, qos=1):
        self.__mqtt_client.publish(topic=self.__topic_to_publish, payload=message, qos=qos)

    def end_connection(self):
        try:
            self.__mqtt_client.loop_stop()
            self.__mqtt_client.disconnect()
            return True
        except:
            return False
