import socket
from client.client import client_receive_file, client_send_file, client_receive_message, client_send_message

from config.settings import SERVER_IP, SERVER_PORT
from utils.utils import comandos

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
            message, _ = client_receive_message(sock)
            print(message)
            if message == "-=-=-=-=-\naplicativo encerrado\n-=-=-=-=-":
                break
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
            # print("comando: " + command + ", argumento: " + argument)
            client_send_message(sock, (SERVER_IP, SERVER_PORT), 
                                comandos.OLA.__str__() + "-" + argument)
        elif(command == "/tchau"):
            print("comando: " + command)
            client_send_message(sock, (SERVER_IP, SERVER_PORT), 
                                comandos.TCHAU.__str__() + "-" + argument)
        elif(command == "/list"):
            print("comando: " + command)
            client_send_message(sock, (SERVER_IP, SERVER_PORT), 
                                comandos.LIST.__str__() + "-")
        elif(command == "/friends"):
            print("comando: " + command)
            client_send_message(sock, (SERVER_IP, SERVER_PORT), 
                                comandos.FRIENDS.__str__() + "-")
        elif(command == "/add"):
            # print("comando: " + command + ", argumento: " + argument)
            client_send_message(sock, (SERVER_IP, SERVER_PORT), 
                                comandos.ADD.__str__() + "-" + argument)
        elif(command == "/rmv"):
            # print("comando: " + command + ", argumento: " + argument)
            client_send_message(sock, (SERVER_IP, SERVER_PORT), 
                                comandos.RMV.__str__() + "-" + argument)
        elif(command == "/ban"):
            # print("comando: " + command + ", argumento: " + argument)
            client_send_message(sock, (SERVER_IP, SERVER_PORT), 
                                comandos.BAN.__str__() + "-" + argument)
        elif(command == "/help"):
            # print("comando: " + command)
            client_send_message(sock, (SERVER_IP, SERVER_PORT), 
                                comandos.HELP.__str__() + "-")
        elif(command == "/kill"):
            print("-=-=-=-=-\naplicativo encerrado\n-=-=-=-=-") 
            break # encerra o aplicativo
            # client_send_message(sock, (SERVER_IP, SERVER_PORT), 
            #                     comandos.KILL.__str__() + "-")
        else:
            print("enviando: " + _input)
            client_send_message(sock, (SERVER_IP, SERVER_PORT), 
                                comandos.MSG.__str__() + "-" + _input) 

    sock.close()

if __name__ == "__main__":
    main()