#!/usr/share/python3

'''
Modo de uso: python3 WebRequestAutomatizado.py [http://SITE ou https://SITE] [caminho/para/wordlist.txt]
Exemplo: python3 WebRequestAutomatizado.py http://www.teste.com.br caminho/para/wordlist.txt
OBS: Se a wordlist não for informada, automaticamente será selecionada a wordlist padrão
'''


def menu():
    print("\n")
    print("\033[1;32m██████      ██  ████     ██  ████\033[0m")
    print("\033[1;32m░█░░░░██    █░█ ░██░██   ░██ █░░░ █\033[0m")
    print("\033[1;32m░█   ░██   █ ░█ ░██░░██  ░██░    ░█\033[0m")
    print("\033[1;32m░██████   ██████░██ ░░██ ░██   ███\033[0m")
    print("\033[1;32m░█░░░░ ██░░░░░█ ░██  ░░██░██  ░░░ █\033[0m")
    print("\033[1;32m░█    ░██    ░█ ░██   ░░████ █   ░█\033[0m")
    print("\033[1;32m░███████     ░█ ░██    ░░███░ ████\033[0m")
    print("\033[1;32m░░░░░░      ░  ░░      ░░░  ░░░░\033[0m")
    print("\n\033[1;32m[+] Criado por: Thiago Perini\033[0m\n")


# Função que receberá a wordlist, site e a extensão
def verificando_site(wordlist, site, ext):
    # Abre o arquivo "wordlist" e realiza o tratamento de caracteres para utf-8 (no caso a wordlist se chamará "arquivo")
    # [+]---------------------------Buscando por diretórios---------------------------[+]
    with open(wordlist, encoding="utf-8") as arquivo:
        print()
        lista_unica = []
        lista_diretorios = []

        print(f"==========Buscando em {site}==========")
        print()
        for palavra in arquivo:
            palavra_convert = palavra.rstrip()  # palavra_convert recebe variavel "palavra" SEM QUEBRA DE LINHAS
            if palavra_convert not in lista_unica:  # Garantindo que uma palavra seja pesquisada somente uma vez
                lista_unica.append(palavra_convert)  # <--- Adicionando a lista para checagens futuras

                site_informado = requests.get(site + "/" + palavra_convert)  # Realizando o request para o site
                status = site_informado.status_code  # Verificando o código de retorno

                if status == 200:  # Se o código for 200 então existe, OK!
                    data = datetime.datetime.now()
                    horario_atual = data.strftime("%H:%M:%S")
                    print(f"\r[\033[1;32m{horario_atual}\033[0;0m] [+] Diretório Encontrado ===>",site + "/" + palavra_convert)  # Imprime o diretório encontrado
                    lista_diretorios.append(site + "/" + palavra_convert)  # Adiciona o diretório a lista para checagens futuras

                else:
                    print("\rTentando com:", (site + '/' + palavra_convert), end="")
                    print("\r", " " * (len("Tentando com: " + (site + '/' + palavra_convert))), end="")

        # [+]---------------------------Buscando por diretórios---------------------------[+]

        # [+]---------------------------Buscando por subdomínios[+]---------------------------[+]

        div = site.split(":")
        pt1 = div[0] + "://"
        pt2 = site.split("//")[1]
        subdominios = []
        print()
        print(f"==========[+]Buscando Subdomínios em {site}==========")
        print()

        with open(wordlist, encoding="utf-8") as arquivo2:
            arquivo2.seek(0)

            for palavra in arquivo2:
                palavra_convert = palavra.rstrip()
                subdominio = (pt1 + palavra_convert + "." + pt2).strip()

                print(f"\rTentando com:", subdominio, end="")
                print("\r", " " * (len("Tentando com:" + subdominio)), end="")
                time.sleep(0.4)
                try:
                    verifica = requests.get(subdominio)
                    status_verifica = verifica.status_code

                    if status_verifica == 200:
                        data = datetime.datetime.now()
                        horario_atual = data.strftime("%H:%M:%S")
                        print(f"\r[\033[1;32m{horario_atual}\033[0;0m] [+] Subdomínio encontrado =====> ", subdominio)
                        subdominios.append(subdominio)
                except:
                    pass

        # [+]---------------------------Buscando por subdomínios[+]---------------------------[+]

        # [+]---------------------------Buscando por arquivos---------------------------[+]
        print()
        print(f"==========[+]Iniciando Busca Por Arquivos {ext}==========")
        print()

        for diretorios in lista_diretorios:

            with open(wordlist, encoding="utf-8") as arquivo:

                arquivo.seek(0)

                for palavras in lista_unica:
                    site_informado = requests.get(diretorios + "/" + palavras + ext)
                    status = site_informado.status_code  # Verificando o código de retorno

                    if status == 200:  # Se o código for 200 então existe, OK!
                        data = datetime.datetime.now()
                        horario_atual = data.strftime("%H:%M:%S")
                        print(f"\r[\033[1;32m{horario_atual}\033[0;0m][+] Arquivo Encontrado ===>", diretorios + "/" + palavras + ext)

                    else:
                        print("\rTentando com:", (diretorios + '/' + palavras + ext), end="")
                        print("\r", " " * (len("Testando com:" + (diretorios + '/' + palavras + ext))), end="")

        # [+]---------------------------Buscando por arquivos---------------------------[+]


# Importando módulos necessários
import requests, sys, datetime, os, time

# Verificando se o usuário informou o site
try:
    site = sys.argv[1]
    verificacao = requests.get(site)
    code_verificacao = verificacao.status_code
    if site.startswith("http://") or site.startswith("https://") and code_verificacao == 200:
        menu()
        print("==========INFO==========")
        print(f"[+] Site: \033[1;32m{site}\033[0m")
    else:
        sys.exit()

    # Perguntando qual extensão o usuário deseja pesquisar
    # Se nada for informado utilizará por padrão .txt
    extensoes_validas = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'mp3', 'mp4', 'svg',
                         'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'json',
                         'php', 'css', 'html', 'htm', 'txt', 'asp', 'aspx',
                         'xml', 'csv', 'rtf', 'odt', 'ods', 'odp', 'tar', 'gz', 'bz2',
                         'rar', '7z', 'sql', 'py', 'java', 'cpp', 'h', 'rb',
                         'phtml', 'twig', 'scss', 'less', 'cgi',
                         'jsx', 'tsx', 'vue', 'swift', 'go', 'yaml', 'yml', 'sh']
    ext = input("[?] Extensão (Enter para seguir padrão): ").strip()
    if ext != "" and ext in extensoes_validas:
        print(f"[+] Extensão: \033[1;32m{ext}\033[0m")
        ext = "." + ext
    else:
        print("[!] Extensão padrão adicionada (\033[1;32m.txt\033[0m)")
        ext = ".txt"

    # Verifica se o site informado existe
    try:
        conferencia = requests.get(site)

        # Se o site existir, verifica se o usuário informou uma wordlist
        try:
            wd = sys.argv[2]
            if os.path.exists(wd):
                wd_informada = wd.split("/")[-1]
                print(f"[+] Wordlist: \033[1;32m{wd_informada}\033[0m")
            else:
                print("\033[1;31m[!] Wordlist Inválida Informada\033[0m")
            # Envia a wordlist, site e extensão para a função "verificando_site"
            verificando_site(wd, site, ext)

        # Se nenhuma wordlist for informada pelo usuario, o programa utilizará a padrão
        except:
            print("[!] Utilizando a Wordlist Padrão: [\033[1;32mWebRequestWD.txt\033[0m]")

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
