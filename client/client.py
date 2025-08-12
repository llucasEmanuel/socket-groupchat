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

    # O recomendado é chamar o get_client_list antes de chamar essa função
    def print_client_list(self, client_names_str):
        name_list = client_names_str.split('\0')
        message = "==== LISTA DE USUÁRIOS ====\n"

        for i, username in enumerate(name_list):
            message = message + f"{i+1} - {username}\n"
        return message

    def recv_start(self):
        send_message(self.sock_recv, (SERVER_IP, SERVER_PORT), 
                     ((2025).to_bytes(4, 'big')).decode('latin1') + str(comandos.IGN) + "-ignore")

    def client_receive_message(self):
        message, _ = receive_message(self.sock_recv)
        return message

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

    def client_input(self):
        _input = input("> ")
        split = _input.split(' ', 2) 
        command = split[0]
        argument = ""
        if len(split) > 1:
            argument = split[1]
        return _input, command, argument

    def thread_receive(self):
        while not kill():
            message = self.client_receive_message()

            split = message.split('-', 1) # melhorar isso
            command = split[0]
            argument = "" if (len(split) <= 1) else split[1] 

            if command == str(comandos.MSG):
                hora_data = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                message = f"{argument} <{hora_data}>"
            elif command == str(comandos.LIST):
                message = self.print_client_list(argument) 
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
            
            # Envia o arquivo para o servidor a partir do socket UDP
            # cada comando deve ter uma função que será criada por outro colaborador
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
                # print("comando: " + command)
                self.client_send_message(portrcv, 
                                    str(comandos.HELP) + "-")
            elif(command == "/kill"):
                print("-=-=-=-=-\naplicativo encerrado\n-=-=-=-=-") 
                set_kill(True) # encerra o aplicativo
                # self.client_send_message(
                #                     str(comandos.KILL) + "-")
            elif(command == "/ignore"):
                # print("comando: " + command)
                self.client_send_message(portrcv, 
                                    str(comandos.IGN) + "-")
            else:
                print("enviando: " + _input)
                self.client_send_message(portrcv, 
                                    str(comandos.MSG) + "-" + _input) 
