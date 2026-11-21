# Importo las herramientas necesarias para ejecutar el sistema.
import logging

# Importo la configuración de registros del sistema.
from logs import configurar_logs, obtener_logger

# Importo el gestor de clientes.
from clientes import GestorClientes

# Importo las clases para administrar los servicios.
from servicios import (
    ServicioSala,
    ServicioEquipo,
    ServicioAsesoria,)

from reservas import Reserva

# Importo las excepciones relacionadas con los clientes.
from excepciones import (
    DatosClienteInvalidosError,
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,)


# Configuro los registros del sistema.
configurar_logs()

# Obtengo el registrador del programa principal.
logger = obtener_logger(__name__)


# Creo el gestor encargado de administrar los clientes.
gestor_clientes = GestorClientes()

# Creo las listas para almacenar los servicios y las reservas.
servicios = []
reservas = []

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

# Defino la función para registrar servicios.
def registrar_servicio():

    try:
        print("\n----- REGISTRO DE SERVICIOS -----")
        print("1. Sala")
        print("2. Equipo")
        print("3. Asesoría")

        tipo = input("Seleccione el tipo de servicio: ")

        identificador = input("Ingrese el identificador: ")
        nombre = input("Ingrese el nombre del servicio: ")
        tarifa = float(input("Ingrese la tarifa por hora: "))

        # Creo el servicio según el tipo seleccionado.
        if tipo == "1":
            servicio = ServicioSala(
                identificador, nombre, tarifa)

        elif tipo == "2":
            cantidad = int(input("Ingrese la cantidad de equipos: "))

            servicio = ServicioEquipo(
                identificador, nombre, tarifa, cantidad)

        elif tipo == "3":
            recargo = float(input("Ingrese el recargo adicional: "))

            servicio = ServicioAsesoria(
                identificador, nombre, tarifa, recargo)

        else:
            print("Tipo de servicio inválido.")
            return

        # Compruebo que el identificador no esté repetido.
        if any(
            existente.identificador == servicio.identificador
            for existente in servicios
        ):
            print("Ya existe un servicio con ese identificador.")
            return

        # Almaceno el servicio registrado.
        servicios.append(servicio)

        print("Servicio registrado correctamente.")
        print(servicio.mostrar_informacion())

        logger.info("Servicio registrado correctamente.")

    except (ValueError, ServicioInvalidoError) as error:
        print(f"Error: {error}")
        logger.warning("No se pudo registrar el servicio: %s", error)

    except Exception:
        logger.exception("Error inesperado al registrar un servicio.")
        print("Ocurrió un error inesperado durante el registro.")

# Defino la función para listar los servicios.
def listar_servicios():

    try:
        # Compruebo si existen servicios registrados.
        if not servicios:
            print("No hay servicios registrados.")
            return

        print("\n----- SERVICIOS REGISTRADOS -----")

        # Recorro y muestro los servicios disponibles.
        for servicio in servicios:
            print(servicio.mostrar_informacion())
            print(f"Disponibilidad: {'Sí' if servicio.disponible else 'No'}")

        logger.info("Listado de servicios consultado.")

    except Exception:
        logger.exception("Error inesperado al listar los servicios.")
        print("No fue posible consultar los servicios.")

# Defino la función para crear reservas.
def crear_reserva():

    try:
        print("\n----- CREAR RESERVA -----")

        # Solicito la identificación del cliente.
        identificacion = input("Ingrese la identificación del cliente: ")
        cliente = gestor_clientes.buscar_cliente(identificacion)

        # Compruebo si existen servicios registrados.
        if not servicios:
            print("Primero debe registrar un servicio.")
            return

        # Muestro los servicios registrados.
        print("\nServicios disponibles:")
        for servicio in servicios:
            print(servicio.mostrar_informacion())

        # Solicito el identificador del servicio.
        identificador = input("\nIngrese el identificador del servicio: ")

        # Busco el servicio seleccionado.
        servicio = next(
            (s for s in servicios if s.identificador == identificador),
            None)

        if servicio is None:
            print("No existe un servicio con ese identificador.")
            return

        # Solicito la duración de la reserva.
        duracion = float(input("Ingrese la duración en horas: "))

        # Creo y almaceno la reserva.
        reserva = Reserva(cliente, servicio, duracion)
        reservas.append(reserva)

        print("Reserva creada correctamente.")
        print(f"Cliente: {cliente.nombre}")
        print(f"Servicio: {servicio.nombre}")
        print(f"Duración: {duracion} horas")
        print(f"Estado: {reserva.estado}")

        logger.info("Reserva creada correctamente.")

    except (
        ClienteNoEncontradoError,
        ReservaInvalidaError,
        ServicioInvalidoError
    ) as error:
        print(f"Error: {error}")
        logger.warning("No se pudo crear la reserva: %s", error)

    except ValueError:
        print("Error: debe ingresar un valor numérico válido.")

    except Exception:
        logger.exception("Error inesperado al crear una reserva.")
        print("Ocurrió un error inesperado al crear la reserva.")

  # Defino la función para listar las reservas.
