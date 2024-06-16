from enum import Enum


SULFIXO_DE_COMANDO  = "/commands"
TOPICO_DE_CONFIGURAR_PADRAO = "CONFIG"
TOPICO_PADRAO = "home"
class COMMAND_STRUCTURE(Enum):
    device_name_index  = 0
    command_index      = 1
    params_start_index = 2

#formato da mensagem "NOME_DO_DEVICE COMANDO_A_SER_EXECUTADO PARAM1 PARAM2 ... PARAMN"
class COMMANDS(Enum):
    turn_off                    = { "code": "TOFF" , "n_params": 0 }
    turn_on                     = { "code": "TON"  , "n_params": 0 }
    disconnect_from_broker      = { "code": "DISC" , "n_params": 0 }
    start_sending_messages      = { "code": "STRSM", "n_params": 0 }
    modify_publishing_topic     = { "code": "MODPT", "n_params": 1 }
    modify_command_topic        = { "code": "MODCT", "n_params": 1 }
    modify_publishing_interval  = { "code": "MODPI", "n_params": 1 }
    change_name                 = { "code": "NAME" , "n_params": 1 }
    echo                        = { "code": "ECHO" , "n_params": 1 }
    
    @property
    def code(self):
        return self.value["code"]

    @property
    def n_params(self):
        return self.value["n_params"]


class MESSAGE_STRUCTURE(Enum):
    src_device_index       = 0
    msg_type_index         = 1
    msg_params_start_index = 2
    

class MESSAGES(Enum):
    first_connection            = { "code": "HELLO" , "n_params": 1 }
    status_n                    = { "code": "ST"    , "n_params": 2 }
    disconnect                  = { "code": "BYE"   , "n_params": 0 }
    @property
    def code(self):
        return self.value["code"]

    @property
    def n_params(self):
        return self.value["n_params"]

class ADRESS(Enum):
    address_all_devices = "ALL"
