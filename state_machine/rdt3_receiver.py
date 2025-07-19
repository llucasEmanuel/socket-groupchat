# RDT3.0 Receiver states
WAIT_PKT_0 = "WAIT_PKT_0"
WAIT_PKT_1 = "WAIT_PKT_1"

# Transitions available
RCV_RIGHT_PKT_0 = "RCV_RIGHT_PKT_0"
RCV_RIGHT_PKT_1 = "RCV_RIGHT_PKT_1"
RCV_WRONG_PKT_0 = "RCV_WRONG_PKT_0"
RCV_WRONG_PKT_1 = "RCV_WRONG_PKT_1"

class RDT3Receiver:
    def __init__(self):
        # initial_state
        self.__state = WAIT_PKT_0
        self.__transitions = {
            WAIT_PKT_0: {
                # Packet 0 received at the wait 0 state
                RCV_RIGHT_PKT_0: WAIT_PKT_1,
                # Packet 1 or corrupt packet received at the wait 0 state
                RCV_WRONG_PKT_0: WAIT_PKT_0,
            },
            WAIT_PKT_1: {
                # Packet 1 received at the wait 1 state
                RCV_RIGHT_PKT_1: WAIT_PKT_0,
                # Packet 0 or corrupt packet received at the wait 1 state
                RCV_WRONG_PKT_1: WAIT_PKT_1,
            }
        }

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
        
    
