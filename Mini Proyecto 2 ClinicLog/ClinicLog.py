from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque, List, Optional
import re


_contador_ids = 0


def generar_id() -> int:
    global _contador_ids
    _contador_ids += 1
    return _contador_ids


def limpiar_pantalla() -> None:
    print("\n" * 2)


def mostrar_encabezado(titulo: str) -> None:
    linea = "=" * 40
    print(linea)
    print(titulo.center(40))
    print(linea)


def leer_cadena(mensaje: str, obligatorio: bool = True) -> str:
    while True:
        valor = input(mensaje).strip()

        if valor or not obligatorio:
            return valor

        print("Error: este campo es obligatorio.")


def leer_entero_rango(mensaje: str, minimo: int, maximo: int) -> int:
    while True:
        texto = input(mensaje).strip()

        try:
            numero = int(texto)

            if minimo <= numero <= maximo:
                return numero

            print(f"Error: ingrese un número entre {minimo} y {maximo}.")

        except ValueError:
            print("Error: ingrese un número entero válido.")


def leer_decimal_positivo(mensaje: str) -> float:
    while True:
        texto = input(mensaje).strip()

        try:
            numero = float(texto)

            if numero >= 0:
                return numero

            print("Error: el valor no puede ser negativo.")

        except ValueError:
            print("Error: ingrese un número decimal válido.")


def confirmar(mensaje: str) -> bool:
    while True:
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()

        if respuesta in ("s", "si", "sí"):
            return True

        if respuesta in ("n", "no"):
            return False

        print("Error: responda con s o n.")


def validar_nombre(nombre: str) -> bool:
    if len(nombre) < 2 or len(nombre) > 50:
        return False

    return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre))


@dataclass
class Paciente:
    id: int
    nombre: str
    apellido: str
    edad: int
    condicion_medica: Optional[str] = None

    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"


@dataclass
class Tratamiento:
    id: int
    id_paciente: int
    nombre: str
    dosis: str
    frecuencia_horas: int
    costo: float


@dataclass
class RegistroSeguimiento:
    id: int
    id_paciente: int
    id_tratamiento: int
    fecha: datetime
    observaciones: str


@dataclass
class BorradoAccion:
    paciente: Paciente
    tratamientos: List[Tratamiento] = field(default_factory=list)
    seguimientos: List[RegistroSeguimiento] = field(default_factory=list)
    fecha_borrado: datetime = field(default_factory=datetime.now)


class Pila:
    def __init__(self) -> None:
        self._elementos: Deque[BorradoAccion] = deque()

    def push(self, item: BorradoAccion) -> None:
        self._elementos.append(item)

    def pop(self) -> Optional[BorradoAccion]:
        if self.is_empty():
            return None

        return self._elementos.pop()

    def peek(self) -> Optional[BorradoAccion]:
        if self.is_empty():
            return None

        return self._elementos[-1]

    def is_empty(self) -> bool:
        return len(self._elementos) == 0

    def size(self) -> int:
        return len(self._elementos)


class GestorPacientes:
    def __init__(self) -> None:
        self.pacientes: List[Paciente] = []

    def registrar(self, paciente: Paciente) -> bool:
        if self.obtener_por_id(paciente.id) is not None:
            return False

        self.pacientes.append(paciente)
        return True

    def listar(self) -> List[Paciente]:
        return sorted(
            self.pacientes,
            key=lambda paciente: (
                paciente.nombre.lower(),
                paciente.apellido.lower()
            )
        )

    def existe(
        self,
        nombre: str,
        apellido: str,
        id_excluir: Optional[int] = None
    ) -> bool:
        return any(
            paciente.id != id_excluir
            and paciente.nombre.lower() == nombre.lower()
            and paciente.apellido.lower() == apellido.lower()
            for paciente in self.pacientes
        )

    def obtener_por_id(self, id_paciente: int) -> Optional[Paciente]:
        for paciente in self.pacientes:
            if paciente.id == id_paciente:
                return paciente

        return None

    def eliminar(self, id_paciente: int) -> bool:
        cantidad_anterior = len(self.pacientes)

        self.pacientes = [
            paciente
            for paciente in self.pacientes
            if paciente.id != id_paciente
        ]

        return len(self.pacientes) < cantidad_anterior


