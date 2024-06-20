from mininet.node import  OVSKernelSwitch
from mininet.link import TCLink
import utils_hosts

def create(net):
	#adicionando os switches
	QTD_SWITCHES=1
	s1=net.addSwitch('s1',cls=OVSKernelSwitch, failMode='standalone')

	#criacao dos hosts baseado no arquivo data_host
	QTD_HOSTS=len(utils_hosts.return_hosts())
	for i in range(1,QTD_HOSTS+1):
		net.addHost('h%d'%i,ip='10.0.0.%d/24'%i)
	
	#largura de banda entre switches e hosts (devices e gateways) 3MB
	bw_hosts=5
	s=1
    #criacao simples dos links entre switches e hosts (devices e gateways)
	for i in range(1,QTD_HOSTS+1):
		link_features = {'bw':bw_hosts}
		net.addLink(net.get("s%d"%(s)),net.get("h%d"%i),cls=TCLink, **link_features)
		if(s==QTD_SWITCHES):
			s=0
		s=s+1
