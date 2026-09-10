from queue_structure import Queue

def imprimir_frente(cola):
    if cola.is_empty():
        print("La cola está vacía.")
    else:
        print("Primer elemento:", cola.front())


cola = Queue()
for elemento in [10, 20, 30]:
    cola.enqueue(elemento)

print("Cola original:", cola)
imprimir_frente(cola)
print("Cola después del ejercicio:", cola)