import socket
from config.settings import SERVER_IP, SERVER_PORT
from server.receiver import receive_file, send_file

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"Servidor iniciado em {SERVER_IP}:{SERVER_PORT}")

    addr = receive_file(sock)
    send_file(sock, addr)

    sock.close()

if __name__ == "__main__":
    main()