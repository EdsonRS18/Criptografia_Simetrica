import socket
import os
import random
import itertools
import pickle

# Função para enviar o arquivo pelo socket
def enviar_arquivo(sock, caminho_arquivo):
    nome_arquivo = os.path.basename(caminho_arquivo)
    tamanho_arquivo = os.path.getsize(caminho_arquivo)

    with open(caminho_arquivo, 'rb') as arquivo:
        sock.sendall(b'UPLOAD')
        sock.sendall(nome_arquivo.encode())
        sock.sendall(str(tamanho_arquivo).encode())  # Enviar o tamanho do arquivo

        tamanho_buffer = 4 * 1024
        while True:
            dados = arquivo.read(tamanho_buffer)
            if not dados:
                break
            sock.sendall(dados)

    print("Arquivo enviado com sucesso.")


# Função para baixar o arquivo pelo socket
def baixar_arquivo(sock, nome_arquivo):
    sock.sendall(b'DOWNLOAD')
    sock.sendall(nome_arquivo.encode())

    resposta = sock.recv(1024).decode()
    if resposta == 'FILE_FOUND':
        tamanho_arquivo = int(sock.recv(1024).decode())
        with open(nome_arquivo, 'wb') as arquivo:
            tamanho_restante = tamanho_arquivo
            tamanho_buffer = 4 * 1024
            while tamanho_restante > 0:
                dados = sock.recv(min(tamanho_buffer, tamanho_restante))
                arquivo.write(dados)
                tamanho_restante -= len(dados)

        print("Arquivo baixado com sucesso.")
    elif resposta == 'FILE_NOT_FOUND':
        print("Arquivo não encontrado no servidor.")
    else:
        print("Erro durante o download do arquivo.")


# Função para criar dicionários de criptografia
# Função para criar dicionários de criptografia e salvá-los com o nome fornecido pelo usuário
def criar_dicionarios_criptografia(num_dicionarios, min_digitos, max_digitos):
    letras_maiusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letras_minusculas = "abcdefghijklmnopqrstuvwxyz"
    numeros = "0123456789"
    letras_acentuadas = "áàãâéèêíìîóòõôúùûçÁÀÃÂÉÈÊÍÌÎÓÒÕÔÚÙÛÇ"
    pontuacoes = "!@#$%&*()-_+=/.,?;: "

    caracteres = letras_maiusculas + letras_minusculas + numeros + letras_acentuadas + pontuacoes + ' '

    dicionarios = []

    for i in range(num_dicionarios):
        num_digitos = random.randint(min_digitos, max_digitos)  # Número de dígitos aleatório
        dicionario = {}

        caracteres_embaralhados = random.sample(caracteres, len(caracteres))

        for j in range(len(caracteres_embaralhados)):
            valor_binario = bin(j)[2:].zfill(num_digitos)

            while valor_binario in dicionario.values():
                j = (j + 1) % len(caracteres_embaralhados)
                valor_binario = bin(j)[2:].zfill(num_digitos)

            dicionario[caracteres_embaralhados[j]] = valor_binario

        dicionarios.append(dicionario)

    # Pedir ao usuário o nome para salvar o arquivo
    nome_arquivo_dicionario = input("Digite o nome para salvar o arquivo do dicionário: ")
    nome_arquivo_dicionario_completo = f"{nome_arquivo_dicionario}.txt"

    try:
        with open(nome_arquivo_dicionario_completo, 'wb') as arquivo_dicionario:
            pickle.dump(dicionarios, arquivo_dicionario)
        print("Dicionários criados e salvos com sucesso.")
    except IOError:
        print("Erro ao salvar os dicionários.")

    return dicionarios

# Função para carregar dicionários de criptografia de um arquivo
def carregar_dicionarios_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'rb') as arquivo:
            dicionarios = pickle.load(arquivo)
        print("Dicionários carregados com sucesso.")
        return dicionarios
    except IOError:
        print("Erro ao carregar os dicionários.")
        return []



# Função para carregar dicionários de criptografia de um arquivo
def carregar_dicionarios_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'rb') as arquivo:
            dicionarios = pickle.load(arquivo)
        print("Dicionários carregados com sucesso.")
        return dicionarios
    except IOError:
        print("Erro ao carregar os dicionários.")
        return []


