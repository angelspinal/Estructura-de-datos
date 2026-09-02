def agregar_numero(pila):
    try:
        num = int(input("Ingrese un número entero: "))
        pila.append(num)
        print(f"Número {num} agregado correctamente.")
    except ValueError:
        print("Error: Debe ingresar un número entero válido.")

def contar_elementos(pila):
    print(f"Total de elementos en la pila: {len(pila)}")

def mostrar_elementos(pila):
    if not pila:
        print("La pila está vacía.")
    else:
        print("Elementos en la pila (del tope a la base):")
        for elemento in reversed(pila):
            print(f"| {elemento} |")
        print("-----")

def calcular_promedio(pila):
    if not pila:
        print("La pila está vacía. No se puede calcular el promedio.")
    else:
        promedio = sum(pila) / len(pila)
        print(f"El promedio de los elementos es: {promedio:.2f}")

def menu_principal():
    pila = []
    
    while True:
        print("\n****Menú de Opciones*****")
        print("1. Agregar números")
        print("2. Contar elementos")
        print("3. Mostrar todos los elementos")
        print("4. Promedio de todos los números")
        print("5. Salir del sistema")
        
        opcion = input("Seleccione una opción (1-5): ")
        print("-" * 25)
        
        if opcion == "1":
            agregar_numero(pila)
        elif opcion == "2":
            contar_elementos(pila)
        elif opcion == "3":
            mostrar_elementos(pila)
        elif opcion == "4":
            calcular_promedio(pila)
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# Punto de entrada del programa
if __name__ == "__main__":
    menu_principal()