from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import re


def limpiar_pantalla():
    print("\n" * 2)


def mostrar_encabezado(titulo: str):
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


def generar_id() -> int:
    return int(datetime.now().timestamp() * 1000) % 1000000


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


class GestorPacientes:
    def __init__(self):
        self.pacientes: List[Paciente] = []

    def registrar(self, paciente: Paciente):
        self.pacientes.append(paciente)

    def listar(self) -> List[Paciente]:
        return sorted(self.pacientes, key=lambda p: (p.nombre, p.apellido))

    def existe(self, nombre: str, apellido: str, id_excluir: Optional[int] = None) -> bool:
        return any(
            p.id != id_excluir
            and p.nombre.lower() == nombre.lower()
            and p.apellido.lower() == apellido.lower()
            for p in self.pacientes
        )

    def eliminar(self, id_paciente: int):
        self.pacientes = [p for p in self.pacientes if p.id != id_paciente]


class GestorTratamientos:
    def __init__(self):
        self.tratamientos: List[Tratamiento] = []

    def registrar(self, tratamiento: Tratamiento):
        self.tratamientos.append(tratamiento)

    def por_paciente(self, id_paciente: int) -> List[Tratamiento]:
        return [t for t in self.tratamientos if t.id_paciente == id_paciente]

    def eliminar_por_paciente(self, id_paciente: int):
        self.tratamientos = [
            t for t in self.tratamientos
            if t.id_paciente != id_paciente
        ]


class GestorSeguimiento:
    def __init__(self):
        self.registros: List[RegistroSeguimiento] = []

    def agregar(self, registro: RegistroSeguimiento):
        self.registros.append(registro)

    def historial_paciente(self, id_paciente: int) -> List[RegistroSeguimiento]:
        return [
            r for r in self.registros
            if r.id_paciente == id_paciente
        ]

    def historial_tratamiento(
        self,
        id_paciente: int,
        id_tratamiento: int
    ) -> List[RegistroSeguimiento]:
        return [
            r for r in self.registros
            if r.id_paciente == id_paciente
            and r.id_tratamiento == id_tratamiento
        ]

    def eliminar_por_paciente(self, id_paciente: int):
        self.registros = [
            r for r in self.registros
            if r.id_paciente != id_paciente
        ]


def inicializar_datos(
    gestor_pacientes: GestorPacientes,
    gestor_tratamientos: GestorTratamientos,
    gestor_seguimiento: GestorSeguimiento
) -> None:
    p1 = Paciente(
        generar_id(),
        "Germán",
        "Pérez",
        35,
        "Hipertensión"
    )

    p2 = Paciente(
        generar_id(),
        "Ana",
        "Gómez",
        28,
        "Diabetes tipo 2"
    )

    gestor_pacientes.registrar(p1)
    gestor_pacientes.registrar(p2)

    t1 = Tratamiento(
        generar_id(),
        p1.id,
        "Losartán",
        "50mg",
        24,
        150.0
    )

    t2 = Tratamiento(
        generar_id(),
        p2.id,
        "Metformina",
        "850mg",
        12,
        80.0
    )

    gestor_tratamientos.registrar(t1)
    gestor_tratamientos.registrar(t2)

    ahora = datetime.now()

    gestor_seguimiento.agregar(
        RegistroSeguimiento(
            generar_id(),
            p1.id,
            t1.id,
            ahora,
            "Toma de prueba"
        )
    )

    gestor_seguimiento.agregar(
        RegistroSeguimiento(
            generar_id(),
            p2.id,
            t2.id,
            ahora,
            "Control inicial"
        )
    )


