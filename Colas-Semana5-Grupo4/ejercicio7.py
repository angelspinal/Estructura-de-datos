from queue_structure import Queue

def invertir_cola(cola):
    if cola.is_empty():
        print("La cola está vacía.")
        return

    cantidad = cola.size()
    invertida = Queue()

    for posicion in range(cantidad):
        temporal = Queue()

        for indice in range(cantidad):
            elemento = cola.dequeue()

            if indice == cantidad - posicion - 1:
                seleccionado = elemento
            else:
                temporal.enqueue(elemento)

        while not temporal.is_empty():
            cola.enqueue(temporal.dequeue())

        invertida.enqueue(seleccionado)

    while not invertida.is_empty():
        cola.enqueue(invertida.dequeue())

cola = Queue()

for elemento in [1, 2, 3, 4, 5]:
    cola.enqueue(elemento)

print("Cola original:", cola)

invertir_cola(cola)

print("Cola invertida:", cola)