import socket
from client.client import client_receive_file, client_send_file

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while (True):
        # Lê o comando do usuário
        string = input("> ")

        # Separa as substrings por espaço
        tokens = string.split()

        if tokens[0] == "/ola":
            if len(tokens) == 1:
                print("Nome de usuário não fornecido.")
                continue
            # Considera que o nome do usuário não tem espaço
            username = tokens[1]
            
            # Envia uma mensagem do tipo /ola para o servidor com o username

    # Mude para o nome do arquivo que quer enviar para o servidor (deve estar na pasta client/data/)
    file_name = "ah_eh.jpg"

    # Envia o arquivo para o servidor a partir do socket UDP
    client_send_file(sock, file_name)

    # Recebe de volta o arquivo do servidor com o nome modificado e armazena em client/data
    client_receive_file(sock)

    sock.close()

if __name__ == "__main__":
    main()