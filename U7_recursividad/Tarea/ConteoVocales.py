def contar_vocales(texto, indice=0):
    if indice == len(texto):
        return 0

    vocales = "aeiouáéíóúüAEIOUÁÉÍÓÚÜ"

    if texto[indice] in vocales:
        return 1 + contar_vocales(texto, indice + 1)

    return contar_vocales(texto, indice + 1)


texto = input("Ingrese un texto: ")

print("Cantidad de vocales:", contar_vocales(texto))