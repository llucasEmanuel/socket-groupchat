import os
from config.settings import BUFFER_SIZE
from state_machine.rdt3_receiver import RDT3Receiver

def receive_file(sock, file_prefix):

    receiver = RDT3Receiver()

    # Recebe primeiro o nome do arquivo
    file_name, addr = receiver.rdt_receive(sock)

    file_name = file_name.decode()
    # Renomeia o arquivo
    received_file_name = file_prefix + file_name

    with open(received_file_name, "wb") as f:
        # Recebe os dados até o EOF
        while True:
            data, _ = receiver.rdt_receive(sock)
            if data == b'EOF':
                break
            f.write(data)
    
    # Renomeia para apenas o nome do arquivo
    received_file_name = os.path.basename(received_file_name)
    print(f"Arquivo '{file_name}' recebido e renomeado para '{received_file_name}'.")
    # Retorna (IP, porta) de quem enviou o arquivo
    return addr, received_file_name

def send_file(sock, addr, file_path):
    file_name = os.path.basename(file_path)
    # Envia primeiro o nome do arquivo
    sock.sendto(file_name.encode(), addr)
    with open(file_path, "rb") as f:
        # Envia os dados do arquivo
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            sock.sendto(data, addr)
    # Envia o marcador do fim do arquivo
    sock.sendto(b'EOF', addr)