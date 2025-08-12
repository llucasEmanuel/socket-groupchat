import os
from config.settings import SERVER_IP, SERVER_PORT
from utils.utils import receive_file, send_file, receive_message, send_message
from utils.rdt_utils import kill, set_kill
from utils.utils import comandos

from datetime import datetime

class Client:
    def __init__(self, sock_send, sock_recv):
        self.friend_list = []
        self.sock_send = sock_send
        self.sock_recv = sock_recv

    def recv_start(self):
        send_message(self.sock_recv, (SERVER_IP, SERVER_PORT), 
                     ((2025).to_bytes(4, 'big')).decode('latin1') + str(comandos.IGN) + "-ignore")

    def thread_receive(self):
        while not kill():
            message, addr = self.client_receive_message()

            split = message.split('-', 1) # melhorar isso
            command = split[0]
            argument = "" if (len(split) <= 1) else split[1] 

            if command == str(comandos.MSG):
                hora_data = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                message = f"{argument} <{hora_data}>"
            elif command == str(comandos.LIST):
                message = self.print_client_list(argument) 
            elif (command == str(comandos.FRIENDS)):
                # lista os amigos do usuário 
                message = "lista de amigos: amigo1, amigo2" 
            elif (command == str(comandos.ADD)):
                # adiciona um usuário à lista de amigos
                message = argument + " adicionado à lista de amigos" 
            elif (command == str(comandos.RMV)):
                # remove um usuário da lista de amigos
                message = argument + " removido da lista de amigos"
            else: 
                message = argument
            
            print("\n"+message+"\n> ",end="")
            if message == "-=-=-=-=-\naplicativo encerrado\n-=-=-=-=-":
                break

    def thread_userinput(self, portrcv : str):
        while not kill():

            _input, command, argument = self.client_input()
            if _input == "":
                continue
            try:
                if(command == "abort"):
                    set_kill(True) 
                    continue 
                if  (command == "/ola"):
                    # print("comando: " + command + ", argumento: " + argument)
                    self.client_send_message(portrcv,
                                        str(comandos.OLA) + "-" + argument)
                elif(command == "/tchau"):
                    print("comando: " + command)
                    self.client_send_message(portrcv,
                                        str(comandos.TCHAU) + "-" + argument)
                elif(command == "/list"):
                    print("comando: " + command)
                    self.client_send_message(portrcv,
                                        str(comandos.LIST) + "-")
                elif(command == "/friends"):
                    # ser lista de amigos conectados
                    print("comando: " + command)
                    self.client_send_message(portrcv,
                                        str(comandos.FRIENDS) + "-")
                elif(command == "/add"):
                    # print("comando: " + command + ", argumento: " + argument)
                    self.client_send_message(portrcv,
                                        str(comandos.ADD) + "-" + argument)
                elif(command == "/rmv"):
                    # print("comando: " + command + ", argumento: " + argument)
                    self.client_send_message(portrcv, 
                                        str(comandos.RMV) + "-" + argument)
                elif(command == "/ban"):
                    # print("comando: " + command + ", argumento: " + argument)
                    self.client_send_message(portrcv, 
                                        str(comandos.BAN) + "-" + argument)
                elif(command == "/help"):
                    # lista os comandos disponíveis a depender do status do usuário
                    print("comandos disponíveis: \n\t/ola, \n\t/tchau, \n\t/list, \n\t/friends, \n\t/add <user>, \n\t/rmv <user>, \n\t/ban <user>, \n\t/help, \n\t/kill")
                elif(command == "/kill"):
                    set_kill(True) # encerra o aplicativo
                    self.client_send_message(portrcv,
                                        str(comandos.KILL) + "-")
                    print("-=-=-=-=-\naplicativo encerrado\n-=-=-=-=-") 
                elif(command == "/ignore"):
                    # print("comando: " + command)
                    self.client_send_message(portrcv, 
                                        str(comandos.IGN) + "-")
                else:
                    print("enviando: " + _input)
                    self.client_send_message(portrcv, 
                                        str(comandos.MSG) + "-" + _input) 
            except:
                print("Ocorreu um erro de conexão...")

    def client_input(self):
        _input = input("> ")
        split = _input.split(' ', 2) 
        command = split[0]
        argument = ""
        if len(split) > 1:
            argument = split[1]
        return _input, command, argument

    def client_receive_message(self):
        message, addr = receive_message(self.sock_recv)
        return message, addr

    def client_send_message(self, portrcv : str, message : str):
        # Sempre envia para o servidor
        send_message(self.sock_send, (SERVER_IP, SERVER_PORT), 
                     portrcv + message)

    def client_receive_file(self, file_prefix="recv_"):
        file_prefix = os.path.join("client", "data", file_prefix)
        sender_addr = receive_file(self.sock_recv, file_prefix)
        return sender_addr

    def client_send_file(self, file_name):
        file_path = os.path.join("client", "data", file_name)
        # Sempre envia para o servidor
        send_file(self.sock_send, (SERVER_IP, SERVER_PORT), file_path)

    def print_client_list(self, client_names_str):
        name_list = client_names_str.split('\0')

        if not name_list:
            return "Nenhum usuário conectado."

        message = "==== LISTA DE USUÁRIOS ====\n"
        for i, username in enumerate(name_list):
            message = message + f"{i+1} - {username}\n"

        return message