class GestorTratamientos:
    def __init__(self) -> None:
        self.tratamientos: List[Tratamiento] = []

    def registrar(self, tratamiento: Tratamiento) -> bool:
        if self.existe_id(tratamiento.id):
            return False

        self.tratamientos.append(tratamiento)
        return True

    def existe_id(self, id_tratamiento: int) -> bool:
        return any(
            tratamiento.id == id_tratamiento
            for tratamiento in self.tratamientos
        )

    def por_paciente(self, id_paciente: int) -> List[Tratamiento]:
        return [
            tratamiento
            for tratamiento in self.tratamientos
            if tratamiento.id_paciente == id_paciente
        ]

    def eliminar_por_paciente(self, id_paciente: int) -> List[Tratamiento]:
        tratamientos_eliminados = self.por_paciente(id_paciente)

        self.tratamientos = [
            tratamiento
            for tratamiento in self.tratamientos
            if tratamiento.id_paciente != id_paciente
        ]

        return tratamientos_eliminados

    def restaurar_lista(self, tratamientos: List[Tratamiento]) -> int:
        cantidad_restaurada = 0

        for tratamiento in tratamientos:
            if self.registrar(tratamiento):
                cantidad_restaurada += 1

        return cantidad_restaurada


class GestorSeguimiento:
    def __init__(self) -> None:
        self.registros: List[RegistroSeguimiento] = []

    def agregar(self, registro: RegistroSeguimiento) -> bool:
        if self.existe_id(registro.id):
            return False

        self.registros.append(registro)
        return True

    def existe_id(self, id_registro: int) -> bool:
        return any(
            registro.id == id_registro
            for registro in self.registros
        )

    def historial_paciente(self, id_paciente: int) -> List[RegistroSeguimiento]:
        return [
            registro
            for registro in self.registros
            if registro.id_paciente == id_paciente
        ]

    def historial_tratamiento(
        self,
        id_paciente: int,
        id_tratamiento: int
    ) -> List[RegistroSeguimiento]:
        return [
            registro
            for registro in self.registros
            if registro.id_paciente == id_paciente
            and registro.id_tratamiento == id_tratamiento
        ]

    def eliminar_por_paciente(
        self,
        id_paciente: int
    ) -> List[RegistroSeguimiento]:
        registros_eliminados = self.historial_paciente(id_paciente)

        self.registros = [
            registro
            for registro in self.registros
            if registro.id_paciente != id_paciente
        ]

        return registros_eliminados

    def restaurar_lista(
        self,
        registros: List[RegistroSeguimiento]
    ) -> int:
        cantidad_restaurada = 0

        for registro in registros:
            if self.agregar(registro):
                cantidad_restaurada += 1

        return cantidad_restaurada


def inicializar_datos(
    gestor_pacientes: GestorPacientes,
    gestor_tratamientos: GestorTratamientos,
    gestor_seguimiento: GestorSeguimiento
) -> None:
    p1 = Paciente(
        id=generar_id(),
        nombre="Germán",
        apellido="Pérez",
        edad=35,
        condicion_medica="Hipertensión"
    )

    p2 = Paciente(
        id=generar_id(),
        nombre="Ana",
        apellido="Gómez",
        edad=28,
        condicion_medica="Diabetes tipo 2"
    )

    gestor_pacientes.registrar(p1)
    gestor_pacientes.registrar(p2)

    t1 = Tratamiento(
        id=generar_id(),
        id_paciente=p1.id,
        nombre="Losartán",
        dosis="50mg",
        frecuencia_horas=24,
        costo=150.0
    )

    t2 = Tratamiento(
        id=generar_id(),
        id_paciente=p2.id,
        nombre="Metformina",
        dosis="850mg",
        frecuencia_horas=12,
        costo=80.0
    )

    gestor_tratamientos.registrar(t1)
    gestor_tratamientos.registrar(t2)

    ahora = datetime.now()

    seguimiento_1 = RegistroSeguimiento(
        id=generar_id(),
        id_paciente=p1.id,
        id_tratamiento=t1.id,
        fecha=ahora,
        observaciones="Toma de prueba"
    )

    seguimiento_2 = RegistroSeguimiento(
        id=generar_id(),
        id_paciente=p2.id,
        id_tratamiento=t2.id,
        fecha=ahora,
        observaciones="Control inicial"
    )

    gestor_seguimiento.agregar(seguimiento_1)
    gestor_seguimiento.agregar(seguimiento_2)


