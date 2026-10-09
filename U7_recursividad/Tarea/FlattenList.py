def flatten_lista(lista):
    resultado = []

    for elemento in lista:
        if isinstance(elemento, list):
            resultado.extend(flatten_lista(elemento))
        else:
            resultado.append(elemento)

    return resultado


lista = [1, [2, [3, 4], 5]]

print("Lista plana:", flatten_lista(lista))