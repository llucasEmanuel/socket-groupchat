import time 

class Timer:
    def __init__(self, timeout_interval):
        self.__timeout_interval = timeout_interval
        self.__start = None
        
    def start(self):
        self.__start = time.time()

    # Retorna True se houver timeout e False caso contrário
    def timeout(self):
        return (time.time() - self.__start >= self.__timeout_interval)


    