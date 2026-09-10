from queue_structure import Queue

def imprimir_tamano(cola):
    print("Cantidad de elementos:", cola.size())


cola = Queue()
for elemento in [10, 20, 30, 40]:
    cola.enqueue(elemento)

print("Cola:", cola)
imprimir_tamano(cola)