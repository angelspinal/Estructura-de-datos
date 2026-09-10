from queue_structure import Queue

def colocar_mayor_al_fondo(cola):
    if cola.is_empty():
        print("La cola está vacía.")
        return

    cantidad = cola.size()
    mayor = cola.front()

    for _ in range(cantidad):
        elemento = cola.dequeue()
        if elemento > mayor:
            mayor = elemento
        cola.enqueue(elemento)

    auxiliar = Queue()
    eliminado = False

    for _ in range(cantidad):
        elemento = cola.dequeue()
        if elemento == mayor and not eliminado:
            eliminado = True
        else:
            auxiliar.enqueue(elemento)

    while not auxiliar.is_empty():
        cola.enqueue(auxiliar.dequeue())

    cola.enqueue(mayor)

cola = Queue()
for elemento in [8, 15, 3, 11, 6]:
    cola.enqueue(elemento)

print("Cola original:", cola)
colocar_mayor_al_fondo(cola)
print("Cola con el mayor al fondo:", cola)