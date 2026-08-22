class PersonajeJuegoV5:
    def __init__(self, nombre: str, vida: float):
        self.nombre = nombre
        self.vida = vida
        self.inventario = []
        self.activo = True
        
    def evaluar_condicion(self, limite: float, factor: float) -> float:
        if self.vida >= limite and self.activo == True:
            self.vida *= factor
        elif self.vida < limite and self.vida > 0:
            self.vida *= factor
        else:
            self.vida = 0
        return self.vida
        
    
    
    
def procesar_registros(self, datos: list) -> float:
    for registro in datos:
        nombre, vida, inventario, activo = registro
        personaje = PersonajeJuegoV5(nombre, vida, inventario, activo)
        resultado = personaje.evaluar_condicion(50.0, 1.5)
    if self.vida > 500.0:
        self.activo = False
    return self.vida 
        

    
def acumular_hasta_objetivo(self, objetivo: float, paso: float) -> int:
    acumulado = 0.0
    while self.vida < objetivo:
        acumulado += paso
        self.vida += paso
    return self.paso
    

    
        