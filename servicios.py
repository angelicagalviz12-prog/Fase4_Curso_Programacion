from abc import abstractmethod
from math import isfinite

from entidades import Entidad
from excepciones import ServicioInvalidoError


def numero_valido(valor, campo):
    # Compruebo que el dato sea un número finito y no negativo.
    if (
        type(valor) not in (int, float)
        or (isinstance(valor, float) and not isfinite(valor))
        or valor < 0
    ):
        raise ServicioInvalidoError(f"{campo} debe ser un número válido y no negativo.")
    return valor


class Servicio(Entidad):
    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ServicioInvalidoError("El identificador del servicio es obligatorio.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio es obligatorio.")
        if not isinstance(disponible, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")

        super().__init__(identificador.strip())
        self.nombre = nombre.strip()
        self.tarifa_hora = numero_valido(tarifa_hora, "La tarifa por hora")
        self.disponible = disponible

    def mostrar_informacion(self):
        return f"{self.identificador} - {self.nombre} | Tarifa por hora: {self.tarifa_hora}"

    def calcular_costo(self, horas, descuento=0, impuesto=0):
        horas = numero_valido(horas, "La duración")
        if horas == 0:
            raise ServicioInvalidoError("La duración debe ser mayor que cero.")

        # Uso 10 para representar un 10 %.
        descuento = numero_valido(descuento, "El descuento")
        impuesto = numero_valido(impuesto, "El impuesto")
        if descuento > 100 or impuesto > 100:
            raise ServicioInvalidoError("Los porcentajes deben estar entre 0 y 100.")

        subtotal = self.calcular_subtotal(horas)
        total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)
        return round(total, 2)

    @abstractmethod
    def calcular_subtotal(self, horas):
        # Cada tipo de servicio calcula su subtotal de forma distinta.
        pass


class ServicioSala(Servicio):
    def calcular_subtotal(self, horas):
        return horas * self.tarifa_hora


class ServicioEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, cantidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if type(cantidad) is not int or cantidad < 1:
            raise ServicioInvalidoError("La cantidad de equipos debe ser un entero positivo.")
        self.cantidad = cantidad

    def calcular_subtotal(self, horas):
        return horas * self.tarifa_hora * self.cantidad


class ServicioAsesoria(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, recargo=0, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        self.recargo = numero_valido(recargo, "El recargo")

    def calcular_subtotal(self, horas):
        return horas * self.tarifa_hora + self.recargo
