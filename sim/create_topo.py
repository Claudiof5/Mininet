from mininet.node import  OVSKernelSwitch
from mininet.link import TCLink
import utils_hosts
from sys import maxsize

def create(net, max_hosts=maxsize):
	#adicionando os switches
	QTD_SWITCHES=1
	s1=net.addSwitch('s1',cls=OVSKernelSwitch, failMode='standalone')

	#criacao dos hosts baseado no arquivo data_host
	QTD_HOSTS= min(len(utils_hosts.return_hosts()), max_hosts)
	for i in range(1,QTD_HOSTS+1):
		net.addHost(f'h{i}',ip=f'10.0.0.{i}/24')
		
		
	#largura de banda entre switches e hosts (devices e gateways) 3MB
	bw_hosts=5
	s=1
    #criacao simples dos links entre switches e hosts (devices e gateways)
	for i in range(1,QTD_HOSTS+1):
		link_features = {'bw':bw_hosts}
		net.addLink(net.get("s1"),net.get(f"h{i}"),cls=TCLink, **link_features)
		
