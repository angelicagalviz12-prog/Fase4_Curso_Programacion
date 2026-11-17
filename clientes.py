# Importo el sistema de registro de eventos.
import logging

# Importo el gestor que voy a probar.
from clientes import GestorClientes

# Importo la excepción base de las operaciones de clientes.
from excepciones import ErrorCliente


# Ejecuto las pruebas únicamente al iniciar este archivo directamente.
if __name__ == "__main__":
    # Configuro el archivo de logs para esta ejecución de prueba.
    logging.basicConfig(
        filename="sistema.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        encoding="utf-8",
    )

    # Obtengo el logger de la prueba.
    logger = logging.getLogger(__name__)

    # Creo el gestor de clientes en memoria.
    gestor = GestorClientes()

    # Defino registros válidos e inválidos con datos ficticios.
    casos = [
        ("C001", "Ana Pérez", "ana@example.com"),
        ("C001", "Luis Gómez", "luis@example.com"),
        ("C002", "", "cliente@example.com"),
        ("C003", "Laura Díaz", "correo-invalido"),
        (None, "Pedro Ruiz", "pedro@example.com"),
        ("C004", "Sofía López", "sofia@example.com"),
    ]

    # Ejecuto cada caso independientemente.
    for numero, datos in enumerate(casos, start=1):
        # Intento registrar el cliente.
        try:
            cliente = gestor.registrar_cliente(*datos)

        # Capturo los errores previstos y conservo su detalle en el log.
        except ErrorCliente as error:
            logger.exception("Error en el caso de clientes %s.", numero)
            print(f"Caso {numero}: operación rechazada: {error}")

        # Muestro el resultado únicamente si el registro fue exitoso.
        else:
            print(f"Caso {numero}: {cliente.mostrar_information()}")

        # Registro el cierre del intento, tanto si fue válido como inválido.
        finally:
            logger.info("Finalizó el caso de clientes %s.", numero)

    # Muestro que el sistema continuó después de los errores.
    print(f"Clientes registrados: {len(gestor.listar_clientes())}")
