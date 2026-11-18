# Importo las herramientas necesarias para ejecutar el sistema.
import logging

# Importo la configuración de registros del sistema.
from logs import configurar_logs, obtener_logger

# Importo el gestor de clientes.
from clientes import GestorClientes

# Importo las excepciones relacionadas con los clientes.
from excepciones import (
    DatosClienteInvalidosError,
    ClienteDuplicadoError,
    ClienteNoEncontradoError)


# Configuro los registros del sistema.
configurar_logs()

# Obtengo el registrador del programa principal.
logger = obtener_logger(__name__)


# Creo el gestor encargado de administrar los clientes.
gestor_clientes = GestorClientes()


# Defino la función para registrar un cliente.
def registrar_cliente():

    try:
        # Solicito los datos del cliente.
        identificador = input("Ingrese la identificación: ")
        nombre = input("Ingrese el nombre: ")
        correo = input("Ingrese el correo electrónico: ")

        # Registro el cliente mediante el gestor.
        cliente = gestor_clientes.registrar_cliente(
            identificador, nombre, correo)

        # Confirmo el registro.
        print("Cliente registrado correctamente.")
        print(cliente.mostrar_informacion())

        # Registro la operación realizada.
        logger.info("Registro de cliente completado.")

    except (
        DatosClienteInvalidosError,
        ClienteDuplicadoError
    ) as error:
        # Informo el error y lo registro.
        print(f"Error: {error}")
        logger.warning("No se pudo registrar el cliente: %s", error)

    except Exception:
        # Registro cualquier error inesperado.
        logger.exception("Error inesperado al registrar un cliente.")
        print("Ocurrió un error inesperado durante el registro.")


# Defino la función para buscar un cliente.
def buscar_cliente():

    try:
        # Solicito la identificación del cliente.
        identificador = input("Ingrese la identificación del cliente: ")

        # Busco el cliente registrado.
        cliente = gestor_clientes.buscar_cliente(identificador)

        # Muestro la información encontrada.
        print(cliente.mostrar_informacion())

        # Registro la consulta realizada.
        logger.info("Búsqueda de cliente completada.")

    except ClienteNoEncontradoError as error:
        # Informo que no se encontró el cliente.
        print(f"Error: {error}")
        logger.warning("Consulta de cliente no encontrada: %s", error)

    except Exception:
        # Registro cualquier error inesperado.
        logger.exception("Error inesperado al buscar un cliente.")
        print("Ocurrió un error inesperado durante la búsqueda.")


# Defino la función para listar los clientes.
def listar_clientes():

    try:
        # Consulto los clientes registrados.
        clientes = gestor_clientes.listar_clientes()

        # Compruebo si existen clientes.
        if not clientes:
            print("No hay clientes registrados.")
            return

        # Recorro y muestro los clientes.
        for cliente in clientes:
            print(cliente.mostrar_informacion())

        # Registro la consulta de clientes.
        logger.info("Listado de clientes consultado.")

    except Exception:
        # Registro cualquier error inesperado.
        logger.exception("Error inesperado al listar los clientes.")
        print("No fue posible consultar los clientes.")


# Defino el menú principal del sistema.
def main():

    # Registro el inicio del sistema.
    logger.info("Inicio del sistema Software FJ.")

    # Muestro el mensaje de bienvenida.
    print("----------------------------------")
    print(" BIENVENIDO AL SISTEMA SOFTWARE FJ ")
    print("----------------------------------")

    # Mantengo el menú activo hasta que el usuario decida salir.
    while True:

        print("\n----- MENÚ PRINCIPAL -----")
        print("1. Registrar cliente")
        print("2. Buscar cliente")
        print("3. Listar clientes")
        print("4. Salir")

        # Solicito la opción del usuario.
        opcion = input("Seleccione una opción: ")

        # Ejecuto la operación seleccionada.
        if opcion == "1":
            registrar_cliente()

        elif opcion == "2":
            buscar_cliente()

        elif opcion == "3":
            listar_clientes()

        elif opcion == "4":
            print("Gracias por utilizar Software FJ.")
            logger.info("El usuario finalizó el programa.")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


# Verifico si estoy ejecutando este archivo directamente.
if __name__ == "__main__":
    main()
