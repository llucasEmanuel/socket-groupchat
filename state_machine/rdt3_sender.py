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