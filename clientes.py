# Importo las herramientas para registrar eventos.
import logging

# Importo las expresiones regulares para validar correos.
import re

# Importo la clase base del sistema.
from entidades import Entidad

# Importo las excepciones que proporcionará el módulo compartido.
from excepciones import (
    DatosClienteInvalidosError,
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
)

# Utilizo la configuración de logs del programa principal.
logger = logging.getLogger(__name__)


# Represento un cliente mediante herencia de Entidad.
class Cliente(Entidad):

    # Recibo y valido los datos obligatorios del cliente.
    def __init__(self, identificador=None, nombre=None, correo=None):
        # Valido el identificador antes de crear el objeto.
        identificador = self._validar_texto(identificador, "identificador")

        # Compruebo el nombre del cliente.
        nombre = self._validar_nombre(nombre)

        # Compruebo el formato del correo.
        correo = self._validar_correo(correo)

        # Inicializo el identificador en la clase base.
        super().__init__(identificador)

        # Almaceno el nombre en un atributo privado.
        self.__nombre = nombre

        # Almaceno el correo en un atributo privado.
        self.__correo = correo

    # Defino una validación que no necesita acceder al objeto.
    @staticmethod
    def _validar_texto(valor, campo):
        # Rechazo datos faltantes o que no sean texto.
        if not isinstance(valor, str):
            raise DatosClienteInvalidosError(f"El campo {campo} es obligatorio y debe ser texto.")

        # Elimino espacios externos.
        valor = valor.strip()

        # Rechazo cadenas vacías.
        if not valor:
            raise DatosClienteInvalidosError(f"El campo {campo} no puede estar vacío.")

        # Devuelvo el dato validado.
        return valor

    # Defino las validaciones del nombre.
    @staticmethod
    def _validar_nombre(nombre):
        # Compruebo que sea un texto no vacío.
        nombre = Cliente._validar_texto(nombre, "nombre")

        # Aplico el límite de longitud propuesto para el proyecto.
        if not 2 <= len(nombre) <= 100:
            raise DatosClienteInvalidosError("El nombre debe tener entre 2 y 100 caracteres.")

        # Verifico que el nombre contenga alguna letra.
        if not any(caracter.isalpha() for caracter in nombre):
            raise DatosClienteInvalidosError("El nombre debe contener al menos una letra.")

        # Devuelvo el nombre validado.
        return nombre

    # Defino una validación básica del correo electrónico.
    @staticmethod
    def _validar_correo(correo):
        # Compruebo que el correo sea un texto no vacío.
        correo = Cliente._validar_texto(correo, "correo")

        # Verifico su estructura básica.
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            raise DatosClienteInvalidosError("El correo electrónico tiene un formato inválido.")

        # Devuelvo el correo validado.
        return correo

    # Permito consultar el nombre sin un setter público.
    @property
    def nombre(self):
        # Devuelvo el nombre encapsulado.
        return self.__nombre

    # Permito consultar el correo sin un setter público.
    @property
    def correo(self):
        # Devuelvo el correo encapsulado.
        return self.__correo

    # Implemento el método abstracto definido en Entidad.
    def mostrar_informacion(self):
        # Construyo la descripción del cliente.
        return (
            f"Cliente: {self.nombre} | "
            f"Identificación: {self.identificador} | "
            f"Correo: {self.correo}")


# Gestiono los clientes mediante una lista en memoria.
class GestorClientes:

    # Inicializo el gestor.
    def __init__(self):
        # Creo la colección interna de clientes.
        self.__clientes = []

    # Registro clientes con datos válidos e identificadores únicos.
    def registrar_cliente(self, identificador=None, nombre=None, correo=None):
        # Creo el cliente y ejecuto sus validaciones.
        cliente = Cliente(identificador, nombre, correo)

        # Verifico si el identificador ya está registrado.
        if any(
            existente.identificador == cliente.identificador
            for existente in self.__clientes):
            raise ClienteDuplicadoError(
                "Ya existe un cliente con ese identificador.")

        # Agrego el cliente después de validar todos los datos.
        self.__clientes.append(cliente)

        # Registro el evento sin incluir datos personales.
        logger.info("Cliente registrado correctamente.")

        # Entrego el objeto para su uso en otros módulos.
        return cliente

    # Busco un cliente registrado.
    def buscar_cliente(self, identificador=None):
        # Valido el identificador recibido.
        identificador = Cliente._validar_texto(identificador, "identificador")

        # Recorro la lista interna.
        for cliente in self.__clientes:
            # Compruebo si corresponde al cliente solicitado.
            if cliente.identificador == identificador:
                # Registro la consulta exitosa.
                logger.info("Consulta de cliente realizada correctamente.")

                # Devuelvo el cliente encontrado.
                return cliente

        # Informo que el cliente no está registrado.
        raise ClienteNoEncontradoError("No existe un cliente con ese identificador.")

    # Consulto los clientes registrados.
    def listar_clientes(self):
       # Registro la consulta del listado de clientes.
        logger.info("Listado de clientes consultado.")
        
        # Devuelvo una copia para proteger la lista interna.
        return self.__clientes.copy()
