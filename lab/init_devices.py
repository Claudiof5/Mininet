from broker_configs import mqtt_broker_configs
from device_types import DeviceType


def initDevices():
    devs =[
    {"broker_ip": mqtt_broker_configs["HOST"], "port": mqtt_broker_configs["PORT"], "client_name": "lamp1", "keepalive": mqtt_broker_configs["KEEPALIVE"]},
    {"broker_ip": mqtt_broker_configs["HOST"], "port": mqtt_broker_configs["PORT"], "client_name": "phone", "keepalive": mqtt_broker_configs["KEEPALIVE"]},
    {"broker_ip": mqtt_broker_configs["HOST"], "port": mqtt_broker_configs["PORT"], "client_name": "sensor", "keepalive": mqtt_broker_configs["KEEPALIVE"]}
    ]
    
    return devs