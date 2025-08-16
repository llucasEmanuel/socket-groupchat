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
        self.online = False
        self.current_username = None  # Armazena o username atual
        
    def add_friend(self, username):
        """Adiciona um amigo à lista local"""
        if not username.strip():
            print("Nome de usuário não pode estar vazio.")
            return
            
        if username == self.current_username:
            print("Você não pode adicionar a si mesmo como amigo.")
            return
            
        if username in self.friend_list:
            print(f"'{username}' já está na sua lista de amigos.")
            return
            
        self.friend_list.append(username)
        print(f"'{username}' foi adicionado à sua lista de amigos.")

    def rmv_friend(self, username):
        """Remove um amigo da lista local"""
        if not username.strip():
            print("Nome de usuário não pode estar vazio.")
            return
            
        if username in self.friend_list:
            self.friend_list.remove(username)
            print(f"'{username}' foi removido da sua lista de amigos.")
        else:
            print(f"'{username}' não está na sua lista de amigos.")

    def list_friends(self):
        """Lista todos os amigos"""
        if not self.friend_list:
            print("Sua lista de amigos está vazia.")
            return
            
        print("==== LISTA DE AMIGOS ====")
        for i, friend in enumerate(self.friend_list, 1):
            print(f"{i} - {friend}")
    
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

            split = message.split('-', 1)
            command = split[0]
            argument = "" if (len(split) <= 1) else split[1]

            if command == str(comandos.MSG):
                timestamp = datetime.now().strftime("%H:%M:%S-%d/%m/%Y")
                
                # Parsing da mensagem: IP/USERNAME: texto
                sender_addr = None
                sender_username = None
                message_text = None

                if "/" in argument and ":" in argument:
                    try:
                        # Divide em IP e resto
                        sender_info, message_text = argument.split(":", 1)
                        if "/" in sender_info:
                            sender_addr, sender_username = sender_info.split("/", 1)
  
                            sender_addr = sender_addr.strip("()")
                            ip, port = sender_addr.split(",")
                            port = port.strip()
                            sender_username = sender_username.strip()
                            message_text = message_text.strip()
                        else:
                            sender_username = sender_info.strip()
                            message_text = message_text.strip()
                    except ValueError:
                        # Se não conseguir fazer parse, usa o formato original
                        message_text = argument

                # Verifica se é amigo e adiciona tag
                if sender_username and sender_username in self.friend_list:
                    display_name = f"[ amigo ] {sender_username}"
                else:
                    display_name = sender_username

                # Monta a mensagem final
                if ip and port and display_name and message_text:
                    message = f"{ip[1:-1]}:{port}/~{display_name}: {message_text} {timestamp}"
                elif display_name and message_text:
                    message = f"{display_name}: {message_text} {timestamp}"
                else:
                    message = f"{argument} {timestamp}"

            elif command == str(comandos.LIST):
                message = self.print_client_list(argument)
            else:
                message = argument
            
            print("\n"+message+"\n" + self._inputprint(), end="")
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

                if (command == "/ola"):
                    if(not self.online):
                        self.client_send_message(portrcv,
                                            str(comandos.OLA) + "-" + argument)
                        self.current_username = argument  # Armazena o username
                        self.online = True
                elif(command == "/tchau"):
                    if(self.online):
                        self.client_send_message(portrcv,
                                            str(comandos.TCHAU) + "-" + argument)
                        self.current_username = None  # Limpa o username
                        self.online = False
                elif(command == "/list"):
                    if(self.online):
                        self.client_send_message(portrcv,
                                            str(comandos.LIST) + "-")
                elif(command == "/friends"):
                    # PROCESSAMENTO LOCAL - não envia para servidor
                    self.list_friends()
                elif(command == "/add"):
                    # PROCESSAMENTO LOCAL - não envia para servidor
                    if not argument:
                        print("Uso: /add <username>")
                    else:
                        self.add_friend(argument)
                elif(command == "/rmv"):
                    # PROCESSAMENTO LOCAL - não envia para servidor
                    if not argument:
                        print("Uso: /rmv <username>")
                    else:
                        self.rmv_friend(argument)
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
                    print(
                        "comandos disponíveis: \n\t/ola <nome> \n\t\t(entra no chat) \n\t/tchau \n\t\t(sai do chat) \n\t/list \n\t\t(lista pessoas online no chat) \n\t/friends \n\t\t(lista seus amigos) \n\t/add <user> \n\t\t(adiciona amigo) \n\t/rmv <user> \n\t\t(remove amigo) \n\t/ban <user> \n\t\t(inicia votação para banir usuario) \n\t/vote <y|n> \n\t\t(vota para banir usuario) \n\t/kill \n\t\t(fecha aplicativo) \n\t/help"
                    )
                elif(command == "/kill"):
                    set_kill(True)
                    self.client_send_message(portrcv,
                                        str(comandos.KILL) + "-")
                    print("-=-=-=-=-\naplicativo encerrado\n-=-=-=-=-") 
                elif(command == "/ignore"):
                    self.client_send_message(portrcv, 
                                        str(comandos.IGN) + "-")
                else:
                    if self.online:
                        print("enviando: " + _input)
                        self.client_send_message(portrcv, 
                                            str(comandos.MSG) + "-" + _input)
                    else:
                        print("Você precisa estar conectado para enviar mensagens.")
            except Exception as e:
                print(f"\033[33mOcorreu um erro de conexão: {e}\033[0m")

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
        send_message(self.sock_send, (SERVER_IP, SERVER_PORT), 
                     portrcv + message)

    def client_receive_file(self, file_prefix="recv_"):
        file_prefix = os.path.join("client", "data", file_prefix)
        sender_addr = receive_file(self.sock_recv, file_prefix)
        return sender_addr

    def client_send_file(self, file_name):
        file_path = os.path.join("client", "data", file_name)
        send_file(self.sock_send, (SERVER_IP, SERVER_PORT), file_path)

    def print_client_list(self, client_names_str):
        name_list = client_names_str.split('\0')

        if not name_list or name_list == ['']:
            return "Nenhum usuário conectado."

        message = "==== LISTA DE USUÁRIOS ====\n"
        for i, username in enumerate(name_list):
            # Mostra se é amigo na lista também
            if username in self.friend_list:
                message += f"{i+1} - [ amigo ] {username}\n"
            else:
                message += f"{i+1} - {username}\n"

        return message