from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP, UDP, ICMP

def monitora_dados(packet):

	# Verifica a camada 2 para extrair endereços MAC
	if packet.haslayer(Ether):
	
		eth = packet.getlayer(Ether)
		
		print("============================================")
		print(f"\033[1;36m[Camada 2 - Enlace] - Origem: {eth.src} | Destino: {eth.dst}\033[0m")
		
	
	# Verifica a camada 3 para extrair endereços lógicos (IP)  
	if packet.haslayer(IP):
	
		ip = packet.getlayer(IP)
		
		print(f"\033[1;32m[Camada 3 - Rede] - Origem: {ip.src} | Destino: {ip.dst}\33[0m")
		
		
		# Verifica a camada 3 para extrair o tipo e o código do ICMP 
		if packet.haslayer(ICMP):
		
			icmp = packet.getlayer(ICMP)
			
			print(f"\033[1;36m[Camada 3 - Rede - (ICMP)] Tipo: {icmp.type} | Código: {icmp.code}\033[0m")
		
		
		# Verifica a camada 4 para extrair a porta de origem e porta de destino
		elif packet.haslayer(TCP):
		
			tcp = packet.getlayer(TCP)
			
			print(f"\033[1;33m[Camada 4 - Transporte - TCP] - Porta origem: {tcp.sport} | Porta destino: {tcp.dport} | FLAG: {tcp.flags}\033[0m")
		
		elif packet.haslayer(UDP):
		
			udp = packet.getlayer(UDP)
			
			print(f"\033[1;33m[Camada 4 - Transporte - UDP] - Porta origem: {udp.sport} | Porta destino: {udp.dport}\033[0m")
			
			
		# Verifica se o segmento possui payload, se sim, extrai o payload.
		if packet.haslayer(Raw):
			
			payload = hexdump(packet.getlayer(Raw).load, dump=True)
				
			print(f"\033[1;31m[Camada 7 - Aplicação] - Dados: \033[0m")
			print(f"\033[1;31m{payload}\033[0m")

				
	

print("\033[1;36m[+]--The Argus--[+]\033[0m - Criado por: \033[1;36mThiago Perini\033[0m")
sniff(prn=monitora_dados, store=False)
