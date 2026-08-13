from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import re

def limpiar_pantalla():
    print("\n" * 2)

def mostrar_encabezado(titulo: str):
    linea = "=" * 50
    print(linea)
    print(titulo.center(50))
    print(linea)

def leer_cadena(mensaje: str, obligatorio: bool = True) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor or not obligatorio:
            return valor
        print("Error: Este campo es obligatorio. Intente nuevamente.")

def leer_entero_rango(mensaje: str, minimo: int, maximo: int) -> int:
    while True:
        try:
            valor = input(mensaje).strip()
            if not valor:
                print("Error: Este campo es obligatorio. Intente nuevamente.")
                continue
            numero = int(valor)
            if minimo <= numero <= maximo:
                return numero
            print(f"Error: Ingrese un valor entre {minimo} y {maximo}.")
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")

def leer_decimal_positivo(mensaje: str, obligatorio: bool = True) -> float:
    while True:
        try:
            valor = input(mensaje).strip()
            if not valor and not obligatorio:
                return 0.0
            if not valor:
                print("Error: Este campo es obligatorio. Intente nuevamente.")
                continue
            numero = float(valor)
            if numero >= 0:
                return numero
            print("Error: El valor no puede ser negativo.")
        except ValueError:
            print("Error: Debe ingresar un número decimal válido.")

def confirmar(mensaje: str) -> bool:
    while True:
        resp = input(f"{mensaje} (s/n): ").strip().lower()
        if resp in ("s", "si", "sí"):
            return True
        elif resp in ("n", "no"):
            return False
        else:
            print("Error: Responda 's' para sí o 'n' para no.")

def generar_id() -> int:
    return int(datetime.now().timestamp() * 1000) % 1000000

def validar_nombre(nombre: str) -> bool:
    if len(nombre) < 2 or len(nombre) > 50:
        return False
    return bool(re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre))

def validar_texto_largo(texto: str, maximo: int = 100) -> bool:
    return len(texto) <= maximo

@dataclass
class Paciente:
    id: int
    nombre: str
    apellido: str
    edad: int
    condicion_medica: Optional[str] = None
    alergias: List[str] = field(default_factory=list)

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def __str__(self) -> str:
        return f"{self.nombre_completo} - {self.edad} años"

@dataclass
class Tratamiento:
    id: int
    id_paciente: int
    nombre: str
    dosis: str
    frecuencia_horas: int
    costo: float

    def __str__(self) -> str:
        return f"{self.nombre} ({self.dosis}) - Cada {self.frecuencia_horas}h - ${self.costo:.2f}"

@dataclass
class RegistroSeguimiento:
    id: int
    id_paciente: int
    id_tratamiento: int
    fecha: datetime
    observaciones: str
    realizado: bool = True

    def __str__(self) -> str:
        return f"{self.fecha.strftime('%d/%m/%Y %H:%M')} - {self.observaciones}"

class GestorPacientes:
    def __init__(self):
        self.pacientes: List[Paciente] = []

    def registrar_paciente(self, paciente: Paciente):
        self.pacientes.append(paciente)

    def buscar_por_nombre(self, nombre: str) -> List[Paciente]:
        return [p for p in self.pacientes if nombre.lower() in p.nombre.lower()]

    def obtener_por_id(self, id_paciente: int) -> Optional[Paciente]:
        for p in self.pacientes:
            if p.id == id_paciente:
                return p
        return None

    def listar_todos(self) -> List[Paciente]:
        return sorted(self.pacientes, key=lambda p: (p.nombre, p.apellido))

    def existe_paciente(self, nombre: str, apellido: str) -> bool:
        return any(
            p.nombre.lower() == nombre.lower() and p.apellido.lower() == apellido.lower()
            for p in self.pacientes
        )

class GestorTratamientos:
    def __init__(self):
        self.tratamientos: List[Tratamiento] = []

    def registrar_tratamiento(self, tratamiento: Tratamiento):
        self.tratamientos.append(tratamiento)

    def obtener_por_paciente(self, id_paciente: int) -> List[Tratamiento]:
        return [t for t in self.tratamientos if t.id_paciente == id_paciente]

    def buscar_por_nombre(self, nombre: str) -> List[Tratamiento]:
        return [t for t in self.tratamientos if nombre.lower() in t.nombre.lower()]

