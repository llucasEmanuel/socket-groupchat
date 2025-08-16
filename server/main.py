import socket
from config.settings import SERVER_IP, SERVER_PORT
from server.server import Server

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"Servidor iniciado em {SERVER_IP}:{SERVER_PORT}")

    server = Server(sock)

    server._loop_sending_message()

    server.sock.close()

if __name__ == "__main__":
    main()
