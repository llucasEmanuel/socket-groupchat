import socket
from config.settings import SERVER_IP, SERVER_PORT
from server.server import server_receive_file, server_send_file

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"Servidor iniciado em {SERVER_IP}:{SERVER_PORT}")

    addr, rfname = server_receive_file(sock)
    server_send_file(sock, addr, rfname)

    sock.close()

if __name__ == "__main__":
    main()