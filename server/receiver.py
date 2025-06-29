import os
from config.settings import BUFFER_SIZE

def receive_file(sock):
    file_name, addr = sock.recvfrom(BUFFER_SIZE)
    file_name = file_name.decode()

    with open("received_file", "wb") as f:
        while True:
            data, _ = sock.recvfrom(BUFFER_SIZE)
            if data == b'EOF':
                break
            f.write(data)
    
    print(f"Arquivo '{file_name}' recebido.")
    os.rename("received_file", "received_file_returned")
    return addr

def send_file(sock, addr):
    with open("received_file_returned", "rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            sock.sendto(data, addr)
    sock.sendto(b'EOF', addr)
