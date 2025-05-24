from typing import List
from negocio.servicio import ServicioCafeteria
from negocio.bebida import Bebida

class CafeteriaUI:
    def __init__(self, servicio: ServicioCafeteria):
        self.servicio = servicio

    def seleccionar_tamaño(self) -> str:
        print("\nSeleccione el tamaño de la bebida:")
        print("1. Pequeño")
        print("2. Mediano")
        print("3. Grande")
        opcion = int(input("Opción: ").strip())
        return {1: "pequeño", 2: "mediano", 3: "grande"}.get(opcion, "mediano")

    def seleccionar_sabor(self) -> str:
        print("\nSeleccione un sabor:")
        print("1. Vainilla")
        print("2. Caramelo")
        print("3. Avellana")
        print("4. Ninguno")
        opcion = int(input("Opción: ").strip())
        return {1: "vainilla", 2: "caramelo", 3: "avellana", 4: None}.get(opcion, None)

    def agregar_ingredientes(self, bebida: Bebida) -> Bebida:
        while True:
            print("\n¿Desea agregar un ingrediente extra?")
            print("1. Leche")
            print("2. Canela")
            print("3. Miel")
            print("4. Crema")
            print("5. Sabor")
            print("6. No agregar más ingredientes")
            opcion = int(input("Opción: ").strip())
            if opcion == 6:
                break
            bebida = self.servicio.agregar_ingrediente(bebida, opcion, self.seleccionar_sabor() if opcion == 5 else None)
        return bebida

    def seleccionar_descuento(self) -> str:
        print("\nSeleccione el tipo de descuento:")
        print("1. Ninguno")
        print("2. Cliente Regular (5%)")
        print("3. Estudiante (15%)")
        print("4. Empleado (30%)")
        opcion = int(input("Opción: ").strip())
        return {1: "ninguno", 2: "regular", 3: "estudiante", 4: "empleado"}.get(opcion, "ninguno")

    def mostrar_menu(self):
        cliente = input("Ingrese su nombre: ").strip() or "Cliente Anónimo"
        pedido_id = self.servicio.crear_pedido(cliente)
        while True:
            print("\nSeleccione una bebida:")
            print("1. Café")
            print("2. Té")
            print("3. Chocolate Caliente")
            print("4. Terminar pedido")
            try:
                opcion_bebida = int(input("Opción: ").strip())
                if opcion_bebida == 4:
                    if not self.servicio.pedido_tiene_bebidas(pedido_id):
                        print("El pedido está vacío. Agregue al menos una bebida.")
                        continue
                    break
                tamaño = self.seleccionar_tamaño()
                bebida = self.servicio.crear_bebida(opcion_bebida, tamaño)
                bebida = self.agregar_ingredientes(bebida)
                self.servicio.agregar_bebida_pedido(pedido_id, bebida)
                print(f"Bebida agregada: {bebida.get_descripcion()} - Bs {bebida.get_precio():.2f}")
            except ValueError:
                print("Selección inválida. Intente nuevamente.")
        descuento = self.seleccionar_descuento()
        self.servicio.aplicar_descuento(pedido_id, descuento)
        print("\n" + self.servicio.generar_recibo(pedido_id))
        print("\n======= PEDIDO FINALIZADO =======")