from utils.utils import receive_file, send_file

def server_receive_file(sock, file_prefix="recv_"):
    sender_addr = receive_file(sock, file_prefix)
    return sender_addr

def server_send_file(sock, addr, file_path):
    send_file(sock, addr, file_path)

