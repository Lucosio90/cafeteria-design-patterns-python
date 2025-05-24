from datetime import datetime
from typing import List
from negocio.bebida import Bebida
from abc import ABC, abstractmethod

class EstrategiaDescuento(ABC):
    @abstractmethod
    def aplicar_descuento(self, precio_total: float) -> float:
        pass

    @abstractmethod
    def get_descripcion(self) -> str:
        pass

class DescuentoRegular(EstrategiaDescuento):
    def aplicar_descuento(self, precio_total: float) -> float:
        return precio_total * 0.95

    def get_descripcion(self) -> str:
        return "Descuento para clientes regulares (5%)"

class DescuentoEstudiante(EstrategiaDescuento):
    def aplicar_descuento(self, precio_total: float) -> float:
        return precio_total * 0.85

    def get_descripcion(self) -> str:
        return "Descuento para estudiantes (15%)"

class DescuentoEmpleado(EstrategiaDescuento):
    def aplicar_descuento(self, precio_total: float) -> float:
        return precio_total * 0.7

    def get_descripcion(self) -> str:
        return "Descuento para empleados (30%)"

class SinDescuento(EstrategiaDescuento):
    def aplicar_descuento(self, precio_total: float) -> float:
        return precio_total

    def get_descripcion(self) -> str:
        return "Sin descuento"

class Pedido:
    def __init__(self, cliente: str, id_pedido: str, estrategia_descuento: EstrategiaDescuento = SinDescuento()):
        self.cliente = cliente
        self.items: List[Bebida] = []
        self.estrategia_descuento = estrategia_descuento
        self.fecha = datetime.now()
        self.id_pedido = id_pedido

    def agregar_bebida(self, bebida: Bebida) -> None:
        self.items.append(bebida)

    def cambiar_estrategia_descuento(self, estrategia_descuento: EstrategiaDescuento) -> None:
        self.estrategia_descuento = estrategia_descuento

    def calcular_total(self) -> float:
        subtotal = sum(item.get_precio() for item in self.items)
        return self.estrategia_descuento.aplicar_descuento(subtotal)

    def generar_recibo(self) -> str:
        recibo = [
            "CAFETERÍA - RECIBO",
            f"Fecha: {self.fecha.strftime('%d/%m/%Y %H:%M')}",
            f"Pedido: {self.id_pedido}",
            f"Cliente: {self.cliente}",
            "--------------------------------------------",
            "DETALLE DEL PEDIDO:"
        ]
        for i, item in enumerate(self.items, 1):
            recibo.append(f"{i}. {item.get_descripcion()} - Bs {item.get_precio():.2f}")
        subtotal = sum(item.get_precio() for item in self.items)
        total = self.calcular_total()
        ahorro = subtotal - total
        recibo.extend([
            "--------------------------------------------",
            f"Subtotal: Bs {subtotal:.2f}",
            f"Descuento: {self.estrategia_descuento.get_descripcion()}",
            f"Ahorro: Bs {ahorro:.2f}",
            f"TOTAL: Bs {total:.2f}",
            "--------------------------------------------",
            "¡Gracias por su visita!"
        ])
        return "\n".join(recibo)