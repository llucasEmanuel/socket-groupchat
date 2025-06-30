from config.settings import SERVER_IP, SERVER_PORT
from utils.utils import receive_file, send_file

def client_receive_file(sock, file_prefix="recv_"):
    sender_addr = receive_file(sock, file_prefix)
    return sender_addr

def client_send_file(sock, file_path):
    # Sempre envia para o servidor
    send_file(sock, (SERVER_IP, SERVER_PORT), file_path)