def seleccionar_paciente(
    gestor_pacientes: GestorPacientes
) -> Optional[Paciente]:
    pacientes = gestor_pacientes.listar()

    if not pacientes:
        print("No hay pacientes registrados.")
        input("Presione Enter para continuar...")
        return None

    for indice, paciente in enumerate(pacientes, start=1):
        print(
            f"{indice}. {paciente.nombre_completo()} "
            f"[ID: {paciente.id}] - {paciente.edad} años"
        )

    seleccion = leer_entero_rango(
        "Seleccione paciente (número): ",
        1,
        len(pacientes)
    )

    return pacientes[seleccion - 1]


def registrar_paciente_menu(
    gestor_pacientes: GestorPacientes
) -> None:
    mostrar_encabezado("REGISTRAR PACIENTE")

    while True:
        nombre = leer_cadena("Nombre: ")

        if validar_nombre(nombre):
            break

        print("Error: el nombre solo puede contener letras (2-50 caracteres).")

    while True:
        apellido = leer_cadena("Apellido: ")

        if validar_nombre(apellido):
            break

        print("Error: el apellido solo puede contener letras (2-50 caracteres).")

    if gestor_pacientes.existe(nombre, apellido):
        print("Advertencia: ya existe un paciente con ese nombre y apellido.")

        if not confirmar("¿Desea continuar y registrar otro?"):
            print("Operación cancelada.")
            input("Presione Enter para continuar...")
            return

    edad = leer_entero_rango("Edad: ", 0, 120)

    condicion = leer_cadena(
        "Condición médica (opcional, Enter para saltar): ",
        obligatorio=False
    )

    paciente = Paciente(
        id=generar_id(),
        nombre=nombre,
        apellido=apellido,
        edad=edad,
        condicion_medica=condicion if condicion else None
    )

    gestor_pacientes.registrar(paciente)

    print(
        f"Paciente {paciente.nombre_completo()} registrado "
        f"correctamente con ID {paciente.id}."
    )

    input("Presione Enter para continuar...")


def registrar_tratamiento_menu(
    gestor_pacientes: GestorPacientes,
    gestor_tratamientos: GestorTratamientos
) -> None:
    mostrar_encabezado("REGISTRAR TRATAMIENTO")

    paciente = seleccionar_paciente(gestor_pacientes)

    if paciente is None:
        return

    nombre = leer_cadena("Nombre del tratamiento: ")
    dosis = leer_cadena("Dosis: ")

    frecuencia = leer_entero_rango(
        "Frecuencia (horas entre tomas): ",
        1,
        365
    )

    costo = leer_decimal_positivo("Costo: ")

    tratamiento = Tratamiento(
        id=generar_id(),
        id_paciente=paciente.id,
        nombre=nombre,
        dosis=dosis,
        frecuencia_horas=frecuencia,
        costo=costo
    )

    gestor_tratamientos.registrar(tratamiento)

    print(
        f"Tratamiento '{tratamiento.nombre}' registrado para "
        f"{paciente.nombre_completo()}."
    )

    input("Presione Enter para continuar...")


