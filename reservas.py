from clientes import Cliente
from excepciones import (
    ReservaInvalidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)
from servicios import Servicio, numero_valido


class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")

        # Convierto el error de duración en un error propio de la reserva.
        try:
            horas = numero_valido(duracion, "La duración")
        except ServicioInvalidoError as error:
            raise ReservaInvalidaError("La duración de la reserva es inválida.") from error

        if horas == 0:
            raise ReservaInvalidaError("La duración debe ser mayor que cero.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = horas
        self._estado = "pendiente"
        self._total = None

    @property
    def estado(self):
        return self._estado

    @property
    def total(self):
        return self._total

    def procesar(self, descuento=0, impuesto=0):
        # Compruebo si puedo calcular el costo de esta reserva.
        if self.estado != "pendiente":
            raise ReservaInvalidaError("Solo se pueden procesar reservas pendientes.")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible.")

        return self.servicio.calcular_costo(self.duracion, descuento, impuesto)

    def confirmar(self, descuento=0, impuesto=0):
        # Cambio el estado únicamente después de obtener el total.
        total = self.procesar(descuento, impuesto)
        self._total = total
        self._estado = "confirmada"
        return total

    def cancelar(self):
        if self.estado == "cancelada":
            raise ReservaInvalidaError("La reserva ya está cancelada.")
        self._estado = "cancelada"
