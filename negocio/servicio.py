from negocio.bebida import Bebida, BebidaFactory, Leche, Canela, Miel, Crema, Sabor
from negocio.pedido import Pedido, SinDescuento, DescuentoRegular, DescuentoEstudiante, DescuentoEmpleado
from datos.repositorio import RepositorioPedidos
from datetime import datetime

class ServicioCafeteria:
    def __init__(self, repositorio: RepositorioPedidos):
        self.repositorio = repositorio

    def crear_pedido(self, cliente: str) -> str:
        id_pedido = f"PED-{datetime.now().strftime('%Y%m%d')}-{hash(cliente) % 1000:03d}"
        self.repositorio.guardar_pedido(Pedido(cliente, id_pedido))
        return id_pedido

    def crear_bebida(self, tipo: int, tamaño: str) -> Bebida:
        return BebidaFactory.crear_bebida(tipo, tamaño)

    def agregar_ingrediente(self, bebida: Bebida, opcion: int, sabor: str = None) -> Bebida:
        if opcion == 1:
            return Leche(bebida)
        elif opcion == 2:
            return Canela(bebida)
        elif opcion == 3:
            return Miel(bebida)
        elif opcion == 4:
            return Crema(bebida)
        elif opcion == 5 and sabor:
            return Sabor(bebida, sabor)
        return bebida

    def agregar_bebida_pedido(self, id_pedido: str, bebida: Bebida) -> None:
        pedido = self.repositorio.obtener_pedido(id_pedido)
        if pedido:
            pedido.agregar_bebida(bebida)
            self.repositorio.guardar_pedido(pedido)

    def aplicar_descuento(self, id_pedido: str, tipo_descuento: str) -> None:
        pedido = self.repositorio.obtener_pedido(id_pedido)
        if pedido:
            descuento = {
                "ninguno": SinDescuento(),
                "regular": DescuentoRegular(),
                "estudiante": DescuentoEstudiante(),
                "empleado": DescuentoEmpleado()
            }.get(tipo_descuento, SinDescuento())
            pedido.cambiar_estrategia_descuento(descuento)
            self.repositorio.guardar_pedido(pedido)

    def generar_recibo(self, id_pedido: str) -> str:
        pedido = self.repositorio.obtener_pedido(id_pedido)
        return pedido.generar_recibo() if pedido else "Pedido no encontrado"

    def pedido_tiene_bebidas(self, id_pedido: str) -> bool:
        pedido = self.repositorio.obtener_pedido(id_pedido)
        return bool(pedido and pedido.items)