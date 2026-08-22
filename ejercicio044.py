class PersonajeJuegoV5:
    def __init__(self, nombre: str, vida: float):
        self.nombre = nombre
        self.vida = vida
        self.inventario = []
        self.activo = True

    def evaluar_condicion(self, limite: float, factor: float) -> float:
        if self.vida >= limite and self.activo == True:
            return self.vida * factor
        elif self.vida < limite and self.vida > 0:
            return self.vida + 10.0
        else:
            return 0.0

    def procesar_registros(self, datos: list) -> float:
        for valor in datos:
            if valor is None:
                continue
            self.vida += valor
            self.inventario.append(valor)
            if self.vida > 500.0:
                self.activo = False
        return self.vida

    def acumular_hasta_objetivo(self, objetivo: float, paso: float) -> int:
        contador = 0
        while self.vida < objetivo:
            self.vida += paso
            contador += 1
        return contador