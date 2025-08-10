import socket
from client.client import client_receive_file, client_send_file

from config.settings import SERVER_IP, SERVER_PORT
from utils.utils import receive_message, send_message

"""
// Organização dos comandos

Funcionalidade:
    /Comando argumento1 argumento2 ...

Conectar à sala:
    /ola <nome_do_usuario>
Sair da sala:
    /tchau
Exibir lista de usuários do chat:
    /list
Exibir lista de amigos:
    /friends
Adicionar usuário à lista de amigos:
    /add <nome_do_usuario>
Remover usuário da lista de amigos:
    /rmv <nome_do_usuario>
Banir usuário da sala:
    /ban <nome_do_usuario>
Listar comandos disponíveis:
    /help
Parar aplicativo:
    /kill

// Regras sobre os comandos

só pode ser chamado enquanto o usuario *não está* na sala.
    olamundo,sou
só podem ser chamados enquanto o usuário *está* na sala.
    sair, list, add, rmv e ban
podem ser chamado em *ambos* os casos
    amigos, kill, help
"""

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:

        try:
            message, _ = receive_message(sock)
            print("recebeu: " + message)
        except TimeoutError:
            ...

        # Envia o arquivo para o servidor a partir do socket UDP
        _input = input()
        split = _input.split(' ', 1) 
        command = split[0]
        argument = ""
        if len(split) > 1:
            argument = split[1]
        # cada comando deve ter uma função que será criada por outro colaborador
        if  (command == "/ola"):
            # send_message(sock, (SERVER_IP, SERVER_PORT), OLA + argument)
            print("comando: " + command)
            print("argumento: " + argument)
        elif(command == "/tchau"):
            print("comando: " + command)

        elif(command == "/list"):
            print("comando: " + command)

        elif(command == "/friends"):
            print("comando: " + command)

        elif(command == "/add"):
            print("comando: " + command)
            print("argumento: " + argument)
        elif(command == "/rmv"):
            print("comando: " + command)
            print("argumento: " + argument)
        elif(command == "/ban"):
            print("comando: " + command)
            print("argumento: " + argument)
        elif(command == "/help"):
            print("comando: " + command)

        elif(command == "/kill"):
            print("comando: " + command)
            break
        else:
            print("enviando: " + _input)
            send_message(sock, (SERVER_IP, SERVER_PORT), _input) 
            """MSG + _input"""

    sock.close()

if __name__ == "__main__":
    main()