from queue_structure import Queue

def colocar_primer_nombre_a_al_frente(cola):
    if cola.is_empty():
        print("La cola está vacía.")
        return

    cantidad = cola.size()
    nombre_a = None
    auxiliar = Queue()

    for _ in range(cantidad):
        elemento = cola.dequeue()
        if nombre_a is None and isinstance(elemento, str) and elemento.upper().startswith("A"):
            nombre_a = elemento
        else:
            auxiliar.enqueue(elemento)

    if nombre_a is None:
        while not auxiliar.is_empty():
            cola.enqueue(auxiliar.dequeue())
        print("No se encontró un nombre que inicie con A.")
        return

    cola.enqueue(nombre_a)
    while not auxiliar.is_empty():
        cola.enqueue(auxiliar.dequeue())


cola = Queue()
for nombre in ["Luis", "Carlos", "Ana", "Beatriz"]:
    cola.enqueue(nombre)

print("Cola original:", cola)
colocar_primer_nombre_a_al_frente(cola)
print("Cola con el primer nombre con A al frente:", cola)