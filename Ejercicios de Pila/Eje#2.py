def agregar_nombre(pila):
    nombre = input("Ingrese el primer nombre: ").strip().capitalize()
    if nombre:
        pila.append(nombre)
        print(f"'{nombre}' agregado a la pila.")
    else:
        print("El nombre no puede estar vacío.")

def eliminar_nombre(pila):
    if not pila:
        print("La pila está vacía. No hay elementos para eliminar.")
    else:
        eliminado = pila.pop()
        print(f"'{eliminado}' ha sido eliminado del tope de la pila.")

def mostrar_cima(pila):
    if not pila:
        print("La pila está vacía.")
    else:
        print(f"Elemento en la cima (tope): {pila[-1]}")

def buscar_elemento(pila):
    if not pila:
        print("La pila está vacía.")
        return
    nombre_buscar = input("Ingrese el nombre a buscar: ").strip().capitalize()
    if nombre_buscar in pila:
        posicion_desde_cima = list(reversed(pila)).index(nombre_buscar) + 1
        print(f"'{nombre_buscar}' se encuentra en la pila (Posición {posicion_desde_cima} desde la cima).")
    else:
        print(f"'{nombre_buscar}' no se encuentra en la pila.")

def contar_elementos(pila):
    print(f"Total de nombres en la pila: {len(pila)}")

def mostrar_elementos(pila):
    if not pila:
        print("La pila está vacía.")
    else:
        print("\n--- Elementos en la Pila (Cima -> Base) ---")
        for nombre in reversed(pila):
            print(f"| {nombre:<10} |")
        print("--------------")

def limpiar_pila(pila):
    pila.clear()
    print("La pila ha sido vaciada por completo.")

def menu_principal():
    pila_nombres = []
    
    while True:
        print("\n****Menú de Opciones*****")
        print("1. Agregar un nombre a la Pila")
        print("2. Eliminar un nombre a la Pila")
        print("3. Mostrar el último elemento en la Cima")
        print("4. Buscar un elemento en la Pila")
        print("5. Contar cuantos elementos tiene la Pila")
        print("6. Mostrar todos los elementos de la pila")
        print("7. Limpiar la Pila")
        print("8. Salir")
        
        opcion = input("Seleccione una opción (1-8): ").strip()
        print("-" * 30)
        
        if opcion == "1":
            agregar_nombre(pila_nombres)
        elif opcion == "2":
            eliminar_nombre(pila_nombres)
        elif opcion == "3":
            mostrar_cima(pila_nombres)
        elif opcion == "4":
            buscar_elemento(pila_nombres)
        elif opcion == "5":
            contar_elementos(pila_nombres)
        elif opcion == "6":
            mostrar_elementos(pila_nombres)
        elif opcion == "7":
            limpiar_pila(pila_nombres)
        elif opcion == "8":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente del 1 al 8.")

if __name__ == "__main__":
    menu_principal() 