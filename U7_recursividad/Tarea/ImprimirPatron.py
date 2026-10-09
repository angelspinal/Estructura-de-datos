def imprimir_patron(n, fila=1):
    if fila > n:
        return

    print("*" * fila)

    imprimir_patron(n, fila + 1)


n = int(input("Ingrese un número: "))

imprimir_patron(n)