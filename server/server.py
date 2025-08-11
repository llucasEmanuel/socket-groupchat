import os
from utils.utils import receive_file, send_file, receive_message, send_message

def server_receive_file(sock, file_prefix="recv_"):
    file_prefix = os.path.join("server", "data", file_prefix)
    sender_addr, receive_file_name = receive_file(sock, file_prefix)
    return sender_addr, receive_file_name

def server_send_file(sock, addr, file_name):
    file_path = os.path.join("server", "data", file_name)
    send_file(sock, addr, file_path)

def server_receive_message(sock):
    message, addr = receive_message(sock)
    return message, addr

def server_send_message(sock, addr, message):
    # Sempre envia para o servidor
    send_message(sock, addr, message)