# Função para criptografar uma mensagem usando os dicionários de criptografia
def criptografar_mensagem(mensagem, dicionarios):
    mensagem_criptografada = ""
    iterador_dicionarios = itertools.cycle(dicionarios)
    espaco = None

    for letra in mensagem:
        if letra == ' ':
            if espaco is None:
                dicionario = next(iterador_dicionarios)
                espaco = dicionario.get(' ')
                if espaco is None:
                    espaco = dicionario[next(iter(dicionario))]
            mensagem_criptografada += espaco
        else:
            dicionario = next(iterador_dicionarios)
            if letra in dicionario:
                mensagem_criptografada += dicionario[letra]

    return mensagem_criptografada


# Função para descriptografar uma mensagem usando os dicionários de criptografia
def descriptografar_mensagem(mensagem_criptografada, dicionarios):
    mensagem_original = ""
    iterador_dicionarios = itertools.cycle(dicionarios)
    espaco = None

    while mensagem_criptografada:
        dicionario = next(iterador_dicionarios)
        num_bits = len(dicionario[next(iter(dicionario))])

        if mensagem_criptografada[:num_bits] == espaco:
            mensagem_original += ' '
            mensagem_criptografada = mensagem_criptografada[num_bits:]
        else:
            for letra, valor_binario in dicionario.items():
                if mensagem_criptografada[:num_bits] == valor_binario:
                    mensagem_original += letra
                    mensagem_criptografada = mensagem_criptografada[num_bits:]
                    break

    return mensagem_original


# Função para exibir os dicionários de criptografia
def exibir_dicionarios(dicionarios):
    for i, dicionario in enumerate(dicionarios):
        print(f"Dicionário {i+1}:")
        for chave, valor in dicionario.items():
            print(f"{chave}: {valor}")
        print()


# Função para exibir o menu
def exibir_menu():
    print("======= MENU =======")
    print("1 - Criar dicionários de criptografia")
    print("2 - Criptografar mensagem")
    print("3 - Descriptografar mensagem")
    print("4 - Exibir dicionários")
    print("5 - Baixar arquivo")
    print("6 - Upload de arquivo")
    print("7 - carregar dicionario")
    print("0 - Sair")
    print("====================")



def main():
    dicionarios = []
    dicionarios_iter = None

    host = '192.168.0.6'  # Substitua isso pelo endereço IP ou nome do servidor
    port = 5000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))

        while True:
            exibir_menu()
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                num_dicionarios = int(input("Digite o número de dicionários que você deseja criar: "))
                min_digitos = int(input("Digite o número mínimo de dígitos para cada dicionário: "))
                max_digitos = int(input("Digite o número máximo de dígitos para cada dicionário: "))
                dicionarios = criar_dicionarios_criptografia(num_dicionarios, min_digitos, max_digitos)
                dicionarios_iter = itertools.cycle(dicionarios)

            elif opcao == "2":
                if dicionarios:
                    mensagem = input("Digite a mensagem que você deseja criptografar: ")
                    mensagem_criptografada = criptografar_mensagem(mensagem, dicionarios)
                    print("Mensagem criptografada:", mensagem_criptografada)
                else:
                    print("Nenhum dicionário encontrado. Crie os dicionários primeiro.")

            elif opcao == "3":
                if dicionarios:
                    mensagem_criptografada = input("Digite a mensagem criptografada recebida: ")
                    mensagem_original = descriptografar_mensagem(mensagem_criptografada, dicionarios)
                    print("Mensagem original:", mensagem_original)
                else:
                    print("Nenhum dicionário encontrado. Crie os dicionários primeiro.")

            elif opcao == "4":
                if dicionarios:
                    exibir_dicionarios(dicionarios)
                else:
                    print("Nenhum dicionário encontrado. Crie os dicionários primeiro.")

            elif opcao == "5":
                
                    nome_arquivo = input("Digite o nome do arquivo para baixar: ")
                    baixar_arquivo(sock, nome_arquivo)
                
            elif opcao == "6":
                    caminho_arquivo = input("Digite o caminho do arquivo para upload: ")
                    enviar_arquivo(sock, caminho_arquivo)
                
            elif opcao == "7":  # Nova opção para carregar dicionário do arquivo
                nome_arquivo = input("Digite o nome do arquivo do dicionário para carregar: ")
                dicionarios = carregar_dicionarios_arquivo(nome_arquivo)
                dicionarios_iter = itertools.cycle(dicionarios)

            elif opcao == "0":
                break
            else:
                print("Opção inválida. Tente novamente.")

    except Exception as e:
        print("Erro:", e)
    finally:
        sock.close()


if __name__ == "__main__":
    main()
