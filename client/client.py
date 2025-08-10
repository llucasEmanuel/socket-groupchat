import os
from config.settings import SERVER_IP, SERVER_PORT
from utils.utils import receive_file, send_file, send_message, receive_message

def client_receive_file(sock, file_prefix="recv_"):
    file_prefix = os.path.join("client", "data", file_prefix)
    sender_addr = receive_file(sock, file_prefix)
    return sender_addr

def client_send_file(sock, file_name):
    file_path = os.path.join("client", "data", file_name)
    # Sempre envia para o servidor
    send_file(sock, (SERVER_IP, SERVER_PORT), file_path)

def client_receive_message(sock):
    receive_message(sock)

def client_send_message(sock, addr, message):
    send_message(sock, addr, message)

