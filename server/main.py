import socket
from config.settings import SERVER_IP, SERVER_PORT
from server.server import Server
from utils.utils import comandos

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"Servidor iniciado em {SERVER_IP}:{SERVER_PORT}")

    server = Server(sock)

    while True:
        is_for_all = False
        message, addr = server.server_receive_message()
        split = message.split('-', 1) 
        command = split[0]
        argument = "" if (len(split) <= 1) else split[1] 

        print(f"recebeu: {command} e {argument} do endereço: {addr}")
        if(argument == "destroy the mainframe"):
            break
        elif (command == str(comandos.OLA)):
            # coloca o usuário na lista de conectados
            is_for_all, message = server.add_client(argument, addr)
        elif (command == str(comandos.TCHAU)):
            # tira o usuário na lista de conectados
            argument = str(addr) # buscar o nome de usuario a partir do endereço
            message = "usuario " + argument + " saiu da sala"
        elif (command == str(comandos.LIST)):
            # lista os usuários conectados na sala
            message = "lista de usuarios: \nuser1, \nuser2, \nuser3"
        elif (command == str(comandos.FRIENDS)):
            # lista os amigos do usuário
            message = "lista de amigos: amigo1, amigo2"
        elif (command == str(comandos.ADD)):
            # adiciona um usuário à lista de amigos
            message = argument + " adicionado à lista de amigos"
        elif (command == str(comandos.RMV)):
            # remove um usuário da lista de amigos
            message = argument + " removido da lista de amigos"
        elif (command == str(comandos.BAN)):
            # inicia a votação para banir um usuário da sala
            message = "votação para o banimento de " + argument + " da sala"
        elif (command == str(comandos.HELP)):
            # lista os comandos disponíveis a depender do status do usuário
            message = "comandos disponíveis: /ola, /tchau, /list, /friends, /add <user>, /rmv <user>, /ban <user>, /help, /kill"
            # se o usuario estiver conectado printa os disponiveis, se não, printa os outros 
        elif (command == str(comandos.KILL)):
            message = "aplicativo encerrado"
            # usuario desconecta do servidor
        elif (command == str(comandos.MSG)):
            message = argument
            # envia mensagem para todos os usuários na sala
        elif (command == str(comandos.IGN)):
            print("ignored")
            continue
        else:
            message = argument
        
        # se for um comando, adiciona esses símbolos para diferenciar de uma mensagem normal
        if command == str(comandos.MSG.value): 
            user = "idk" # server.find_client(addr) 
            message = f"{addr}/{user}: {message}" 
        else:
            message = "-=-\n" + message + "\n-=-"

        print(f"enviando: {command} {message}") 
        if is_for_all: 
            server.broadcast_message(command + "-" + message)
        else: 
            server.server_send_message(addr, command + "-" + message)
            
    sock.close()

if __name__ == "__main__":
    main()