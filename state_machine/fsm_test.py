import rdt3_sender as snd
import rdt3_receiver as rcv

def main():

    print("Sender FSM")
    sender = snd.RDT3Sender()
    sender.transition(snd.APL_CALL)
    sender.transition(snd.RCV_WRONG_ACK_0)
    sender.transition(snd.RCV_RIGHT_ACK_0)
    sender.transition(snd.RCV_ACK_ON_WAIT)
    sender.transition(snd.APL_CALL)
    sender.transition(snd.TIMEOUT)
    sender.transition(snd.RCV_RIGHT_ACK_1)

    print("\nReceiver FSM")
    receiver = rcv.RDT3Receiver()
    receiver.transition(rcv.RCV_WRONG_PKT_0)
    receiver.transition(rcv.RCV_RIGHT_PKT_0)
    receiver.transition(rcv.RCV_WRONG_PKT_1)
    receiver.transition(rcv.RCV_RIGHT_PKT_1)


if __name__ == "__main__":
    main()