def ver_pacientes(
    gestor_pacientes: GestorPacientes,
    gestor_tratamientos: GestorTratamientos
) -> None:
    mostrar_encabezado("LISTA DE PACIENTES")

    pacientes = gestor_pacientes.listar()

    if not pacientes:
        print("No hay pacientes registrados.")
        input("Presione Enter para continuar...")
        return

    for indice, paciente in enumerate(pacientes, start=1):
        print(
            f"{indice}. {paciente.nombre_completo()} "
            f"[ID: {paciente.id}] - {paciente.edad} años"
        )

        if paciente.condicion_medica:
            print(f"   Condición: {paciente.condicion_medica}")
        else:
            print("   Condición: Sin registrar")

        tratamientos = gestor_tratamientos.por_paciente(paciente.id)

        if tratamientos:
            print("   Tratamientos:")

            for tratamiento in tratamientos:
                print(
                    f"      - {tratamiento.nombre} "
                    f"({tratamiento.dosis}) cada "
                    f"{tratamiento.frecuencia_horas}h, "
                    f"costo {tratamiento.costo:.2f}"
                )
        else:
            print("   Sin tratamientos")

        print()

    input("Presione Enter para continuar...")


def editar_paciente_menu(
    gestor_pacientes: GestorPacientes
) -> None:
    mostrar_encabezado("EDITAR PACIENTE")

    paciente = seleccionar_paciente(gestor_pacientes)

    if paciente is None:
        return

    print("Presione Enter para conservar el valor actual.")

    while True:
        nuevo_nombre = input(f"Nombre [{paciente.nombre}]: ").strip()

        if nuevo_nombre == "":
            nuevo_nombre = paciente.nombre
            break

        if validar_nombre(nuevo_nombre):
            break

        print("Error: el nombre solo puede contener letras (2-50 caracteres).")

    while True:
        nuevo_apellido = input(f"Apellido [{paciente.apellido}]: ").strip()

        if nuevo_apellido == "":
            nuevo_apellido = paciente.apellido
            break

        if validar_nombre(nuevo_apellido):
            break

        print("Error: el apellido solo puede contener letras (2-50 caracteres).")

    if gestor_pacientes.existe(
        nuevo_nombre,
        nuevo_apellido,
        paciente.id
    ):
        print("Error: ya existe otro paciente con ese nombre y apellido.")
        input("Presione Enter para continuar...")
        return

    while True:
        texto_edad = input(f"Edad [{paciente.edad}]: ").strip()

        if texto_edad == "":
            nueva_edad = paciente.edad
            break

        try:
            nueva_edad = int(texto_edad)

            if 0 <= nueva_edad <= 120:
                break

            print("Error: ingrese una edad entre 0 y 120.")

        except ValueError:
            print("Error: ingrese un número entero válido.")

    nueva_condicion = input(
        f"Condición médica [{paciente.condicion_medica or 'Sin registrar'}]: "
    ).strip()

    if nueva_condicion == "":
        nueva_condicion = paciente.condicion_medica

    paciente.nombre = nuevo_nombre
    paciente.apellido = nuevo_apellido
    paciente.edad = nueva_edad
    paciente.condicion_medica = nueva_condicion

    print("Paciente actualizado correctamente.")
    input("Presione Enter para continuar...")


def eliminar_paciente_menu(
    gestor_pacientes: GestorPacientes,
    gestor_tratamientos: GestorTratamientos,
    gestor_seguimiento: GestorSeguimiento,
    pila_borrados: Pila
) -> None:
    mostrar_encabezado("ELIMINAR PACIENTE")

    paciente = seleccionar_paciente(gestor_pacientes)

    if paciente is None:
        return

    print(
        f"Se eliminará únicamente a: {paciente.nombre_completo()} "
        f"[ID: {paciente.id}]"
    )
    print("También se eliminarán únicamente sus tratamientos y seguimientos.")

    if not confirmar("¿Desea continuar?"):
        print("Operación cancelada.")
        input("Presione Enter para continuar...")
        return

    tratamientos_eliminados = gestor_tratamientos.por_paciente(paciente.id)
    seguimientos_eliminados = gestor_seguimiento.historial_paciente(paciente.id)

    accion_borrado = BorradoAccion(
        paciente=paciente,
        tratamientos=tratamientos_eliminados.copy(),
        seguimientos=seguimientos_eliminados.copy(),
        fecha_borrado=datetime.now()
    )

    pila_borrados.push(accion_borrado)

    gestor_tratamientos.eliminar_por_paciente(paciente.id)
    gestor_seguimiento.eliminar_por_paciente(paciente.id)
    eliminado = gestor_pacientes.eliminar(paciente.id)

    if eliminado:
        print(
            f"Paciente {paciente.nombre_completo()} eliminado correctamente. "
            f"Puede usar la opción Undo para restaurarlo."
        )
    else:
        print("No se pudo eliminar el paciente.")

    input("Presione Enter para continuar...")


