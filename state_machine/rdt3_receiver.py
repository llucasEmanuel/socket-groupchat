from config.settings import BUFFER_SIZE
from utils.rdt_utils import send_with_loss_sim
from utils.rdt_utils import kill

# Estados do receptor RDT3.0
WAIT_PKT_0 = "WAIT_PKT_0"
WAIT_PKT_1 = "WAIT_PKT_1"

class RDT3Receiver:
    def __init__(self, initial_state=WAIT_PKT_0):
        # Estado inicial
        self.__state = initial_state
        # Estados possíveis que caad estado pode transicionar
        self.__transitions = {
            WAIT_PKT_0: [
                # Pacote 0 recebido no estado WAIT_PKT_0
                WAIT_PKT_1,
                # Pacote 1 ou corrompido recebido no estado WAIT_PKT_0
                WAIT_PKT_0,
            ],
            WAIT_PKT_1: [
                # Pacote 1 recebido no estado WAIT_PKT_1
                WAIT_PKT_0,
                # Pacote 0 ou corrompido recebido no estado WAIT_PKT_1
                WAIT_PKT_1,
            ]
        }

    def transition(self, new_state):
        target_states = self.__transitions[self.__state]

        if new_state in target_states:
            # print(f"({self.__state}) ---> ({new_state})")
            self.__state = new_state
        else:
            raise KeyError(f"Invalid transition from state '{self.__state}' to state '{new_state}'")

    def get_state(self):
        return self.__state

    def rdt_receive(self, sock):
        while True:
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)

                #if data == HANDSHAKE:
                #    teria q ser rdt_send???
                #    send_with_loss_sim(sock, NEGA_HANDSHAKE, addr)
                #    continue
                #

                if self.__state == WAIT_PKT_0:
                    seqnum = data[0]
                    payload = data[1:]

                    # Envia ack para o transmissor (número de sequência sempre é igual ao ack)
                    send_with_loss_sim(sock, seqnum.to_bytes(BUFFER_SIZE, 'big'), addr)

                    # Recebeu o número de sequência esperado
                    if seqnum == 0:
                        self.transition(WAIT_PKT_1)
                        return payload, addr

                elif self.__state == WAIT_PKT_1:
                    seqnum = data[0]
                    payload = data[1:]

                    # Envia ack para o transmissor (número de sequência sempre é igual ao ack)
                    send_with_loss_sim(sock, seqnum.to_bytes(BUFFER_SIZE, 'big'), addr)

                    # Recebeu o número de sequência esperado
                    if seqnum == 1:
                        self.transition(WAIT_PKT_0)
                        return payload, addr
            except TimeoutError:
                if kill():
                    return b'EOF', (0,0)