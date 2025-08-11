import os
from utils.utils import receive_file, send_file, send_message

class ClientRegister:
    def __init__(self, username, addr):
        self.username = username
        # tupla: (ip, porta)
        self.addr = addr

class Server: 
    def __init__(self):
        # cria uma lista vazia de ClientRegister
        self.client_list = [ClientRegister]
        self.ban_list = [ClientRegister]
        
    def add_client(self, sock, username, addr):   

        # caso esteja banido
        for banned_client in self.ban_list:
            if(username == banned_client.username):

                output_message = f"\033[31m[Server] ☠️ Acesso negado ☠️: '{username}' foi banido do chat!! \033[0m"
                send_message(sock, addr, output_message)
                print(output_message)
                return
            
        # caso já exista um username igual no chat
        for client in self.client_list:
            if(username == client.username):

                output_message = f"\033[33m[Server] ⚠️ o username '{username}' já está em uso. ⚠️\033[0m"
                send_message(sock, addr, output_message)
                print(output_message)
                return

        # adicionando novo cliente
        client = ClientRegister(username, addr)
        self.client_list.append(client)  

        output_message = f"[Server] '{username}' foi adicionado ao chat."
        self.broadcast_message(sock, output_message)
        print(output_message)

    def remove_client(self, sock, username, ban_on=False):
        for client in self.client_list:

            if(username == client.username):
                self.client_list.remove(client)

                if(not ban_on):
                    output_message = f"[Server] '{username}' saiu do chat."
                    print(output_message)
                    self.broadcast_message(sock, output_message)
                else:
                    print(f"[Server] '{username}' foi removido do chat.")

                return

        output_message = "\033[33m[Server] ⚠️ Ocorreu um erro, não foi possível remover o usuário. ⚠️\033[0m"
        print(output_message)
                
    # Envia a lista de clientes para o cliente de endereço addr que usou /list
    def send_client_list(self, sock, addr):
        client_names = [client.username for client in self.client_list]

        # Concatena os nomes dos clientes em uma string (usa \0 para separar cada username)
        all_names_string = "\0".join(client_names)

        # Envia apenas a string para o cliente
        send_message(sock, addr, all_names_string)

    def broadcast_message(self, sock, message):

        for client in self.client_list:
            send_message(sock, client.addr, message)

class ClientRegister:
    def __init__(self, username, addr):
        self.username = username
        # tupla: (ip, porta)
        self.addr = addr

class Server: 
    def __init__(self):
        # cria uma lista vazia de ClientRegister
        self.client_list = [ClientRegister]
        self.ban_list = [ClientRegister]

    def send_client_list(self, sock, addr):
        # precisamos da função de enviar mensagem
        pass
        
    def add_client(self, username, addr):   

        # caso esteja banido
        for banned_client in self.ban_list:
            if(username == banned_client.username):
                print(f"\033[31m ☠️ Acesso negado ☠️: {username} foi banido do chat!! \033[0m")
                return
            
        # caso já exista um username igual no chat
        for client in self.client_list:
            if(username == client.username):
                print(f"\033[33m ⚠️ o username '{username}' já está em uso. ⚠️\033[0m")
                return

        # adicionando novo cliente
        client = ClientRegister(username, addr)
        self.client_list.append(client)
        
        # TODO: notificar clientes que o novo cliente foi adicionado no chat

def server_receive_file(sock, file_prefix="recv_"):
    file_prefix = os.path.join("server", "data", file_prefix)
    sender_addr, receive_file_name = receive_file(sock, file_prefix)
    return sender_addr, receive_file_name

def server_send_file(sock, addr, file_name):
    file_path = os.path.join("server", "data", file_name)
    send_file(sock, addr, file_path)