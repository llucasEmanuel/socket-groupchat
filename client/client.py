import os
from config.settings import SERVER_IP, SERVER_PORT
from utils.utils import receive_file, send_file, receive_message, send_message
from utils.rdt_utils import kill, set_kill
from utils.utils import comandos

def client_receive_file(sock, file_prefix="recv_"):
    file_prefix = os.path.join("client", "data", file_prefix)
    sender_addr = receive_file(sock, file_prefix)
    return sender_addr

def client_send_file(sock, file_name):
    file_path = os.path.join("client", "data", file_name)
    # Sempre envia para o servidor
    send_file(sock, (SERVER_IP, SERVER_PORT), file_path)

def client_receive_message(sock):
    message, _ = receive_message(sock)
    return message

def client_send_message(sock, portrcv : str, message : str):
    # Sempre envia para o servidor
    send_message(sock, (SERVER_IP, SERVER_PORT), portrcv + message)

def recv_start(sock):
    client_send_message(sock, ((2025).to_bytes(4, 'big')).decode('latin1'), comandos.IGN.__str__() + "-ignore")

def client_input():
    _input = input("> ")
    split = _input.split(' ', 2) 
    command = split[0]
    argument = ""
    if len(split) > 1:
        argument = split[1]
    return _input, command, argument

def thread_receive(sock):
    while not kill():
        message = client_receive_message(sock)
        print("\n"+message+"\n> ",end="")
        if message == "-=-=-=-=-\naplicativo encerrado\n-=-=-=-=-":
            break

def thread_userinput(sock, portrcv : str):
    while not kill():

        _input, command, argument = client_input()
        if _input == "":
            continue
        
        # Envia o arquivo para o servidor a partir do socket UDP
        # cada comando deve ter uma função que será criada por outro colaborador
        if  (command == "/ola"):
            # print("comando: " + command + ", argumento: " + argument)
            client_send_message(sock, portrcv,
                                comandos.OLA.__str__() + "-" + argument)
        elif(command == "/tchau"):
            print("comando: " + command)
            client_send_message(sock, portrcv,
                                comandos.TCHAU.__str__() + "-" + argument)
        elif(command == "/list"):
            print("comando: " + command)
            client_send_message(sock, portrcv,
                                comandos.LIST.__str__() + "-")
        elif(command == "/friends"):
            print("comando: " + command)
            client_send_message(sock, portrcv,
                                comandos.FRIENDS.__str__() + "-")
        elif(command == "/add"):
            # print("comando: " + command + ", argumento: " + argument)
            client_send_message(sock, portrcv,
                                comandos.ADD.__str__() + "-" + argument)
        elif(command == "/rmv"):
            # print("comando: " + command + ", argumento: " + argument)
            client_send_message(sock, portrcv, 
                                comandos.RMV.__str__() + "-" + argument)
        elif(command == "/ban"):
            # print("comando: " + command + ", argumento: " + argument)
            client_send_message(sock, portrcv, 
                                comandos.BAN.__str__() + "-" + argument)
        elif(command == "/help"):
            # print("comando: " + command)
            client_send_message(sock, portrcv, 
                                comandos.HELP.__str__() + "-")
        elif(command == "/kill"):
            print("-=-=-=-=-\naplicativo encerrado\n-=-=-=-=-") 
            set_kill(True) # encerra o aplicativo
            # client_send_message(sock, 
            #                     comandos.KILL.__str__() + "-")
        elif(command == "/ignore"):
            # print("comando: " + command)
            client_send_message(sock, portrcv, 
                                comandos.IGN.__str__() + "-")
        else:
            print("enviando: " + _input)
            client_send_message(sock, portrcv, 
                                comandos.MSG.__str__() + "-" + _input) 