def deshacer_ultimo_borrado_menu(
    gestor_pacientes: GestorPacientes,
    gestor_tratamientos: GestorTratamientos,
    gestor_seguimiento: GestorSeguimiento,
    pila_borrados: Pila
) -> None:
    mostrar_encabezado("DESHACER ÚLTIMA ELIMINACIÓN")

    if pila_borrados.is_empty():
        print("No hay eliminaciones previas para deshacer.")
        input("Presione Enter para continuar...")
        return

    accion = pila_borrados.peek()

    if accion is None:
        print("No hay eliminaciones previas para deshacer.")
        input("Presione Enter para continuar...")
        return

    if gestor_pacientes.obtener_por_id(accion.paciente.id) is not None:
        print(
            "No se puede restaurar porque el paciente ya existe "
            "en el sistema."
        )
        input("Presione Enter para continuar...")
        return

    accion = pila_borrados.pop()

    if accion is None:
        print("No se pudo recuperar la eliminación.")
        input("Presione Enter para continuar...")
        return

    gestor_pacientes.registrar(accion.paciente)

    tratamientos_restaurados = gestor_tratamientos.restaurar_lista(
        accion.tratamientos
    )

    seguimientos_restaurados = gestor_seguimiento.restaurar_lista(
        accion.seguimientos
    )

    print(
        f"Paciente restaurado: {accion.paciente.nombre_completo()} "
        f"[ID: {accion.paciente.id}]"
    )
    print(f"Tratamientos restaurados: {tratamientos_restaurados}")
    print(f"Seguimientos restaurados: {seguimientos_restaurados}")
    print(
        "Eliminación original: "
        f"{accion.fecha_borrado.strftime('%d/%m/%Y %H:%M:%S')}"
    )

    input("Presione Enter para continuar...")


def gestionar_pacientes_menu(
    gestor_pacientes: GestorPacientes,
    gestor_tratamientos: GestorTratamientos,
    gestor_seguimiento: GestorSeguimiento,
    pila_borrados: Pila
) -> None:
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTIONAR PACIENTES")

        print("1. Ver pacientes")
        print("2. Editar paciente")
        print("3. Eliminar paciente")
        print("4. Volver")

        opcion = leer_entero_rango(
            "Seleccione una opción (1-4): ",
            1,
            4
        )

        if opcion == 1:
            ver_pacientes(
                gestor_pacientes,
                gestor_tratamientos
            )

        elif opcion == 2:
            editar_paciente_menu(gestor_pacientes)

        elif opcion == 3:
            eliminar_paciente_menu(
                gestor_pacientes,
                gestor_tratamientos,
                gestor_seguimiento,
                pila_borrados
            )

        elif opcion == 4:
            break


