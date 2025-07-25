from config.settings import BUFFER_SIZE
from utils.rdt_utils import ONE_1, ZERO_1, ONE_B, ZERO_B, send_with_loss_sim

# Estados do transmissor RDT3.0 
WAIT_APL_0 = "WAIT_APL_0"
WAIT_APL_1 = "WAIT_APL_1"
WAIT_ACK_0 = "WAIT_ACK_0"
WAIT_ACK_1 = "WAIT_ACK_1"

class RDT3Sender:
    def __init__(self, initial_state=WAIT_APL_0):
        # Estado inicial
        self.__state = initial_state
        # Estados possíveis que caad estado pode transicionar
        self.__transitions = {
            WAIT_APL_0: {
                # Recebe ACK no estado de WAIT_APL_0
                WAIT_APL_0,
                # Recebe chamada da camada de aplicação para envio de pacote 0
                WAIT_ACK_0
            },
            WAIT_ACK_0: {
                # Recebe ACK 1 ou corrompido
                WAIT_ACK_0,
                # Timeout
                WAIT_ACK_0,
                # Recebe ACK 0
                WAIT_APL_1
            },
            WAIT_APL_1: {
                # Recebe ACK no estado de WAIT_APL_1
                WAIT_APL_1,
                # Recebe chamada da camada de aplicação para envio de pacote 1
                WAIT_ACK_1
            },
            WAIT_ACK_1: {
                # Recebe ACK 0 ou corrompido
                WAIT_ACK_1,
                # Timeout
                WAIT_ACK_1,
                # Recebe ACK 1
                WAIT_APL_0
            }
        }

    def transition(self, new_state):
        target_states = self.__transitions[self.__state]

        if new_state in target_states:
            print(f"({self.__state}) ---> ({new_state})")
            self.__state = new_state
        else:
            raise KeyError(f"Transição inválida do estado '{self.__state}' para o estado '{new_state}'")

    def get_state(self):
        return self.__state
    
    def rdt_send(self, sock, addr, data):
        while True:
            # Estado de envio do arquivo 0
            if self.__state == WAIT_APL_0: 
                # Envia segmento e vai para estado de espera
                send_with_loss_sim(sock, ZERO_1 + data, addr)
                self.transition(WAIT_ACK_0)
            # Estado de espera do ack 0
            elif self.__state == WAIT_ACK_0: 
                # Tenta receber ack
                try: 
                    ack, _ = sock.recvfrom(BUFFER_SIZE)
                    # Se receber ack correto, encerra laço
                    if ack == ZERO_B:
                        self.transition(WAIT_APL_1)
                        break
                    elif ack == ONE_B:
                        # Se mantém no mesmo estado
                        self.transition(WAIT_ACK_0)
                    else:
                        break
                # Se houver timeout, reenvia pacote
                except TimeoutError:
                    send_with_loss_sim(sock, ZERO_1 + data, addr)
                    print("Ocorreu timeout, pacote reenviado")
            # Estado de envio do arquivo 1
            elif self.__state == WAIT_APL_1: 
                # Envia segmento e vai para estado de espera
                send_with_loss_sim(sock, ONE_1 + data, addr)
                self.transition(WAIT_ACK_1)
            # Estado de espera do ack 1
            elif self.__state == WAIT_ACK_1: 
                # Tenta receber ack
                try:
                    ack, _ = sock.recvfrom(BUFFER_SIZE)
                    # Se receber ack correto, encerra laço
                    if ack == ONE_B:
                        self.transition(WAIT_APL_0)
                        break
                    elif ack == ZERO_B:
                        # Se mantém no mesmo estado
                        self.transition(WAIT_ACK_1)
                    else:
                        break
                # Se houver timeout, reenvia pacote
                except TimeoutError:
                    send_with_loss_sim(sock, ONE_1 + data, addr)
                    print("Ocorreu timeout, pacote reenviado")