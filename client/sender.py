import os
from config.settings import SERVER_IP, SERVER_PORT, BUFFER_SIZE

def send_file(sock, file_path):
    sock.sendto(os.path.basename(file_path).encode(), (SERVER_IP, SERVER_PORT)) # N sei se isso funcina
    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            sock.sendto(data, (SERVER_IP, SERVER_PORT))
    sock.sendto(b'EOF', (SERVER_IP, SERVER_PORT))
    print(f"Arquivo '{file_path}' enviado ao servidor.")