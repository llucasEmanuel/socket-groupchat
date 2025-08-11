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

    # Envia a lista de clientes para o cliente de endereço addr que usou /list
    def send_client_list(self, sock, addr):
        client_names = [client.username for client in self.client_list]

        # Concatena os nomes dos clientes em uma string (usa \0 para separar cada username)
        all_names_string = "\0".join(client_names)

        # Envia apenas a string para o cliente
        send_message(sock, addr, all_names_string)


def server_receive_file(sock, file_prefix="recv_"):
    file_prefix = os.path.join("server", "data", file_prefix)
    sender_addr, receive_file_name = receive_file(sock, file_prefix)
    return sender_addr, receive_file_name

def server_send_file(sock, addr, file_name):
    file_path = os.path.join("server", "data", file_name)
    send_file(sock, addr, file_path)