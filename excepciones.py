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
# Defino una excepción para los servicios con datos inválidos.
class ServicioInvalidoError(Exception):
    pass

# Defino una excepción para los servicios que no están disponibles.
class ServicioNoDisponibleError(Exception):
    pass

# Defino una excepción para las reservas con datos inválidos.
class ReservaInvalidaError(Exception):
    pass
