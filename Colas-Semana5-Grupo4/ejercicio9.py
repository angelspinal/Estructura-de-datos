from math import sqrt
from queue_structure import Queue

def crear_cola_de_raices(cola):
    cola_raices = Queue()
    cantidad = cola.size()

    for _ in range(cantidad):
        elemento = cola.dequeue()

        if elemento < 0:
            raise ValueError("No se puede calcular la raíz real de un número negativo.")

        cola_raices.enqueue(sqrt(elemento))
        cola.enqueue(elemento)

    return cola_raices

cola = Queue()
for elemento in [1, 4, 9, 16]:
    cola.enqueue(elemento)

print("Cola original:", cola)
cola_raices = crear_cola_de_raices(cola)
print("Cola original después del proceso:", cola)
print("Cola temporal con raíces:", cola_raices)