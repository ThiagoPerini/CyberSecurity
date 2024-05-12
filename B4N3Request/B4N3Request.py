#!/usr/share/python3

# Modo de uso: python3 WebRequestAutomatizado.py [http://SITE ou https://SITE] [caminho/para/wordlist.txt]
# Exemplo: python3 WebRequestAutomatizado.py http://www.teste.com.br caminho/para/wordlist.txt
# OBS: Se a wordlist não for informada, automaticamente será selecionada a wordlist padrão.
# Extensões Testadas: .txt, .php, .cgi, .css


def menu():
    print("\n")
    print("██████      ██  ████     ██  ████  ")
    print("░█░░░░██    █░█ ░██░██   ░██ █░░░ █")
    print("░█   ░██   █ ░█ ░██░░██  ░██░    ░█")
    print("░██████   ██████░██ ░░██ ░██   ███ ")
    print("░█░░░░ ██░░░░░█ ░██  ░░██░██  ░░░ █")
    print("░█    ░██    ░█ ░██   ░░████ █   ░█")
    print("░███████     ░█ ░██    ░░███░ ████ ")
    print("░░░░░░      ░  ░░      ░░░  ░░░░   ")
    print("\n[+] Criado por: Thiago Perini\n")

# Função que receberá a wordlist, site e a extensão
def verificando_site(wordlist, site, ext):
    # Abre o arquivo "wordlist" e realiza o tratamento de caracteres para utf-8 (no caso a wordlist se chamará "arquivo")
    # [+]---------------------------Buscando por diretórios---------------------------[+]
    with open(wordlist, encoding="utf-8") as arquivo:
        print()
        lista_unica = []
        lista_diretorios = []

        print(f"==========[+]Buscando em {site}==========")
        print()
        for palavra in arquivo:
            palavra_convert = palavra.rstrip() # palavra_convert recebe variavel "palavra" SEM QUEBRA DE LINHAS
            if palavra_convert not in lista_unica: # Garantindo que uma palavra seja pesquisada somente uma vez
                lista_unica.append(palavra_convert) # <--- Adicionando a lista para checagens futuras

                site_informado = requests.get(site + "/" + palavra_convert) # Realizando o request para o site
                status = site_informado.status_code # Verificando o código de retorno

                if status == 200: # Se o código for 200 então existe, OK!
                      data = datetime.datetime.now()
                      horario_atual = data.strftime("%H:%M:%S")
                      print(f"\r[{horario_atual}] [+] Diretório Encontrado ===>", site + "/" + palavra_convert) # Imprime o diretório encontrado
                      lista_diretorios.append(site + "/" + palavra_convert) # Adiciona o diretório a lista para checagens futuras

                else:
                    print("\rTentando com:", (site + '/' + palavra_convert), end="")
                    print("\r"," " * (len("Tentando com: " + (site + '/' + palavra_convert))), end="")


        # [+]---------------------------Buscando por diretórios---------------------------[+]

        # [+]---------------------------Buscando por arquivos---------------------------[+]
        print()
        print(f"==========[+]Iniciando Busca Por Arquivos {ext}==========")
        print()

        for diretorios in lista_diretorios:

            with open(wordlist, encoding="utf-8") as arquivo:

                arquivo.seek(0)

                for palavras in lista_unica:
                    site_informado = requests.get(diretorios + "/" + palavras + ext)
                    status = site_informado.status_code # Verificando o código de retorno

                    if status == 200: # Se o código for 200 então existe, OK!
                        data = datetime.datetime.now()
                        horario_atual = data.strftime("%H:%M:%S")
                        print(f"\r[{horario_atual}][+] Arquivo Encontrado ===>", diretorios + "/" + palavras + ext)
                    else:
                        print("\rTentando com:", (diretorios + '/' + palavras + ext), end="")
                        print("\r"," " * (len("Testando com:" + (diretorios + '/' + palavras + ext))), end="")

        # [+]---------------------------Buscando por arquivos---------------------------[+]
        print("\n\r[!] Busca Finalizada.")

# Importando módulos necessários
import requests, sys, datetime


# Verificando se o usuário informou o site
try:
    site = sys.argv[1]
    if site.startswith("http://") or site.startswith("https://"):
        menu()
        print("==========INFO==========")
        print(f"[+] Site: {site}")
    else:
        sys.exit()

    # Perguntando qual extensão o usuário deseja pesquisar
    # Se nada for informado utilizará por padrão .txt
    ext = input("[?] Extensão (Enter para seguir padrão): ")
    if ext != "":
        print(f"[+] Extensão: {ext}")
        ext = "." + ext
    else:
        print("[!] Extensão padrão adicionada (.txt)")
        ext = ".txt"

    # Verifica se o site informado existe
    try:
        conferencia = requests.get(site)

        # Se o site existir, verifica se o usuário informou uma wordlist
        try:
            wd = sys.argv[2]
            wd_informada = wd.split("/")[-1]
            print(f"[+] Wordlist: {wd_informada}")
            # Envia a wordlist, site e extensão para a função "verificando_site"
            verificando_site(wd, site, ext)

        # Se nenhuma wordlist for informada pelo usuario, o programa utilizará a padrão
        except:
            print("[!] Utilizando a Wordlist Padrão: WebRequestWD.txt")

            try:
                # Envia a wordlist, site e extensão para a função "verificando_site"
                verificando_site("WebRequestWD.txt", site, ext)


            except:
                # Informa um erro se o usuário não possuir a wordlist padrão
                print("[?] Erro ao utilizar wordlist padrão, certifique-se que você tenha feito o Download da mesma.")


    except:
        # Se o site informado não existir, mostra a mensagem.
        print("[!] Site inválido")


except:
    # Se o argumento 1 (site) não for informado, imprimirá isto.
    print("[!] Site não informado")
    print("[!] Modo de uso: http://SITE ou https://SITE")
