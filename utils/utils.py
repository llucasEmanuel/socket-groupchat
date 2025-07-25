import os
import sys
from config.settings import BUFFER_SIZE, HEADER_SIZE
from state_machine.rdt3_receiver import RDT3Receiver
from state_machine.rdt3_sender import RDT3Sender

DATA_SIZE = BUFFER_SIZE - HEADER_SIZE

def receive_file(sock, file_prefix):

    # Inicializa receiver rdt3.0
    receiver = RDT3Receiver()
    sock.settimeout(1)

    # Recebe primeiro o nome do arquivo
    file_name, addr = receiver.rdt_receive(sock)
    file_name = file_name.decode()
    # Renomeia o arquivo
    received_file_name = file_prefix + file_name
    print("Nome do arquivo sendo recebido: " + received_file_name)

    # Recebe tamanho do arquivo
    size, _ = receiver.rdt_receive(sock)
    size = int.from_bytes(size, 'big')
    print(f"Tamanho do arquivo sendo recebido: {size}")

    with open(received_file_name, "wb") as f:
        # Recebe os dados até o EOF
        i = 0
        while True:
            data, _ = receiver.rdt_receive(sock)
            if data == b'EOF':
                break
            f.write(data)
            print(f"{100*(DATA_SIZE*i + len(data)) / size : .0f}% recebido")
            i = i+1
    
    # Renomeia para apenas o nome do arquivo
    received_file_name = os.path.basename(received_file_name)
    print(f"Arquivo '{file_name}' recebido e renomeado para '{received_file_name}'.")
    # Retorna (IP, porta) de quem enviou o arquivo
    return addr, received_file_name

def send_file(sock, addr, file_path):

    with open(file_path, "rb") as f:

        # Inicializa sender rdt3.0
        file_name = os.path.basename(file_path)
        sender = RDT3Sender()
        sock.settimeout(1)

        # Envia primeiro o nome do arquivo
        sender.rdt_send(sock, addr, file_name.encode())

        # Envia tamanho do arquivo
        size = os.path.getsize(file_path)
        print(f"tamanho do arquivo enviado: {size}")
        sender.rdt_send(sock, addr, size.to_bytes(4, 'big'))

        # Envia os dados do arquivo
        i = 0
        while True:
            data = f.read(DATA_SIZE)
            if not data:
                break
            sender.rdt_send(sock, addr, data)
            print(f"{100*(DATA_SIZE*i + len(data)) / size : .0f}% enviado")
            i = i+1

    # Envia o marcador do fim do arquivo
    sender.rdt_send(sock, addr, b'EOF')
    print(f"Arquivo '{file_name}' enviado com sucesso")