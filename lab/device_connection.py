import threading
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
        self.__topic_subscription = topics.value[0]
        self.__topic_to_publish = topics.value[1]

    def start_connection(self):
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, self.__client_name)
        mqtt_client.user_data_set({'topic_subscription': self.__topic_subscription})
        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_subscribe = self.on_subscribe
        mqtt_client.on_message = self.on_message

        mqtt_client.connect(host=self.__broker_ip, port=self.__port, keepalive=self.__keepalive)
        self.__mqtt_client = mqtt_client
        self.__mqtt_client.loop_start()
        self.mqtt_thread = threading.Thread(target=self.publish)
        self.mqtt_thread.daemon = True
        self.mqtt_thread.start()

    def on_connect(self, client, userdata, flags, rc, props=None):
        print(f'on_connect called with: client={client}, userdata={userdata}, flags={flags}, rc={rc}, props={props}')
        if rc == 0:
            print(f'Successfully connected: {client}')
            topic_subscription = userdata['topic_subscription']
            client.subscribe(topic_subscription)
        else:
            print(f'Failed Connection! code={rc}')

    def on_subscribe(self, client, userdata, mid, reason_code_list, properties):
        print('Client Subscribed')
        print(f'on_subscribe called with: client={client}, userdata={userdata}, mid={mid}, reason_code_list={reason_code_list}, properties={properties}')

    def on_message(self, client, userdata, message):
        print('Message Received!')
        print(f'Client: {client}')
        print(f'on_message called with: client={client}, userdata={userdata}, message={message}')
        print(f'Message payload: {message.payload}')

    def publish(self):
        qos=1
        while True:
            try:
                message = "Code 5"
                self.__mqtt_client.publish(topic=self.__topic_to_publish, payload=message, qos=qos)
                time.sleep(5)
            except KeyboardInterrupt:
                self.end_connection()

    def end_connection(self):
        try:
            self.__mqtt_client.loop_stop()
            self.__mqtt_client.disconnect()
            super(Device, self).terminate()
            return True
        except:
            return False
