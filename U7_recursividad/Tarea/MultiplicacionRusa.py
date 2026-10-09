def multiplicacion_rusa(a, b):
    if b == 0:
        return 0

    if b < 0:
        return -multiplicacion_rusa(a, -b)

    if b % 2 == 0:
        return multiplicacion_rusa(a + a, b // 2)

    return a + multiplicacion_rusa(a, b - 1)


a = int(input("Ingrese el primer número: "))
b = int(input("Ingrese el segundo número: "))

print("Resultado:", multiplicacion_rusa(a, b))