class GestorSeguimiento:
    def __init__(self):
        self.registros: List[RegistroSeguimiento] = []

    def agregar_registro(self, registro: RegistroSeguimiento):
        self.registros.append(registro)

    def obtener_historial_paciente(self, id_paciente: int) -> List[RegistroSeguimiento]:
        return [r for r in self.registros if r.id_paciente == id_paciente]

    def obtener_historial_tratamiento(self, id_paciente: int, id_tratamiento: int) -> List[RegistroSeguimiento]:
        return [r for r in self.registros 
                if r.id_paciente == id_paciente and r.id_tratamiento == id_tratamiento]

def inicializar_datos(gestor_pacientes, gestor_tratamientos, gestor_seguimiento):
    p1 = Paciente(generar_id(), "Germán", "Pérez", 35, "Hipertensión", ["Penicilina", "Aspirina"])
    p2 = Paciente(generar_id(), "Ana", "Gómez", 28, "Diabetes Tipo 2", ["Metformina"])
    p3 = Paciente(generar_id(), "Carlos", "López", 45, None, [])
    p4 = Paciente(generar_id(), "María", "Rodríguez", 62, "Artritis", ["Ibuprofeno"])

    gestor_pacientes.registrar_paciente(p1)
    gestor_pacientes.registrar_paciente(p2)
    gestor_pacientes.registrar_paciente(p3)
    gestor_pacientes.registrar_paciente(p4)

    t1 = Tratamiento(generar_id(), p1.id, "Losartán", "50mg", 24, 150.00)
    t2 = Tratamiento(generar_id(), p1.id, "Aspirina", "100mg", 24, 25.00)
    t3 = Tratamiento(generar_id(), p2.id, "Metformina", "850mg", 12, 80.00)
    t4 = Tratamiento(generar_id(), p2.id, "Insulina NPH", "20UI", 24, 320.00)
    t5 = Tratamiento(generar_id(), p3.id, "Omeprazol", "20mg", 24, 45.00)
    t6 = Tratamiento(generar_id(), p4.id, "Diclofenaco", "75mg", 12, 60.00)

    gestor_tratamientos.registrar_tratamiento(t1)
    gestor_tratamientos.registrar_tratamiento(t2)
    gestor_tratamientos.registrar_tratamiento(t3)
    gestor_tratamientos.registrar_tratamiento(t4)
    gestor_tratamientos.registrar_tratamiento(t5)
    gestor_tratamientos.registrar_tratamiento(t6)

    ahora = datetime.now()
    r1 = RegistroSeguimiento(generar_id(), p1.id, t1.id, ahora.replace(hour=8, minute=0), "Toma matutina sin complicaciones")
    r2 = RegistroSeguimiento(generar_id(), p1.id, t1.id, ahora.replace(hour=20, minute=0), "Toma nocturna completada")
    r3 = RegistroSeguimiento(generar_id(), p2.id, t3.id, ahora.replace(hour=7, minute=30), "Toma con desayuno")
    r4 = RegistroSeguimiento(generar_id(), p2.id, t4.id, ahora.replace(hour=21, minute=0), "Aplicación de insulina")
    r5 = RegistroSeguimiento(generar_id(), p4.id, t6.id, ahora.replace(hour=14, minute=0), "Toma después de almuerzo")

    gestor_seguimiento.agregar_registro(r1)
    gestor_seguimiento.agregar_registro(r2)
    gestor_seguimiento.agregar_registro(r3)
    gestor_seguimiento.agregar_registro(r4)
    gestor_seguimiento.agregar_registro(r5)

