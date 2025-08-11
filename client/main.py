import socket
import threading
from client.client import thread_receive, thread_userinput
from utils.utils import comandos

def main():
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    thread_entrada = threading.Thread(target=thread_userinput, args=[sock_send])
    thread_receiver = threading.Thread(target=thread_receive, args=[sock_send])
    thread_entrada.daemon = True
    thread_receiver.daemon = True

    # Start each thread
    thread_entrada.start()
    thread_receiver.start()

    # Wait for all threads to finish
    thread_entrada.join()
    thread_receiver.join()

    sock_send.close()
    sock_recv.close()

if __name__ == "__main__":
    main()