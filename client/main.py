import socket
import threading
from client.client import Client

def main():
<<<<<<< HEAD
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Mude para o nome do arquivo que quer enviar para o servidor (deve estar na pasta client/data/)
    file_name = "ah_eh.jpg"
=======
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
>>>>>>> 928fbc915c3d0a1da935e552fd522bf667532ef5

    client = Client(sock_send, sock_recv)
    try:
        client.recv_start()
    except:
        print("Erro iniciando conexão...")
        exit(1)

    portrcv = ((client.sock_recv.getsockname()[1]).to_bytes(4, 'big')).decode('latin1')

    thread_entrada = threading.Thread(target=client.thread_userinput, args=[portrcv])
    thread_receiver = threading.Thread(target=client.thread_receive)
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
