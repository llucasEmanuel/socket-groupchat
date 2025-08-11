import os
from config.settings import SERVER_IP, SERVER_PORT
from utils.utils import receive_file, send_file, send_message, receive_message

class Client:
    def __init__(self):
        self.friend_list = []

    def get_client_list(self, sock):
        # client_names_str terá o formato "<user1>\0<user2>\0<user3>"
        client_names_str = receive_message(sock)
        name_list = client_names_str.split('\0')
        return name_list
    
    # O recomendado é chamar o get_client_list antes de chamar essa função
    def print_client_list(self, name_list):
        print("==== LISTA DE USUÁRIOS ====")

        for i, username in enumerate(name_list):
            print(f"{i+1} - {username}")

class Client:
    def __init__(self):
        self,friend_list = []

def client_receive_file(sock, file_prefix="recv_"):
    file_prefix = os.path.join("client", "data", file_prefix)
    sender_addr = receive_file(sock, file_prefix)
    return sender_addr

def client_send_file(sock, file_name):
    file_path = os.path.join("client", "data", file_name)
    # Sempre envia para o servidor
    send_file(sock, (SERVER_IP, SERVER_PORT), file_path)
