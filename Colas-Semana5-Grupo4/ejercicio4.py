from queue_structure import Queue

def colocar_menor_al_frente(cola):
    if cola.is_empty():
        print("La cola está vacía.")
        return

    cantidad = cola.size()
    menor = cola.front()

    for _ in range(cantidad):
        elemento = cola.dequeue()
        if elemento < menor:
            menor = elemento
        cola.enqueue(elemento)

    auxiliar = Queue()
    eliminado = False

    for _ in range(cantidad):
        elemento = cola.dequeue()
        if elemento == menor and not eliminado:
            eliminado = True
        else:
            auxiliar.enqueue(elemento)

    cola.enqueue(menor)

    while not auxiliar.is_empty():
        cola.enqueue(auxiliar.dequeue())

cola = Queue()
for elemento in [8, 15, 3, 11, 6]:
    cola.enqueue(elemento)

print("Cola original:", cola)
colocar_menor_al_frente(cola)
print("Cola con el menor al frente:", cola)