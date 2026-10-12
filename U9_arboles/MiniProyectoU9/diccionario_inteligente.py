from pathlib import Path


class Palabra:
    def __init__(self, texto, definicion):
        self.texto = texto.strip().lower()
        self.definicion = definicion.strip()

    def __str__(self):
        return f"{self.texto}: {self.definicion}"


class NodoPalabra:
    def __init__(self, palabra):
        self.palabra = palabra
        self.izquierdo = None
        self.derecho = None


class DiccionarioBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, palabra):
        if self.raiz is None:
            self.raiz = NodoPalabra(palabra)
        else:
            self._insertar_recursivo(self.raiz, palabra)

    def _insertar_recursivo(self, nodo_actual, palabra):
        if palabra.texto < nodo_actual.palabra.texto:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = NodoPalabra(palabra)
            else:
                self._insertar_recursivo(
                    nodo_actual.izquierdo,
                    palabra
                )

        elif palabra.texto > nodo_actual.palabra.texto:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = NodoPalabra(palabra)
            else:
                self._insertar_recursivo(
                    nodo_actual.derecho,
                    palabra
                )

    def buscar_exacta(self, texto):
        texto = texto.strip().lower()
        return self._buscar_exacta_recursivo(self.raiz, texto)

    def _buscar_exacta_recursivo(self, nodo_actual, texto):
        if nodo_actual is None:
            return None

        if texto == nodo_actual.palabra.texto:
            return nodo_actual.palabra

        if texto < nodo_actual.palabra.texto:
            return self._buscar_exacta_recursivo(
                nodo_actual.izquierdo,
                texto
            )

        return self._buscar_exacta_recursivo(
            nodo_actual.derecho,
            texto
        )

    def palabras_en_orden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.palabra)
            self._inorden_recursivo(nodo.derecho, resultado)

    def buscar_por_prefijo(self, prefijo):
        prefijo = prefijo.strip().lower()
        resultado = []
        self._buscar_prefijo_recursivo(
            self.raiz,
            prefijo,
            resultado
        )
        return resultado

    def _buscar_prefijo_recursivo(self, nodo, prefijo, resultado):
        if nodo is None:
            return

        self._buscar_prefijo_recursivo(
            nodo.izquierdo,
            prefijo,
            resultado
        )

        if nodo.palabra.texto.startswith(prefijo):
            resultado.append(nodo.palabra)

        self._buscar_prefijo_recursivo(
            nodo.derecho,
            prefijo,
            resultado
        )

    def cantidad_palabras(self):
        return len(self.palabras_en_orden())


def cargar_palabras(ruta_archivo):
    diccionario = DiccionarioBST()

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()

                if not linea:
                    continue

                if "|" not in linea:
                    continue

                texto, definicion = linea.split("|", 1)
                palabra = Palabra(texto, definicion)
                diccionario.insertar(palabra)

    except FileNotFoundError:
        print(f"\nNo se encontró el archivo: {ruta_archivo}")

    return diccionario


def mostrar_menu():
    print("\n" + "=" * 45)
    print("      DICCIONARIO INTELIGENTE BST")
    print("=" * 45)
    print("1. Buscar palabra exacta")
    print("2. Autocompletar por prefijo")
    print("3. Ver diccionario completo")
    print("4. Ver cantidad de palabras")
    print("5. Salir")


def ejecutar_diccionario():
    ruta_archivo = Path(__file__).parent / "palabras.txt"
    diccionario = cargar_palabras(ruta_archivo)

    if diccionario.raiz is None:
        print("No fue posible cargar las palabras.")
        return

    print(
        f"\nDiccionario cargado correctamente con "
        f"{diccionario.cantidad_palabras()} palabras."
    )

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            texto = input("Ingrese la palabra a buscar: ")
            palabra = diccionario.buscar_exacta(texto)

            if palabra is None:
                print("\nLa palabra no se encuentra en el diccionario.")
            else:
                print(f"\nPalabra: {palabra.texto}")
                print(f"Definición: {palabra.definicion}")

        elif opcion == "2":
            prefijo = input("Ingrese un prefijo: ")
            coincidencias = diccionario.buscar_por_prefijo(prefijo)

            if not coincidencias:
                print("\nNo se encontraron palabras con ese prefijo.")
            else:
                print("\nSugerencias:")
                for palabra in coincidencias:
                    print(f"- {palabra.texto}")

        elif opcion == "3":
            palabras = diccionario.palabras_en_orden()

            print("\nDICCIONARIO COMPLETO")
            print("-" * 45)

            for palabra in palabras:
                print(f"{palabra.texto}: {palabra.definicion}")

        elif opcion == "4":
            print(
                f"\nEl diccionario contiene "
                f"{diccionario.cantidad_palabras()} palabras."
            )

        elif opcion == "5":
            print("\nGracias por utilizar el Diccionario Inteligente.")
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


if __name__ == "__main__":
    ejecutar_diccionario()