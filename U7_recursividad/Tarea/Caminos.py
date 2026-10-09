def caminos_tablero(filas, columnas):
    if filas == 1 or columnas == 1:
        return 1

    return caminos_tablero(filas - 1, columnas) + caminos_tablero(filas, columnas - 1)


filas = int(input("Ingrese la cantidad de filas: "))
columnas = int(input("Ingrese la cantidad de columnas: "))

print("Cantidad de caminos:", caminos_tablero(filas, columnas))