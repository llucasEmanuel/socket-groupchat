from config.settings import BUFFER_SIZE
from random import random

# Números de sequência 1 e 0 truncados para 1 byte
ONE_1 = (1).to_bytes(1, 'big')
ZERO_1 = (0).to_bytes(1, 'big')
ONE_B = (1).to_bytes(BUFFER_SIZE, 'big')
ZERO_B = (0).to_bytes(BUFFER_SIZE, 'big')

# Porcentagem de haver perda de pacotes no simulador
LOSS_P = 0

# Envia o pacote com a probabilidade de perda determinada por LOSS_P
def send_with_loss_sim(sock, data, addr):
    # print(f"enviando mensagem de tamanho {len(data)}")
    if random() > LOSS_P:
        sock.sendto(data, addr)
    else:
        # print("Pacote não foi enviado")
        ...