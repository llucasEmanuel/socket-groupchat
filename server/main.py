import socket
from config.settings import SERVER_IP, SERVER_PORT
from server.server import server_receive_file, server_send_file

from utils.utils import receive_message, send_message

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"Servidor iniciado em {SERVER_IP}:{SERVER_PORT}")

    while True:
        try:
            message, addr = receive_message(sock)
            print("recebeu: " + message)
            if(message == "destroy the mainframe"):
                break
            message = message + "?"
            print("enviando: " + message)
            send_message(sock, addr, message)
        except TimeoutError:
            ...

    sock.close()

if __name__ == "__main__":
    main()