class PilaDepartamentos:
    def __init__(self):
        self.pila = []

    def agregar(self):
        departamento = input("Ingrese el nombre del departamento: ").strip().title()
        if departamento:
            self.pila.append(departamento)
            print(f"Departamento '{departamento}' agregado correctamente.")
        else:
            print("El nombre del departamento no puede estar vacío.")

    def remover(self):
        if self.esta_vacia():
            print("La pila está vacía. No hay departamentos para remover.")
        else:
            eliminado = self.pila.pop()
            print(f"Se removió '{eliminado}' del tope de la pila.")

    def imprimir_informacion(self):
        if self.esta_vacia():
            print("La pila está vacía.")
            return
        
        print("\n--- Información de la Pila ---")
        print(f"Cantidad total de departamentos: {len(self.pila)}")
        print(f"Departamento en la cima (tope): {self.pila[-1]}")
        print("\nContenido completo (Del tope a la base):")
        for i, dept in enumerate(reversed(self.pila), 1):
            print(f"{i}. {dept}")
        print("-" * 30)

    def esta_vacia(self):
        return len(self.pila) == 0


def menu():
    pila_nicaragua = PilaDepartamentos()

    while True:
        print("\n**** Menú de Opciones - Departamentos de Nicaragua ****")
        print("1. Agregar departamento")
        print("2. Remover departamento")
        print("3. Imprimir información de la pila")
        print("4. Salir")

        opcion = input("Seleccione una opción (1-4): ").strip()
        print("-" * 45)

        if opcion == "1":
            pila_nicaragua.agregar()
        elif opcion == "2":
            pila_nicaragua.remover()
        elif opcion == "3":
            pila_nicaragua.imprimir_informacion()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    menu()