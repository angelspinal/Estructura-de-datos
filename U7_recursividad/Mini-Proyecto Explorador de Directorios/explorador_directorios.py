class ExploradorRecursivo:
    def imprimir_arbol(self, sistema, nivel=0):
        if not sistema:
            return

        for nombre, contenido in sistema.items():
            sangria = "    " * nivel

            if isinstance(contenido, dict):
                print(f"{sangria}📁 {nombre}")
                self.imprimir_arbol(contenido, nivel + 1)
            else:
                print(f"{sangria}📄 {nombre} ({contenido})")

    def buscar_archivo(self, sistema, nombre, ruta=""):
        if not sistema:
            return None

        for nombre_actual, contenido in sistema.items():
            ruta_actual = f"{ruta}/{nombre_actual}" if ruta else nombre_actual

            if isinstance(contenido, dict):
                resultado = self.buscar_archivo(
                    contenido,
                    nombre,
                    ruta_actual
                )

                if resultado is not None:
                    return resultado

            elif nombre_actual == nombre:
                return ruta_actual

        return None

    def contar_archivos(self, sistema):
        if not sistema:
            return 0

        total = 0

        for contenido in sistema.values():
            if isinstance(contenido, dict):
                total += self.contar_archivos(contenido)
            else:
                total += 1

        return total


sistema_archivos = {
    "Documentos": {
        "apuntes.txt": "10kb",
        "fotos": {
            "vacaciones.png": "2mb",
            "perro.jpg": "1mb"
        }
    },
    "Proyectos": {
        "recursividad.py": "5kb",
        "presentacion.pptx": "3mb"
    },
    "sistema.dll": "500kb"
}

explorador = ExploradorRecursivo()

print("ÁRBOL DE DIRECTORIOS")
explorador.imprimir_arbol(sistema_archivos)

archivo_buscado = input("\nIngrese el nombre del archivo a buscar: ")

ruta = explorador.buscar_archivo(
    sistema_archivos,
    archivo_buscado
)

if ruta is not None:
    print(f"\nArchivo encontrado en: {ruta}")
else:
    print("\nEl archivo no fue encontrado.")

total_archivos = explorador.contar_archivos(sistema_archivos)

print(f"\nCantidad total de archivos: {total_archivos}")