def listar_reservas():

    try:
        # Compruebo si existen reservas registradas.
        if not reservas:
            print("No hay reservas registradas.")
            return

        print("\n----- RESERVAS REGISTRADAS -----")

        # Recorro y muestro la información de cada reserva.
        for indice, reserva in enumerate(reservas, start=1):
            print(f"\nReserva {indice}")
            print(f"Cliente: {reserva.cliente.nombre}")
            print(f"Servicio: {reserva.servicio.nombre}")
            print(f"Duración: {reserva.duracion} horas")
            print(f"Estado: {reserva.estado}")

            if reserva.total is not None:
                print(f"Total: ${reserva.total:.2f}")

        logger.info("Listado de reservas consultado.")

    except Exception:
        logger.exception("Error inesperado al listar las reservas.")
        print("No fue posible consultar las reservas.")

# Defino la función para confirmar reservas.
def confirmar_reserva():

    try:
        # Compruebo si existen reservas registradas.
        if not reservas:
            print("No hay reservas para confirmar.")
            return

        # Muestro las reservas registradas.
        listar_reservas()

        # Solicito el número de la reserva.
        numero = int(input("\nIngrese el número de la reserva: "))

        # Compruebo que el número sea válido.
        if numero < 1 or numero > len(reservas):
            print("El número de reserva no es válido.")
            return

        # Selecciono la reserva correspondiente.
        reserva = reservas[numero - 1]

        # Solicito los porcentajes de descuento e impuesto.
        descuento = float(input("Ingrese el descuento (%): "))
        impuesto = float(input("Ingrese el impuesto (%): "))

        # Confirmo la reserva y calculo su costo.
        total = reserva.confirmar(descuento, impuesto)

        print("Reserva confirmada correctamente.")
        print(f"Total a pagar: ${total:.2f}")

        logger.info("Reserva confirmada correctamente.")

    except (
        ReservaInvalidaError,
        ServicioInvalidoError,
        ServicioNoDisponibleError
    ) as error:
        print(f"Error: {error}")
        logger.warning("No se pudo confirmar la reserva: %s", error)

    except ValueError:
        print("Error: ingrese valores numéricos válidos.")

    except Exception:
        logger.exception("Error inesperado al confirmar una reserva.")
        print("Ocurrió un error inesperado al confirmar la reserva.")

# Defino la función para cancelar reservas.
def cancelar_reserva():

    try:
        # Compruebo si existen reservas registradas.
        if not reservas:
            print("No hay reservas para cancelar.")
            return

        # Muestro las reservas registradas.
        listar_reservas()

        # Solicito el número de la reserva.
        numero = int(input("\nIngrese el número de la reserva: "))

        # Compruebo que el número sea válido.
        if numero < 1 or numero > len(reservas):
            print("El número de reserva no es válido.")
            return

        # Selecciono la reserva correspondiente.
        reserva = reservas[numero - 1]

        # Cancelo la reserva seleccionada.
        reserva.cancelar()

        print("Reserva cancelada correctamente.")
        print(f"Estado actual: {reserva.estado}")

        logger.info("Reserva cancelada correctamente.")

    except ReservaInvalidaError as error:
        print(f"Error: {error}")
        logger.warning("No se pudo cancelar la reserva: %s", error)

    except ValueError:
        print("Error: debe ingresar un número válido.")

    except Exception:
        logger.exception("Error inesperado al cancelar una reserva.")
        print("Ocurrió un error inesperado al cancelar la reserva.")
        
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
        print("4. Registrar servicio")
        print("5. Listar servicios")
        print("6. Crear reserva")
        print("7. Listar reservas")
        print("8. Confirmar reserva")
        print("9. Cancelar reserva")
        print("10. Salir")

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
            registrar_servicio()
            
        elif opcion == "5":
            listar_servicios()
            
        elif opcion == "6":
            crear_reserva()
            
        elif opcion == "7":
            listar_reservas()
            
        elif opcion == "8":
            confirmar_reserva()
            
        elif opcion == "9":
            cancelar_reserva()
            
        elif opcion == "10":
            print("Gracias por utilizar Software FJ.")
            logger.info("El usuario finalizó el programa.")
            break
        
        else:
            print("Opción inválida. Intente nuevamente.")


# Verifico si estoy ejecutando este archivo directamente.
if __name__ == "__main__":
    main()