def registrar_paciente_menu(gestor_pacientes, gestor_tratamientos, gestor_seguimiento):
    mostrar_encabezado("REGISTRAR PACIENTE")

    while True:
        nombre = leer_cadena("Nombre: ")
        if validar_nombre(nombre):
            break
        print("Error: El nombre solo puede contener letras (2-50 caracteres).")

    while True:
        apellido = leer_cadena("Apellido: ")
        if validar_nombre(apellido):
            break
        print("Error: El apellido solo puede contener letras (2-50 caracteres).")

    if gestor_pacientes.existe_paciente(nombre, apellido):
        print("Advertencia: Ya existe un paciente registrado con este nombre y apellido.")
        if not confirmar("¿Desea continuar y registrar de todas formas?"):
            print("Operación cancelada.")
            input("Presione Enter para continuar...")
            return

    edad = leer_entero_rango("Edad: ", 0, 120)

    condicion = leer_cadena("Condición médica (opcional, Enter para saltar): ", obligatorio=False)
    if condicion and not validar_texto_largo(condicion, 100):
        condicion = condicion[:100]

    alergias_txt = leer_cadena("Alergias separadas por coma (opcional, Enter para saltar): ", obligatorio=False)
    alergias = []
    if alergias_txt:
        alergias = [a.strip() for a in alergias_txt.split(",") if a.strip()]
        if len(alergias) > 10:
            alergias = alergias[:10]

    paciente = Paciente(generar_id(), nombre, apellido, edad, condicion or None, alergias)
    gestor_pacientes.registrar_paciente(paciente)
    print(f"Paciente {paciente.nombre_completo} registrado exitosamente.")
    input("Presione Enter para continuar...")

def registrar_tratamiento_menu(gestor_pacientes, gestor_tratamientos):
    mostrar_encabezado("REGISTRAR TRATAMIENTO")
    
    pacientes = gestor_pacientes.listar_todos()
    if not pacientes:
        print("No hay pacientes registrados. Registre un paciente primero.")
        input("Presione Enter para continuar...")
        return

    for i, p in enumerate(pacientes, 1):
        print(f"{i}. {p.nombre_completo} ({p.edad} años)")

    seleccion = leer_entero_rango("Seleccione paciente (número): ", 1, len(pacientes))
    paciente = pacientes[seleccion - 1]

    while True:
        nombre = leer_cadena("Nombre del tratamiento: ")
        if len(nombre) >= 2 and len(nombre) <= 50:
            break
        print("Error: El nombre debe tener entre 2 y 50 caracteres.")

    dosis = leer_cadena("Dosis (ej: 500mg, 20UI): ")
    if not validar_texto_largo(dosis, 30):
        dosis = dosis[:30]

    frecuencia = leer_entero_rango("Frecuencia (horas entre tomas, 1-365): ", 1, 365)
    costo = leer_decimal_positivo("Costo del tratamiento: ")

    tratamiento = Tratamiento(generar_id(), paciente.id, nombre, dosis, frecuencia, costo)
    gestor_tratamientos.registrar_tratamiento(tratamiento)
    print(f"Tratamiento '{nombre}' registrado para {paciente.nombre_completo}.")
    input("Presione Enter para continuar...")

def ver_pacientes_menu(gestor_pacientes, gestor_tratamientos):
    mostrar_encabezado("LISTA DE PACIENTES")
    
    pacientes = gestor_pacientes.listar_todos()
    if not pacientes:
        print("No hay pacientes registrados.")
    else:
        print(f"Total de pacientes: {len(pacientes)}\n")
        for i, p in enumerate(pacientes, 1):
            tratamientos = gestor_tratamientos.obtener_por_paciente(p.id)
            print(f"{i}. {p.nombre_completo} - {p.edad} años")
            if p.condicion_medica:
                print(f"   Condición: {p.condicion_medica}")
            if p.alergias:
                print(f"   Alergias: {', '.join(p.alergias)}")
            if tratamientos:
                print(f"   Tratamientos: {len(tratamientos)}")
                for t in tratamientos[:3]:
                    print(f"      * {t}")
                if len(tratamientos) > 3:
                    print(f"      ... y {len(tratamientos) - 3} más")
            else:
                print("   Sin tratamientos")
            print()
    input("Presione Enter para continuar...")