def seguimiento_paciente_menu(
    gestor_pacientes: GestorPacientes,
    gestor_tratamientos: GestorTratamientos,
    gestor_seguimiento: GestorSeguimiento
) -> None:
    mostrar_encabezado("SEGUIMIENTO DE PACIENTE")

    paciente = seleccionar_paciente(gestor_pacientes)

    if paciente is None:
        return

    while True:
        tratamientos = gestor_tratamientos.por_paciente(paciente.id)

        limpiar_pantalla()
        mostrar_encabezado(
            f"SEGUIMIENTO: {paciente.nombre_completo()}"
        )

        print("1. Ver historial completo")
        print("2. Ver historial de un tratamiento")
        print("3. Registrar nueva toma/visita")
        print("4. Volver")

        opcion = leer_entero_rango("Opción: ", 1, 4)

        if opcion == 1:
            historial = gestor_seguimiento.historial_paciente(paciente.id)

            if not historial:
                print("No hay registros para este paciente.")
            else:
                for registro in historial:
                    if registro.id_tratamiento == 0:
                        nombre_tratamiento = "Seguimiento general"
                    else:
                        nombre_tratamiento = (
                            f"Tratamiento ID {registro.id_tratamiento}"
                        )

                    print(
                        f"- {registro.fecha.strftime('%d/%m/%Y %H:%M')} | "
                        f"{nombre_tratamiento} | "
                        f"{registro.observaciones}"
                    )

            input("Presione Enter para continuar...")

        elif opcion == 2:
            if not tratamientos:
                print("Este paciente no tiene tratamientos.")
                input("Presione Enter para continuar...")
                continue

            for indice, tratamiento in enumerate(tratamientos, start=1):
                print(f"{indice}. {tratamiento.nombre}")

            seleccion = leer_entero_rango(
                "Seleccione tratamiento: ",
                1,
                len(tratamientos)
            )

            tratamiento = tratamientos[seleccion - 1]

            historial = gestor_seguimiento.historial_tratamiento(
                paciente.id,
                tratamiento.id
            )

            if not historial:
                print("No hay registros para este tratamiento.")
            else:
                for registro in historial:
                    print(
                        f"- {registro.fecha.strftime('%d/%m/%Y %H:%M')} | "
                        f"{registro.observaciones}"
                    )

            input("Presione Enter para continuar...")

        elif opcion == 3:
            if tratamientos:
                print("Tratamientos del paciente:")

                for indice, tratamiento in enumerate(tratamientos, start=1):
                    print(f"{indice}. {tratamiento.nombre}")

                seleccion = leer_entero_rango(
                    "Seleccione tratamiento: ",
                    1,
                    len(tratamientos)
                )

                tratamiento = tratamientos[seleccion - 1]
                id_tratamiento = tratamiento.id

            else:
                print("El paciente no tiene tratamientos.")
                print("El seguimiento se guardará como seguimiento general.")
                id_tratamiento = 0

            observaciones = leer_cadena("Observaciones: ")

            registro = RegistroSeguimiento(
                id=generar_id(),
                id_paciente=paciente.id,
                id_tratamiento=id_tratamiento,
                fecha=datetime.now(),
                observaciones=observaciones
            )

            gestor_seguimiento.agregar(registro)

            print("Registro agregado.")
            input("Presione Enter para continuar...")

        elif opcion == 4:
            break


def menu_principal() -> None:
    mostrar_encabezado("CLINICLOG - MENÚ PRINCIPAL")
    print("1. Registrar paciente")
    print("2. Registrar tratamiento")
    print("3. Gestionar pacientes")
    print("4. Seguimiento de paciente")
    print("5. Deshacer última eliminación (Undo)")
    print("6. Salir")


def main() -> None:
    gestor_pacientes = GestorPacientes()
    gestor_tratamientos = GestorTratamientos()
    gestor_seguimiento = GestorSeguimiento()
    pila_borrados = Pila()

    inicializar_datos(
        gestor_pacientes,
        gestor_tratamientos,
        gestor_seguimiento
    )

    while True:
        limpiar_pantalla()
        menu_principal()

        opcion = leer_entero_rango(
            "Seleccione una opción (1-6): ",
            1,
            6
        )

        if opcion == 1:
            registrar_paciente_menu(gestor_pacientes)

        elif opcion == 2:
            registrar_tratamiento_menu(
                gestor_pacientes,
                gestor_tratamientos
            )

        elif opcion == 3:
            gestionar_pacientes_menu(
                gestor_pacientes,
                gestor_tratamientos,
                gestor_seguimiento,
                pila_borrados
            )

        elif opcion == 4:
            seguimiento_paciente_menu(
                gestor_pacientes,
                gestor_tratamientos,
                gestor_seguimiento
            )

        elif opcion == 5:
            deshacer_ultimo_borrado_menu(
                gestor_pacientes,
                gestor_tratamientos,
                gestor_seguimiento,
                pila_borrados
            )

        elif opcion == 6:
            mostrar_encabezado("GRACIAS POR USAR CLINICLOG")
            break


if __name__ == "__main__":
    main()