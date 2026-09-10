from queue_structure import Queue

def colocar_primer_nombre_a_al_fondo(cola):
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

    while not auxiliar.is_empty():
        cola.enqueue(auxiliar.dequeue())

    if nombre_a is not None:
        cola.enqueue(nombre_a)
    else:
        print("No se encontró un nombre que inicie con A.")


cola = Queue()
for nombre in ["Luis", "Carlos", "Ana", "Beatriz"]:
    cola.enqueue(nombre)

print("Cola original:", cola)
colocar_primer_nombre_a_al_fondo(cola)
print("Cola con el primer nombre con A al fondo:", cola)