# Creo excepciones personalizados para controlar los errores del sistema.

# Defino una excepción para los datos inválidos de los clientes.
class DatosClienteInvalidoError(Exception):
    pass

# Defino una excepción para evitar el registro de clientes duplicados.
class ClienteDuplicadoError(Exception):
    pass

# Defino una excepción para indicar que un cliente no fue encontrado.
class ClienteNoEncontradoError(Exception):
    pass
