# RDT3.0 Sender states
WAIT_APL_0 = "WAIT_APL_0"
WAIT_APL_1 = "WAIT_APL_1"
WAIT_ACK_0 = "WAIT_ACK_0"
WAIT_ACK_1 = "WAIT_ACK_1"

# Transitions available
APL_CALL = "APL_CALL"
RCV_WRONG_ACK_0 = "RCV_WRONG_ACK_0"
RCV_RIGHT_ACK_0 = "RCV_RIGHT_ACK_0"
RCV_WRONG_ACK_1 = "RCV_WRONG_ACK_1"
RCV_RIGHT_ACK_1 = "RCV_RIGHT_ACK_1"
RCV_ACK_ON_WAIT = "RCV_ACK_ON_WAIT"
TIMEOUT = "TIMEOUT"

class RDT3Sender:
    def __init__(self):
        self.__state = WAIT_APL_0
        self.__transitions = {
            WAIT_APL_0: {
                RCV_ACK_ON_WAIT: WAIT_APL_0,
                APL_CALL: WAIT_ACK_0
            },
            WAIT_ACK_0: {
                RCV_WRONG_ACK_0: WAIT_ACK_0,
                TIMEOUT: WAIT_ACK_0,
                RCV_RIGHT_ACK_0: WAIT_APL_1
            },
            WAIT_APL_1: {
                RCV_ACK_ON_WAIT: WAIT_APL_1,
                APL_CALL: WAIT_ACK_1
            },
            WAIT_ACK_1: {
                RCV_WRONG_ACK_1: WAIT_ACK_1,
                TIMEOUT: WAIT_ACK_1,
                RCV_RIGHT_ACK_1: WAIT_APL_0
            }
        }
        self.num = 0
        # delara timer

    def transition(self, event):
        state_transitions = self.__transitions[self.__state]
        try:
            new_state = state_transitions[event]

            print(f"({self.__state}) -> [{event}] -> ({new_state})")
            self.__state = new_state

        except KeyError:
            raise KeyError(f"Invalid transition: event '{event}' from state '{self.__state}'")

    def get_state(self):
        return self.__state
    
    def rdt_send(self, sock, addr, data):
        while True:
            if self.__state == WAIT_APL_0:
                sock.sendto(bytes(self.num) + data, addr)
                # start timer
                self.transition(WAIT_ACK_0)
            elif self.__state == WAIT_ACK_0:
                if False: # timeout()
                    sock.sendto(bytes(self.num) + data, addr)
                    # start timer
                elif True: # rcv ack 0
                    """ TODO
                    onde será recebido o ack? 
                    como será padronizado o ack 0/1?
                    """
                    # stop timer
                    self.transition(WAIT_APL_1)
                    num = 1
                    break
            elif self.__state == WAIT_APL_1:
                sock.sendto(bytes(self.num) + data, addr)
                # start timer
                self.transition(WAIT_ACK_1)
            elif self.__state == WAIT_ACK_1: