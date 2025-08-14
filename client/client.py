import os
from config.settings import SERVER_IP, SERVER_PORT
from utils.utils import receive_file, send_file, receive_message, send_message
from utils.rdt_utils import kill, set_kill
from utils.utils import comandos

from datetime import datetime

# TODO add value to command encoding from comandos enum
class Client:
    def __init__(self, sock_send, sock_recv):
        self.friend_list = []
        self.sock_send = sock_send
        self.sock_recv = sock_recv
        self.online = False
    
    def _inputprint(self):
        if(self.online):
            return "\033[32m> \033[0m"
        else:
            return "> "

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
            elif (command == str(comandos.VOTE)):
                message = "voto para banir " + argument
            else: 
                message = argument
            
            print("\n"+message+"\n" + self._inputprint(),end="")
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
                    if(not self.online):
                        self.client_send_message(portrcv,
                                            str(comandos.OLA) + "-" + argument)
                        self.online = True
                elif(command == "/tchau"):
                    if(self.online):
                        self.client_send_message(portrcv,
                                            str(comandos.TCHAU) + "-" + argument)
                        self.online = False
                elif(command == "/list"):
                    if(self.online):
                        self.client_send_message(portrcv,
                                            str(comandos.LIST) + "-")
                elif(command == "/friends"):
                    # ser lista de amigos conectados (?)
                    self.client_send_message(portrcv,
                                        str(comandos.FRIENDS) + "-")
                elif(command == "/add"):
                    if(self.online):
                        self.client_send_message(portrcv,
                                            str(comandos.ADD) + "-" + argument)
                elif(command == "/rmv"):
                    self.client_send_message(portrcv, 
                                        str(comandos.RMV) + "-" + argument)
                elif(command == "/ban"):
                    if(self.online):
                        self.client_send_message(portrcv, 
                                            str(comandos.BAN) + "-" + argument)
                elif(command == "/vote"):
                    if(self.online):
                        if argument.lower() in ['y', 'n']:
                            self.client_send_message(portrcv, 
                                                str(comandos.VOTE) + "-" + argument.lower())
                        else:
                            print("Uso: /vote y ou /vote n")
                    else:
                        print("Você precisa estar conectado para votar.")
                elif(command == "/help"):
                    # lista os comandos disponíveis a depender do status do usuário
                    # TODO fazer um print pra cada linha
                    print(
                        "comandos disponíveis: \n\t/ola <nome> \n\t\t(entra no chat) \n\t/tchau \n\t\t(sai do chat) \n\t/list \n\t\t(lista pessoas online no chat) \n\t/friends \n\t\t(lista amigos) \n\t/add <user> \n\t\t(adiciona amigo) \n\t/rmv <user> \n\t\t(remove amigo) \n\t/ban <user> \n\t\t(inicia votação para banir usuario) \n\t/vote <y|n> \n\t\t(vota para banir usuario) \n\t/kill \n\t\t(fecha aplicativo) \n\t/help"
                    )
                elif(command == "/kill"):
                    set_kill(True) # encerra o aplicativo
                    self.client_send_message(portrcv,
                                        str(comandos.KILL) + "-")
                    print("-=-=-=-=-\naplicativo encerrado\n-=-=-=-=-") 
                elif(command == "/ignore"):
                    self.client_send_message(portrcv, 
                                        str(comandos.IGN) + "-")
                else:
                    print("enviando: " + _input)
                    self.client_send_message(portrcv, 
                                        str(comandos.MSG) + "-" + _input) 
            except:
                print("\033[33mOcorreu um erro de conexão...\033[0m")

    def client_input(self):
        _input = input(self._inputprint())
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
