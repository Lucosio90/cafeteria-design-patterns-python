from typing import Dict
from negocio.pedido import Pedido

class RepositorioPedidos:
    def __init__(self):
        self.pedidos: Dict[str, Pedido] = {}

    def guardar_pedido(self, pedido: Pedido) -> None:
        self.pedidos[pedido.id_pedido] = pedido

    def obtener_pedido(self, id_pedido: str) -> Pedido:
        return self.pedidos.get(id_pedido)