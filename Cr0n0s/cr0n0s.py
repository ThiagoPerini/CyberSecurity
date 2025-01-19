import sys
from time import sleep

def intro():
    print(f'\033[1;34m 'r"""
  ____       ___         ___     
 / ___|_ __ / _ \ _ __  / _ \ ___
| |   | '__| | | | '_ \| | | / __|
| |___| |  | |_| | | | | |_| \__ \     | Script desenvolvido por Thiago Perini
 \____|_|   \___/|_| |_|\___/|___/

"""'\033[0;0m')


def binario(ip, mascara):
    cidr = 0
    bin_ip = bin_masc = []

    ip_str = ip.split(".")
    ip_int = [int(valores) for valores in ip_str]
    mascara_str = mascara.split(".")
    mascara_int = [int(valores) for valores in mascara_str]


    bin_ip = [bin(inteiros)[2:].zfill(8) for inteiros in ip_int]
    capture_ip = [int(numeros) for numeros in bin_ip]

    bin_ip_c = ".".join(bin_ip)
    conf_classe = ip_str[0]
    conf_classe = int(conf_classe)
    classe = verifica_classe(conf_classe)

    bin_masc = [bin(inteiros)[2:].zfill(8) for inteiros in mascara_int]
    capture_masc = [int(numeros) for numeros in bin_masc]
    bin_masc_c = ".".join(bin_masc)
    enderecos = sum([1 for valor_binario in bin_masc_c if valor_binario == '0'])
    enderecos_validos = (2 ** enderecos) - 2

    cidr = sum([valores.count('1') for valores in bin_masc])


    cont_rede = sum([1 for rede in mascara_str if rede == '255'])
    rede = ip_str[:cont_rede]
    host = ip_str[len(rede):]



    completo = converte_host_rede(host, rede, ip_int, mascara_int)
    host_c = completo[0]
    rede_c = completo[1]
    rede_list = rede_c.split(".")
    primeiro_host = int(rede_list[-1])
    broadcast = converte_broadcast(rede_c, mascara_int)
    broadcast_list = broadcast.split(".")
    ultimo_host = int(broadcast_list[-1])

    if primeiro_host < 253:
        primeiro_host += 1
    if ultimo_host > 0:
        ultimo_host -= 1


    # Chamando a função "impressao" e passando os argumentos
    impressao(ip, mascara, cidr, bin_ip_c, bin_masc_c, host_c, rede_c, classe, broadcast, enderecos_validos, primeiro_host, ultimo_host)


# Função para converter "host" e "rede"
def converte_host_rede(host_c, rede_c, ip_int, mascara_int):
    contador = 0
    lista_ip = [str(bin(valores)[2:]).zfill(8) for valores in ip_int]
    lista_mascara = [str(bin(valores)[2:]).zfill(8) for valores in mascara_int]
    ip_convert = []
    mascara_convert = []
    lista_rede = []

    # Pegar todos os valores da lista "lista_ip" individualmente e transformar em inteiros
    for itens in lista_ip:
        for valores in itens:
            ip_convert.append(int(valores))

    # Pegar todos os valores da lista "lista_mascara" individualmente e transformar em inteiros
    for itens in lista_mascara:
        for valores in itens:
            mascara_convert.append(int(valores))

    for valor1, valor2 in zip(ip_convert, mascara_convert):
        soma = valor1 & valor2
        if contador == 8:
            lista_rede.append(".")
            contador = 0
        lista_rede.append(str(soma))
        contador += 1

    rede_str = "".join(lista_rede)
    rede_full = rede_str.split(".")
    rede_int = [int(valores, 2) for valores in rede_full]
    rede_int_to_str = [str(valores) for valores in rede_int]
    rede = ".".join(rede_int_to_str)

    for x in range(4 - len(host_c)):
        host_c.insert(0, '0')
    host_completo = ".".join(host_c)


    completo = host_completo, rede

    return list(completo)

def converte_broadcast(rede_c, mascara_int):
    rede_lista = rede_c.split(".") # '203', '0', '113', '168'
    rede_int = [int(valores) for valores in rede_lista] # 203,0,113,168
    rede_binaria = [str(bin(valores)[2:]).zfill(8) for valores in rede_int] # '11001011', '00000000' , '01110001', '10101000'
    broadcast_binario = [str(bin(valores)[2:]).zfill(8) for valores in mascara_int]
    broadcast_binario_rev = ['0' if item == '1' else '1' for valor in broadcast_binario for item in valor if item != "."]

    rede_binario_int = [int(itens) for valores in rede_binaria for itens in valores]
    broadcast_int = [int(valores) for valores in broadcast_binario_rev]
    broadcast_completa = []

    contador = 0
    for valor1, valor2 in zip(rede_binario_int, broadcast_int):
        soma = valor1 | valor2
        if contador == 8:
            broadcast_completa.append(".")
            contador = 0
        broadcast_completa.append(str(soma))
        contador += 1

    broadcast = "".join(broadcast_completa)
    broadcast_cut = broadcast.split(".")
    broadcast_int = [int(valores, 2) for valores in broadcast_cut]
    broadcast_completa = [str(valores) for valores in broadcast_int]
    broadcast_completa = ".".join(broadcast_completa)

    return broadcast_completa

def verifica_classe(conf_classe):
    classe = ""
    if conf_classe >= 1 and conf_classe <= 127:
        classe = "A"
    elif conf_classe >= 128 and conf_classe <= 191:
        classe = "B"
    elif conf_classe >= 192 and conf_classe <= 223:
        classe = "C"
    elif conf_classe >= 224 and conf_classe <= 239:
        classe = "D"
    elif conf_classe >= 240 and conf_classe <= 255:
        classe = "E"

    return classe

def impressao(ip, mascara, cidr, bin_ip_c, bin_masc_c, host_c, rede_c, classe, broadcast, enderecos_validos, primeiro_host, ultimo_host):

   sleep(2)
   print('_______________________________________________')
   print(f"\n\033[1;34m[+] IP: \033[0;0m{ip} \033[1;34m[+] Binario:\033[0;0m  {bin_ip_c}")
   print(f"\033[1;34m[+] Mascara: \033[0;0m{mascara} \033[1;34m[+] Binario:\033[0;0m {bin_masc_c}")
   print(f"\033[1;34m[+] IP/CIDR: \033[0;0m{ip}/{cidr}")
   print(f"\033[1;34m[+] Host: \033[0;0m{host_c}")
   print(f"\033[1;34m[+] Rede: \033[0;0m{rede_c}")
   print(f"\033[1;34m[+] Primeiro host disponível: \033[0;0m{rede_c[:-4]}.{primeiro_host}")
   print(f"\033[1;34m[+] Ultimo host disponível: \033[0;0m{rede_c[:-4]}.{ultimo_host}")
   print(f"\033[1;34m[+] Broadcast:  \033[0;0m{broadcast}")
   print(f"\033[1;34m[+] Classe:\033[0;0m {classe}")
   print(f"\033[1;34m[+] Número de endereços possíveis: \033[0;0m{enderecos_validos}")
   print('_______________________________________________')

def start():
    if len(sys.argv) < 2:
        print("Modo de uso: python3 cr0n0s.py <IP>/<MASCARA>")
    else:
        intro()
        valor = sys.argv[1]
        valor = valor.split("/")
        ip = valor[0]
        mascara = valor[1]

        ip_mascara = binario(ip, mascara)


start()
