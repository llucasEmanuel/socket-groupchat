import rdt3_sender as snd
import rdt3_receiver as rcv

def main():

    print("Sender FSM")
    sender = snd.RDT3Sender()
    sender.transition(snd.WAIT_APL_0)
    sender.transition(snd.WAIT_ACK_0)
    sender.transition(snd.WAIT_ACK_0)
    sender.transition(snd.WAIT_APL_1)
    sender.transition(snd.WAIT_APL_1)
    sender.transition(snd.WAIT_ACK_1)
    sender.transition(snd.WAIT_ACK_1)
    sender.transition(snd.WAIT_APL_0)
    sender.transition(snd.WAIT_APL_0)

    print("\nReceiver FSM")
    receiver = rcv.RDT3Receiver()
    receiver.transition(rcv.WAIT_PKT_0)
    receiver.transition(rcv.WAIT_PKT_1)
    receiver.transition(rcv.WAIT_PKT_1)
    receiver.transition(rcv.WAIT_PKT_0)


if __name__ == "__main__":
    main()