def seleccionar_paciente(
    gestor_pacientes: GestorPacientes
) -> Optional[Paciente]:
    pacientes = gestor_pacientes.listar()

    if not pacientes:
        print("No hay pacientes registrados.")
        input("Presione Enter para continuar...")
        return None

    for i, paciente in enumerate(pacientes, 1):
        print(f"{i}. {paciente.nombre_completo()} ({paciente.edad} años)")

    indice = leer_entero_rango(
        "Seleccione paciente (número): ",
        1,
        len(pacientes)
    )

    return pacientes[indice - 1]


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
        print("Advertencia: ya existe un paciente con este nombre y apellido.")

        if not confirmar("¿Desea continuar y registrar otro?"):
            print("Operación cancelada.")
            input("Presione Enter para continuar...")
            return

    edad = leer_entero_rango("Edad: ", 0, 120)

    condicion = leer_cadena(
        "Condición médica (opcional, Enter para saltar): ",
        obligatorio=False
    )

    if condicion == "":
        condicion = None

    paciente = Paciente(
        generar_id(),
        nombre,
        apellido,
        edad,
        condicion
    )

    gestor_pacientes.registrar(paciente)

    print(f"Paciente {paciente.nombre_completo()} registrado.")
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
        generar_id(),
        paciente.id,
        nombre,
        dosis,
        frecuencia,
        costo
    )

    gestor_tratamientos.registrar(tratamiento)

    print(
        f"Tratamiento '{nombre}' registrado para "
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

    for i, paciente in enumerate(pacientes, 1):
        print(f"{i}. {paciente.nombre_completo()} - {paciente.edad} años")

        if paciente.condicion_medica:
            print(f"   Condición: {paciente.condicion_medica}")

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
        nuevo_nombre = input(
            f"Nombre [{paciente.nombre}]: "
        ).strip()

        if nuevo_nombre == "":
            nuevo_nombre = paciente.nombre
            break

        if validar_nombre(nuevo_nombre):
            break

        print("Error: el nombre solo puede contener letras (2-50 caracteres).")

    while True:
        nuevo_apellido = input(
            f"Apellido [{paciente.apellido}]: "
        ).strip()

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
        texto_edad = input(
            f"Edad [{paciente.edad}]: "
        ).strip()

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
    gestor_seguimiento: GestorSeguimiento
) -> None:
    mostrar_encabezado("ELIMINAR PACIENTE")

    paciente = seleccionar_paciente(gestor_pacientes)

    if paciente is None:
        return

    print(
        f"Se eliminará a {paciente.nombre_completo()} y también "
        "sus tratamientos y registros de seguimiento."
    )

    if not confirmar("¿Desea continuar?"):
        print("Operación cancelada.")
        input("Presione Enter para continuar...")
        return

    gestor_tratamientos.eliminar_por_paciente(paciente.id)
    gestor_seguimiento.eliminar_por_paciente(paciente.id)
    gestor_pacientes.eliminar(paciente.id)

    print("Paciente eliminado correctamente.")
    input("Presione Enter para continuar...")


def gestionar_pacientes_menu(
    gestor_pacientes: GestorPacientes,
    gestor_tratamientos: GestorTratamientos,
    gestor_seguimiento: GestorSeguimiento
) -> None:
    while True:
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
                gestor_seguimiento
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

    tratamientos = gestor_tratamientos.por_paciente(paciente.id)

    while True:
        mostrar_encabezado(
            f"SEGUIMIENTO: {paciente.nombre_completo()}"
        )

        print("1. Ver historial completo")
        print("2. Ver historial de un tratamiento")
        print("3. Registrar nueva toma/visita")
        print("4. Volver")

        opcion = leer_entero_rango("Opción: ", 1, 4)

        if opcion == 1:
            historial = gestor_seguimiento.historial_paciente(
                paciente.id
            )

            if not historial:
                print("No hay registros para este paciente.")
            else:
                for registro in historial:
                    print(
                        f"- {registro.fecha.strftime('%d/%m/%Y %H:%M')} | "
                        f"{registro.observaciones}"
                    )

            input("Presione Enter para continuar...")

        elif opcion == 2:
            if not tratamientos:
                print("Este paciente no tiene tratamientos.")
                input("Presione Enter para continuar...")
                continue

            for i, tratamiento in enumerate(tratamientos, 1):
                print(f"{i}. {tratamiento.nombre}")

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

                for i, tratamiento in enumerate(tratamientos, 1):
                    print(f"{i}. {tratamiento.nombre}")

                seleccion = leer_entero_rango(
                    "Seleccione tratamiento: ",
                    1,
                    len(tratamientos)
                )

                tratamiento = tratamientos[seleccion - 1]
                id_tratamiento = tratamiento.id

            else:
                id_tratamiento = 0

            observaciones = leer_cadena("Observaciones: ")

            registro = RegistroSeguimiento(
                generar_id(),
                paciente.id,
                id_tratamiento,
                datetime.now(),
                observaciones
            )

            gestor_seguimiento.agregar(registro)

            print("Registro agregado.")
            input("Presione Enter para continuar...")

        elif opcion == 4:
            break


def menu_principal():
    mostrar_encabezado("CLINICLOG - MENÚ PRINCIPAL")
    print("1. Registrar paciente")
    print("2. Registrar tratamiento")
    print("3. Gestionar pacientes")
    print("4. Seguimiento de paciente")
    print("5. Salir")


def main():
    gestor_pacientes = GestorPacientes()
    gestor_tratamientos = GestorTratamientos()
    gestor_seguimiento = GestorSeguimiento()

    inicializar_datos(
        gestor_pacientes,
        gestor_tratamientos,
        gestor_seguimiento
    )

    while True:
        limpiar_pantalla()
        menu_principal()

        opcion = leer_entero_rango(
            "Seleccione una opción (1-5): ",
            1,
            5
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
                gestor_seguimiento
            )

        elif opcion == 4:
            seguimiento_paciente_menu(
                gestor_pacientes,
                gestor_tratamientos,
                gestor_seguimiento
            )

        elif opcion == 5:
            mostrar_encabezado("GRACIAS POR USAR CLINICLOG")
            break


if __name__ == "__main__":
    main()