def seguimiento_paciente_menu(gestor_pacientes, gestor_tratamientos, gestor_seguimiento):
    mostrar_encabezado("SEGUIMIENTO DE PACIENTE")
    
    pacientes = gestor_pacientes.listar_todos()
    if not pacientes:
        print("No hay pacientes registrados.")
        input("Presione Enter para continuar...")
        return

    for i, p in enumerate(pacientes, 1):
        print(f"{i}. {p.nombre_completo}")

    seleccion = leer_entero_rango("Seleccione paciente (número): ", 1, len(pacientes))
    paciente = pacientes[seleccion - 1]
    tratamientos = gestor_tratamientos.obtener_por_paciente(paciente.id)

    while True:
        mostrar_encabezado(f"SEGUIMIENTO: {paciente.nombre_completo}")
        print("1. Ver historial completo")
        print("2. Ver historial de un tratamiento")
        print("3. Registrar nueva toma/visita")
        print("4. Volver al menú principal")

        opcion = leer_entero_rango("Seleccione una opción (1-4): ", 1, 4)

        if opcion == 1:
            mostrar_encabezado("HISTORIAL COMPLETO")
            historial = gestor_seguimiento.obtener_historial_paciente(paciente.id)
            if not historial:
                print("No hay registros de seguimiento para este paciente.")
            else:
                print(f"Total de registros: {len(historial)}\n")
                for r in historial:
                    print(f"* {r}")
            input("Presione Enter para continuar...")

        elif opcion == 2:
            if not tratamientos:
                print("Este paciente no tiene tratamientos registrados.")
                input("Presione Enter para continuar...")
                continue
            
            for i, t in enumerate(tratamientos, 1):
                print(f"{i}. {t}")
            
            sel = leer_entero_rango("Seleccione tratamiento (número): ", 1, len(tratamientos))
            tratamiento = tratamientos[sel - 1]
            
            historial = gestor_seguimiento.obtener_historial_tratamiento(paciente.id, tratamiento.id)
            mostrar_encabezado(f"HISTORIAL: {tratamiento.nombre}")
            if not historial:
                print("No hay registros para este tratamiento.")
            else:
                print(f"Total de registros: {len(historial)}\n")
                for r in historial:
                    print(f"* {r}")
            input("Presione Enter para continuar...")

        elif opcion == 3:
            observaciones = leer_cadena("Observaciones de la toma/visita: ")
            if not validar_texto_largo(observaciones, 200):
                observaciones = observaciones[:200]

            id_tratamiento = tratamientos[0].id if tratamientos else 0
            registro = RegistroSeguimiento(
                id=generar_id(),
                id_paciente=paciente.id,
                id_tratamiento=id_tratamiento,
                fecha=datetime.now(),
                observaciones=observaciones,
                realizado=True
            )
            gestor_seguimiento.agregar_registro(registro)
            print("Registro agregado exitosamente.")
            input("Presione Enter para continuar...")

        elif opcion == 4:
            break

def menu_principal():
    mostrar_encabezado("CLINICLOG - SISTEMA DE GESTIÓN CLÍNICA")
    print("1. Registrar paciente")
    print("2. Registrar tratamiento")
    print("3. Ver pacientes")
    print("4. Seguimiento de paciente")
    print("5. Salir del sistema")

def main():
    gestor_pacientes = GestorPacientes()
    gestor_tratamientos = GestorTratamientos()
    gestor_seguimiento = GestorSeguimiento()

    inicializar_datos(gestor_pacientes, gestor_tratamientos, gestor_seguimiento)

    while True:
        limpiar_pantalla()
        menu_principal()
        opcion = leer_entero_rango("\nSeleccione una opción (1-5): ", 1, 5)

        if opcion == 1:
            registrar_paciente_menu(gestor_pacientes, gestor_tratamientos, gestor_seguimiento)
        elif opcion == 2:
            registrar_tratamiento_menu(gestor_pacientes, gestor_tratamientos)
        elif opcion == 3:
            ver_pacientes_menu(gestor_pacientes, gestor_tratamientos)
        elif opcion == 4:
            seguimiento_paciente_menu(gestor_pacientes, gestor_tratamientos, gestor_seguimiento)
        elif opcion == 5:
            mostrar_encabezado("GRACIAS POR USAR CLINICLOG")
            print("¡Hasta luego!\n")
            break

if __name__ == "__main__":
    main()