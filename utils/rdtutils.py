from config.settings import BUFFER_SIZE
from random import random

ONE_1 = (1).to_bytes(1, 'big')
ZERO_1 = (0).to_bytes(1, 'big')
ONE_B = (1).to_bytes(BUFFER_SIZE, 'big')
ZERO_B = (0).to_bytes(BUFFER_SIZE, 'big')

LOSS_P = 0.5
def loss_sym(sock, data, addr):
    # print(f"enviando mensagem de tamanho {len(data)}")
    if random() > LOSS_P:
        sock.sendto(data, addr)
    else:
        print("Pacote não foi enviado")