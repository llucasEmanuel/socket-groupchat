import socket
from config.settings import SERVER_IP, SERVER_PORT
from client.sender import client_receive_file, client_send_file

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    file_path = "client/abacaxi.txt"
    client_send_file(sock, file_path)

    sock.close()

if __name__ == "__main__":
    main()