import os
from state_machine.banMachine import BanStateMachine
from utils.utils import receive_file, send_file, receive_message, send_message

from utils.utils import comandos

class ClientRegister:
    def __init__(self, username, addr):
        self.username = username
        # tupla: (ip, porta)
        self.addr = addr

class Server: 
    def __init__(self, sock):
        # cria uma lista vazia de ClientRegister
        self.client_list = []
        self.ban_list = []
        self.sock = sock
        self.active_Voting = False
        self.ban_Machine = BanStateMachine(self)
        
    def add_client(self, username, addr):   
        output_message = ""
        is_for_all = False
        # caso esteja banido 
        for banned_client in self.ban_list:
            if(username == banned_client.username):
                output_message = f"\033[31m[Server] ☠️ Acesso negado ☠️: '{username}' foi banido do chat!! \033[0m"
                # print(output_message) 
                return is_for_all, output_message
            
        # caso já exista um username igual no chat
        for client in self.client_list:
            if(username == client.username):

                output_message = f"\033[33m[Server] ⚠️ o username '{username}' já está em uso. ⚠️\033[0m"
                # print(output_message)
                return is_for_all, output_message

        # adicionando novo cliente
        client = ClientRegister(username, addr)
        self.client_list.append(client)
        
        self.ban_Machine.handle_client_connect()  

        is_for_all = True
        output_message = f"[Server] '{username}' foi adicionado ao chat."
        # print(output_message)
        return is_for_all, output_message

    def remove_client(self, username, ban_on=False):
        is_for_all = False 
        for client in self.client_list:

            if(username == client.username):
                self.client_list.remove(client)
                
                if not ban_on:
                    self.ban_Machine.handle_client_disconnect(username)
                
                if(not ban_on): 
                    is_for_all = True
                    output_message = f"[Server] '{username}' saiu do chat."
                else:
                    output_message = f"[Server] '{username}' foi removido do chat."
                # print(output_message)
                return is_for_all, output_message

        output_message = "\033[33m[Server] ⚠️ Ocorreu um erro, não foi possível remover o usuário. ⚠️\033[0m"
        # print(output_message)
        return is_for_all, output_message
    # Envia a lista de clientes para o cliente de endereço addr que usou /list
    def send_client_list(self):
        client_names = [client.username for client in self.client_list]

        # Concatena os nomes dos clientes em uma string (usa \0 para separar cada username)
        all_names_string = "\0".join(client_names)

        # Envia apenas a string para o cliente
        return False, all_names_string

    def find_client(self, addr):
        for client in self.client_list:
            if client.addr == addr:
                return client.username
        return "idk"

    def server_receive_message(self):
        message, (ip, _) = receive_message(self.sock)
        # print(int.from_bytes((message[:4]).encode('latin1'), 'big'))
        return message[4:], (ip, int.from_bytes((message[:4]).encode('latin1'), 'big')) 

    def is_user_banned(self, addr):
        """Verifica se um usuário está banido pelo endereço"""
        username = self.find_client(addr)
        if username == "idk":  # Se não conseguir encontrar o username, pode estar banido
            # Verifica na lista de banidos também
            for banned_client in self.ban_list:
                if banned_client.addr == addr:
                    return True
        return False

    def _loop_sending_message(self):
        while True:
            try:
                is_for_all = False
                message = ""
                command, argument, addr = self._process_received_message()

                print(f"recebeu: {command} e \"{argument}\" do endereço: {addr}")
                if self.is_user_banned(addr):
                    ban_notification = "\033[33m[Server] ⚠️ Você foi banido do chat! Sua conexão foi encerrada. ⚠️\033[0m"
                    self.server_send_message(addr, f"{8}-{ban_notification}")
                    print(f"Comando ignorado de usuário banido: {addr}")
                    continue  
                if(argument == "destroy the mainframe"):
                    break 
                elif (command == str(comandos.OLA)):
                    # coloca o usuário na lista de conectados
                    is_for_all, message = self.add_client(argument, addr)
                elif (command == str(comandos.TCHAU)):
                    # tira o usuário na lista de conectados
                    argument = self.find_client(addr) 
                    is_for_all, message = self.remove_client(argument) 
                elif (command == str(comandos.LIST)):
                    # lista os usuários conectados na sala
                    is_for_all, message = self.send_client_list()
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
                    # processa voto para banimento
                    voter_username = self.find_client(addr)
                    response = self.ban_Machine.receive_vote(voter_username, argument)
                    # Envia resposta apenas para quem votou
                    self.server_send_message(addr, f"{command}-{response}")
                    continue  # Não executa o broadcast normal
                    
                elif (command == str(comandos.BAN)):
                    # inicia a votação para banir um usuário da sala
                    target = argument
                    response = self.ban_Machine.request_ban(target)
                    # Envia resposta apenas para quem iniciou
                    self.server_send_message(addr, f"{command}-{response}")
                    continue  # Não executa o broadcast normal
                elif (command == str(comandos.KILL)): 
                    print("kill command received") 
                    argument = self.find_client(addr) 
                    is_for_all, message = self.remove_client(argument) 
                    is_for_all = True 
                    # message = "aplicativo encerrado"
                    # usuario desconecta do servidor
                elif (command == str(comandos.MSG)):
                    # print("message received")
                    is_for_all = True
                    user = self.find_client(addr) 
                    message = f"{addr}/{user}: {argument}" 
                    # envia mensagem para todos os usuários na sala
                elif (command == str(comandos.IGN)):
                    print("ignored")
                    continue
                else:
                    message = argument
                
                # se for um comando, adiciona esses símbolos para diferenciar de uma mensagem normal

                print(f"enviando: {command} {message}") 
                if is_for_all: 
                    self.broadcast_message(command + "-" + message)
                else: 
                    self.server_send_message(addr, command + "-" + message)
            except Exception as e:
                print("\033[33mOcorreu um erro: " + str(e) + "\033[0m")

    def _process_received_message(self):  
        message, addr = self.server_receive_message() 
        split = message.split('-', 1) 
        command = split[0] 
        argument = "" if (len(split) <= 1) else split[1] 
        return command, argument, addr 

    def broadcast_message(self, message):

        for client in self.client_list:
            self.server_send_message(client.addr, message)
    
    def server_send_message(self, addr, message):
        # Sempre envia para o servidor
        send_message(self.sock, addr, message)

    def server_receive_file(self, file_prefix="recv_"):
        file_prefix = os.path.join("server", "data", file_prefix)
        sender_addr, receive_file_name = receive_file(self.sock, file_prefix)
        return sender_addr, receive_file_name

    def server_send_file(self, addr, file_name):
        file_path = os.path.join("server", "data", file_name)
        send_file(self.sock, addr, file_path)
