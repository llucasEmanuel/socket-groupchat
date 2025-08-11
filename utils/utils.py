import os
from config.settings import BUFFER_SIZE, HEADER_SIZE
from state_machine.rdt3_receiver import RDT3Receiver
from state_machine.rdt3_sender import RDT3Sender

DATA_SIZE = BUFFER_SIZE - HEADER_SIZE

def receive_file(sock, file_prefix):

    # Inicializa receiver rdt3.0
    receiver = RDT3Receiver()
    sock.settimeout(1)

    print("\nInício do receptor")

    # Recebe primeiro o nome do arquivo
    file_name, addr = receiver.rdt_receive(sock)
    file_name = file_name.decode()
    # Renomeia o arquivo
    received_file_name = file_prefix + file_name

    # Recebe tamanho do arquivo
    size, _ = receiver.rdt_receive(sock)
    size = int.from_bytes(size, 'big')

    print("Nome do arquivo sendo recebido: " + received_file_name)
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
        sender = RDT3Sender()
        sock.settimeout(1)

        print("\nInício do transmissor")
        # Envia primeiro o nome do arquivo
        file_name = os.path.basename(file_path)
        sender.rdt_send(sock, addr, file_name.encode())

        # Envia tamanho do arquivo
        size = os.path.getsize(file_path)
        sender.rdt_send(sock, addr, size.to_bytes(4, 'big'))

        print("Nome do arquivo sendo enviado: " + file_path)
        print(f"Tamanho do arquivo sendo enviado: {size}")

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
    
def send_message(sock, addr, message):
    # Inicializa sender rdt3.0
    sender = RDT3Sender()
    sock.settimeout(1)
    # print("\nEnviando mensagem...")

    #sender.rdt_send(sock, addr, HANDSHAKE)
    #while(recebe_resposta() == NEGA_HANDSHAKE):
    #    espera um segundo
    #    manda dnovo

    # Envia os dados do arquivo
    while True:
        data = message[:DATA_SIZE]
        message = message[DATA_SIZE:]
        # print("sending: '" + data + "'")
        if not data:
            break
        sender.rdt_send(sock, addr, data.encode())

    # Envia o marcador do fim do arquivo
    sender.rdt_send(sock, addr, b'EOF')
    # print("Mensagem enviada com sucesso")

def receive_message(sock):
    # Inicializa receiver rdt3.0
    receiver = RDT3Receiver()
    sock.settimeout(1)
    # print("\nRecebendo mensagem...")
    message = ""
    addr = 0

    # Recebe os dados até o EOF
    while True:
        data, addr = receiver.rdt_receive(sock)
        if data == b'EOF':
            break
        message += data.decode()
    
    # print("Mensagem recebida com sucesso")
    return message, addr