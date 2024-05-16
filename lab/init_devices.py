from broker_configs import mqtt_broker_configs
from device_types import DeviceTypes

def initDevices():
    devs =[
    {"broker_ip": mqtt_broker_configs["HOST"], "port": mqtt_broker_configs["PORT"], "client_name": "lamp1", "topics": DeviceTypes.STRING, "keepalive": mqtt_broker_configs["KEEPALIVE"]},
    {"broker_ip": mqtt_broker_configs["HOST"], "port": mqtt_broker_configs["PORT"], "client_name": "phone", "topics": DeviceTypes.INTEGER,"keepalive": mqtt_broker_configs["KEEPALIVE"]},
    {"broker_ip": mqtt_broker_configs["HOST"], "port": mqtt_broker_configs["PORT"], "client_name": "sensor", "topics": DeviceTypes.INTEGER, "keepalive": mqtt_broker_configs["KEEPALIVE"]}
    ]
    
    return devs