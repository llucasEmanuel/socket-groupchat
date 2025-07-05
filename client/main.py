import socket
from client.client import client_receive_file, client_send_file

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Mude para o nome do arquivo que quer enviar para o servidor (deve estar na pasta client/data/)
    file_name = "abacaxi.txt"

    # Envia o arquivo para o servidor a partir do socket UDP
    client_send_file(sock, file_name)

    # Recebe de volta o arquivo do servidor com o nome modificado e armazena em client/data
    client_receive_file(sock)

    sock.close()

if __name__ == "__main__":
    main()