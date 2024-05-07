import paho.mqtt.client as mqtt
from mininet import Host

class Device(Host):
    def __init__(self, broker_ip: str, port: int, client_name: str,  topics: list[str], keepalive=60, **kwargs):
        super(Device, self).__init__(client_name, **kwargs)
        self.__broker_ip = broker_ip
        self.__port = port
        self.__client_name = client_name
        self.__keepalive = keepalive
        self.__mqtt_client = None
        self.__topic_subscription = topics[0]
        self.__topic_to_publish = topics[1]

    def start_connection(self):
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, self.__client_name)
        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_subscribe = self.on_subscribe
        mqtt_client.on_message = self.on_message

        mqtt_client.connect(host=self.__broker_ip, port=self.__port, keepalive=self.__keepalive)
        self.__mqtt_client = mqtt_client
        self.__mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f'Cliente Conectado com sucesso: {client}')
            client.subscribe(self.__topic_subscription)
        else:
            print(f'Erro ao me conectar! codigo={rc}')

    def on_subscribe(client, userdata, mid, granted_qos):
        print(f'Cliente Subscribed')
        print(f'QOS: {granted_qos}')

    def on_message(client, userdata, message):
        print('Message Received!')
        print(client)
        print(message.payload)

    def publish(self, message):
        self.__mqtt_client.publish(topic=self.__topic_to_publish, payload=message)

    def end_connection(self):
        try:
            self.__mqtt_client.loop_stop()
            self.__mqtt_client.disconnect()
            return True
        except:
            return False