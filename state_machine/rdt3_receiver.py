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
            print(f"({self.__state}) ---> ({new_state})")
            self.__state = new_state
        else:
            raise KeyError(f"Invalid transition from state '{self.__state}' to state '{new_state}'")

    def get_state(self):
        return self.__state
        
    
