import os
from utils.utils import receive_file, send_file, receive_message, send_message

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

        is_for_all = True
        output_message = f"[Server] '{username}' foi adicionado ao chat."
        # print(output_message)
        return is_for_all, output_message

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
    def send_client_list(self):
        client_names = [client.username for client in self.client_list]

        # Concatena os nomes dos clientes em uma string (usa \0 para separar cada username)
        all_names_string = "\0".join(client_names)

        # Envia apenas a string para o cliente
        return False, all_names_string

    def broadcast_message(self, message):

        for client in self.client_list:
            self.server_send_message(client.addr, message)

    def server_receive_file(self, file_prefix="recv_"):
        file_prefix = os.path.join("server", "data", file_prefix)
        sender_addr, receive_file_name = receive_file(self.sock, file_prefix)
        return sender_addr, receive_file_name

    def server_send_file(self, addr, file_name):
        file_path = os.path.join("server", "data", file_name)
        send_file(self.sock, addr, file_path)

    def server_receive_message(self):
        message, (ip, _) = receive_message(self.sock)
        # print(int.from_bytes((message[:4]).encode('latin1'), 'big'))
        return message[4:], (ip, int.from_bytes((message[:4]).encode('latin1'), 'big')) 

    def server_send_message(self, addr, message):
        # Sempre envia para o servidor
        send_message(self.sock, addr, message)
