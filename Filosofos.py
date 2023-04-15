import threading #Libreria que controla hilos
import random #Libreria que genera numeros random, para las raciones de cada filosofo
import time #Libreria para trabajar con el tiempo, este es para el tiempo que damos para los retrasos 
import queue

class Tenedor:
    def __init__(self):
        self.lock = threading.Lock()

    def adquirir(self):
        self.lock.acquire()

    def liberar(self):
        self.lock.release()

class Filosofo(threading.Thread):
    def __init__(self, nombre, tenedor_izq, tenedor_der, plato):
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.tenedor_izq = tenedor_izq
        self.tenedor_der = tenedor_der
        self.plato = plato

    def pensar(self):
        print(f"{self.nombre} está pensando")
        time.sleep(random.randint(1, 5))

    def comer(self):
        print(f"{self.nombre} está tratando de comer")
        tenedor_izq_disp = self.tenedor_izq.lock.acquire(blocking=False)
        tenedor_der_disp = self.tenedor_der.lock.acquire(blocking=False)
        if tenedor_izq_disp and tenedor_der_disp:
            print(f"{self.nombre} ha tomado los tenedores")
            while self.plato > 0:
                self.plato -= 1
                print(f"{self.nombre} comió un bocado")
                time.sleep(random.randint(1, 3))
            self.tenedor_der.liberar()
            self.tenedor_izq.liberar()
            print(f"{self.nombre} ha terminado de comer")
        else:
            if tenedor_izq_disp:
                self.tenedor_izq.liberar()
            if tenedor_der_disp:
                self.tenedor_der.liberar()
            print(f"{self.nombre} no puede comer")

    def run(self):
        while True:
            self.pensar()
            self.comer()

if __name__ == "__main__":
    n = int(input("Ingrese la cantidad de filósofos: "))
    tenedores = [Tenedor() for i in range(n)]
    filosofos = []
    for i in range(n):
        plato = random.randint(1, 10)
        filosofo = Filosofo(f"Filósofo {i+1}", tenedores[i], tenedores[(i+1)%n], plato)
        filosofos.append(filosofo)
    for filosofo in filosofos:
        filosofo.start()
