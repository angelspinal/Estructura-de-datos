from queue_structure import Queue

def eliminar_ceros(cola):
    if cola.is_empty():
        print("La cola está vacía.")
        return

    cantidad = cola.size()
    auxiliar = Queue()
    ceros = 0

    for _ in range(cantidad):
        elemento = cola.dequeue()
        if elemento == 0:
            ceros += 1
        else:
            auxiliar.enqueue(elemento)

    while not auxiliar.is_empty():
        cola.enqueue(auxiliar.dequeue())

    print("Ceros eliminados:", ceros)

cola = Queue()
for elemento in [0, 5, 0, 8, 3, 0]:
    cola.enqueue(elemento)

print("Cola original:", cola)
eliminar_ceros(cola)
print("Cola sin ceros:", cola)