from enum import Enum


class DeviceTypes(Enum):
    STRING =  ["/string/messages","dev/string/messages"],
    INTEGER = ["/int/messages","dev/int/messages"]