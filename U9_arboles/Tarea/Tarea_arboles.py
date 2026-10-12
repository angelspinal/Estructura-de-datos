from queue import Queue


class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = NodoArbol(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual, valor):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo_actual.derecho, valor)

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return False

        if nodo_actual.valor == valor:
            return True

        if valor < nodo_actual.valor:
            return self._buscar_recursivo(nodo_actual.izquierdo, valor)

        return self._buscar_recursivo(nodo_actual.derecho, valor)

    def inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_recursivo(nodo.derecho, resultado)

    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if nodo is None:
            return None

        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_recursivo(
                nodo.izquierdo,
                valor
            )
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_recursivo(
                nodo.derecho,
                valor
            )
        else:
            if nodo.izquierdo is None and nodo.derecho is None:
                return None

            if nodo.izquierdo is None:
                return nodo.derecho

            if nodo.derecho is None:
                return nodo.izquierdo

            sucesor = self._minimo_nodo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar_recursivo(
                nodo.derecho,
                sucesor.valor
            )

        return nodo

    def _minimo_nodo(self, nodo):
        actual = nodo

        while actual.izquierdo is not None:
            actual = actual.izquierdo

        return actual

    def recorrido_por_niveles(self):
        if self.raiz is None:
            return []

        resultado = []
        cola = Queue()
        cola.put(self.raiz)

        while not cola.empty():
            nodo_actual = cola.get()
            resultado.append(nodo_actual.valor)

            if nodo_actual.izquierdo is not None:
                cola.put(nodo_actual.izquierdo)

            if nodo_actual.derecho is not None:
                cola.put(nodo_actual.derecho)

        return resultado

    def sumar_elementos(self):
        return self._sumar_elementos_recursivo(self.raiz)

    def _sumar_elementos_recursivo(self, nodo):
        if nodo is None:
            return 0

        return (
            nodo.valor
            + self._sumar_elementos_recursivo(nodo.izquierdo)
            + self._sumar_elementos_recursivo(nodo.derecho)
        )

    def es_completo(self):
        return self._es_completo_recursivo(self.raiz)

    def _es_completo_recursivo(self, nodo):
        if nodo is None:
            return True

        if nodo.izquierdo is None and nodo.derecho is None:
            return True

        if nodo.izquierdo is None or nodo.derecho is None:
            return False

        return (
            self._es_completo_recursivo(nodo.izquierdo)
            and self._es_completo_recursivo(nodo.derecho)
        )

    def balancear_arbol(self):
        valores_ordenados = self.inorden()
        arbol_balanceado = ArbolBinarioBusqueda()
        arbol_balanceado.raiz = self._construir_balanceado(
            valores_ordenados,
            0,
            len(valores_ordenados) - 1
        )
        return arbol_balanceado

    def _construir_balanceado(self, valores, inicio, fin):
        if inicio > fin:
            return None

        medio = (inicio + fin) // 2
        nodo = NodoArbol(valores[medio])

        nodo.izquierdo = self._construir_balanceado(
            valores,
            inicio,
            medio - 1
        )

        nodo.derecho = self._construir_balanceado(
            valores,
            medio + 1,
            fin
        )

        return nodo

    def altura(self, nodo=None):
        if nodo is None:
            nodo = self.raiz

        return self._altura_recursiva(nodo)

    def _altura_recursiva(self, nodo):
        if nodo is None:
            return -1

        return 1 + max(
            self._altura_recursiva(nodo.izquierdo),
            self._altura_recursiva(nodo.derecho)
        )

    def mostrar_arbol(self):
        self._mostrar_nodo(self.raiz, "", True)

    def _mostrar_nodo(self, nodo, prefijo, es_izquierdo):
        if nodo is not None:
            siguiente_prefijo = prefijo + (
                "|   " if es_izquierdo else "    "
            )

            self._mostrar_nodo(
                nodo.derecho,
                siguiente_prefijo,
                False
            )

            simbolo = "\\-- " if es_izquierdo else "/-- "
            print(prefijo + simbolo + str(nodo.valor))

            siguiente_prefijo = prefijo + (
                "    " if es_izquierdo else "|   "
            )

            self._mostrar_nodo(
                nodo.izquierdo,
                siguiente_prefijo,
                True
            )


arbol = ArbolBinarioBusqueda()

valores = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

for valor in valores:
    arbol.insertar(valor)

print("ÁRBOL ORIGINAL")
arbol.mostrar_arbol()

print("\nRecorrido inorden:", arbol.inorden())
print("Recorrido por niveles:", arbol.recorrido_por_niveles())
print("Suma de elementos:", arbol.sumar_elementos())
print("¿Todos los nodos internos tienen dos hijos?:", arbol.es_completo())
print("Altura del árbol original:", arbol.altura())

arbol.eliminar(10)
print("\nDespués de eliminar hoja 10:", arbol.inorden())

arbol.eliminar(20)
print("Después de eliminar nodo con un hijo 20:", arbol.inorden())

arbol.eliminar(30)
print("Después de eliminar nodo con dos hijos 30:", arbol.inorden())

arbol_balanceado = arbol.balancear_arbol()

print("\nÁRBOL BALANCEADO")
arbol_balanceado.mostrar_arbol()

print("\nInorden del árbol balanceado:", arbol_balanceado.inorden())
print("Altura del árbol balanceado:", arbol_balanceado.altura())