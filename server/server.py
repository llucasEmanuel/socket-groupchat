import os
from utils.utils import receive_file, send_file

def server_receive_file(sock, file_prefix="recv_"):
    file_prefix = os.path.join("server", "files", file_prefix)
    sender_addr, receive_file_name = receive_file(sock, file_prefix)
    return sender_addr, receive_file_name

def server_send_file(sock, addr, file_name):
    file_path = os.path.join("server", "files", file_name)
    send_file(sock, addr, file_path)

