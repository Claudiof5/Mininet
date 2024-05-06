inicia codigo usando

python3 smart_device.py
o SmartDevice criado manda mensagem para o topico home/temperatura recorrentemente para o broker conectado

uma vez executando o mininet abrir o terminal do broker usando

xterm sta1

para visualizar a chegada das mensagens escrever no novo terminal

mosquitto_sub -h 10.0.0.1 -t "home"

para mandar uma mensagem mqtt para esse topico basta em outro terminal escrever

mosquitto_pub -h 10.0.0.1 -t "home" -m "sua_mensagem"
