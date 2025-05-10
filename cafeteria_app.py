from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

# PATRÓN CREACIONAL: FACTORY METHOD 

# Factory Method define una interfaz para crear bebidas, permitiendo que las
# subclases decidan qué clase instanciar.   Se se usa para crear diferentes
# tipos de bebidas (Café, Té, Chocolate Caliente)
class Bebida(ABC):
    def __init__(self, tamaño: str = "mediano"):
        self.tamaño = tamaño.lower()
        self.nombre = ""
        self.precio_base = 0.0

    def get_precio(self) -> float:
        multiplicador = {"pequeño": 0.8, "mediano": 1.0, "grande": 1.2}
        return self.precio_base * multiplicador.get(self.tamaño, 1.0)

    def get_descripcion(self) -> str:
        return f"{self.nombre} ({self.tamaño})"

class Cafe(Bebida):
    def __init__(self, tamaño: str = "mediano"):
        super().__init__(tamaño)
        self.nombre = "Café"
        self.precio_base = 10.0

class Te(Bebida):
    def __init__(self, tamaño: str = "mediano"):
        super().__init__(tamaño)
        self.nombre = "Té"
        self.precio_base = 8.0

class Chocolate(Bebida):
    def __init__(self, tamaño: str = "mediano"):
        super().__init__(tamaño)
        self.nombre = "Chocolate Caliente"
        self.precio_base = 12.0

class BebidaFactory:
    @staticmethod
    def crear_bebida(tipo: int, tamaño: str) -> Bebida:
        if tipo == 1:
            return Cafe(tamaño)
        elif tipo == 2:
            return Te(tamaño)
        elif tipo == 3:
            return Chocolate(tamaño)
        else:
            raise ValueError("Tipo de bebida inválido")

# PATRÓN ESTRUCTURAL: DECORATOR
# El patrón Decorator permite añadir ingredientes y sabores a las bebidas
# dinámicamente. Aquí se usa para agregar leche, canela, miel, crema y sabores

class IngredienteExtra(Bebida):
    def __init__(self, bebida: Bebida):
        self.bebida = bebida
        self.nombre = bebida.nombre
        self.tamaño = bebida.tamaño
        self.precio_base = bebida.precio_base

    def get_precio(self) -> float:
        return self.bebida.get_precio()

    def get_descripcion(self) -> str:
        return self.bebida.get_descripcion()

class Leche(IngredienteExtra):
    def get_precio(self) -> float:
        return self.bebida.get_precio() + 2.0

    def get_descripcion(self) -> str:
        return f"{self.bebida.get_descripcion()} con Leche"

class Canela(IngredienteExtra):
    def get_precio(self) -> float:
        return self.bebida.get_precio() + 1.5

    def get_descripcion(self) -> str:
        return f"{self.bebida.get_descripcion()} con Canela"

class Miel(IngredienteExtra):
    def get_precio(self) -> float:
        return self.bebida.get_precio() + 1.0

    def get_descripcion(self) -> str:
        return f"{self.bebida.get_descripcion()} con Miel"

class Crema(IngredienteExtra):
    def get_precio(self) -> float:
        return self.bebida.get_precio() + 1.5

    def get_descripcion(self) -> str:
        return f"{self.bebida.get_descripcion()} con Crema"

class Sabor(IngredienteExtra):
    def __init__(self, bebida: Bebida, sabor: str):
        super().__init__(bebida)
        self.sabor = sabor

    def get_precio(self) -> float:
        return self.bebida.get_precio() + 1.0

    def get_descripcion(self) -> str:
        return f"{self.bebida.get_descripcion()} con sabor a {self.sabor}"
    
# PATRÓN DE COMPORTAMIENTO: STRATEGY
# El patrón Strategy permite aplicar diferentes descuentos al total del pedido.
# Las estrategias incluyen descuentos para clientes regulares, estudiantes,
# empleados, y sin descuento.
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

# CLASE PRINCIPAL: PEDIDO
class Pedido:
    def __init__(self, cliente: str, estrategia_descuento: EstrategiaDescuento = SinDescuento()):
        self.cliente = cliente
        self.items: List[Bebida] = []
        self.estrategia_descuento = estrategia_descuento
        self.fecha = datetime.now()
        self.id_pedido = f"PED-{self.fecha.strftime('%Y%m%d')}-{hash(cliente) % 1000:03d}"

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

# INTERFAZ DE USUARIO
def seleccionar_tamaño() -> str:
    print("\nSeleccione el tamaño de la bebida:")
    print("1. Pequeño")
    print("2. Mediano")
    print("3. Grande")
    while True:
        try:
            opcion = int(input("Opción: ").strip())
            if opcion == 1:
                return "pequeño"
            elif opcion == 2:
                return "mediano"
            elif opcion == 3:
                return "grande"
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def seleccionar_sabor() -> str:
    print("\nSeleccione un sabor:")
    print("1. Vainilla")
    print("2. Caramelo")
    print("3. Avellana")
    print("4. Ninguno")
    while True:
        try:
            opcion = int(input("Opción: ").strip())
            if opcion == 1:
                return "vainilla"
            elif opcion == 2:
                return "caramelo"
            elif opcion == 3:
                return "avellana"
            elif opcion == 4:
                return None
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def agregar_ingredientes(bebida: Bebida) -> Bebida:
    while True:
        print("\n¿Desea agregar un ingrediente extra?")
        print("1. Leche")
        print("2. Canela")
        print("3. Miel")
        print("4. Crema")
        print("5. Sabor (vainilla, caramelo, avellana)")
        print("6. No agregar más ingredientes")
        try:
            opcion = int(input("Opción: ").strip())
        except ValueError:
            print("Opción inválida. Intente nuevamente.")
            continue

        if opcion == 1:
            bebida = Leche(bebida)
            print("Añadido: Leche (+Bs 2.0)")
        elif opcion == 2:
            bebida = Canela(bebida)
            print("Añadido: Canela (+Bs 1.5)")
        elif opcion == 3:
            bebida = Miel(bebida)
            print("Añadido: Miel (+Bs 1.0)")
        elif opcion == 4:
            bebida = Crema(bebida)
            print("Añadido: Crema (+Bs 1.5)")
        elif opcion == 5:
            sabor = seleccionar_sabor()
            if sabor:
                bebida = Sabor(bebida, sabor)
                print(f"Añadido: Sabor a {sabor} (+Bs 1.0)")
        elif opcion == 6:
            break
        else:
            print("Opción inválida. Intente nuevamente.")
    return bebida

def seleccionar_descuento() -> EstrategiaDescuento:
    print("\nSeleccione el tipo de descuento:")
    print("1. Ninguno")
    print("2. Cliente Regular (5%)")
    print("3. Estudiante (15%)")
    print("4. Empleado (30%)")
    while True:
        try:
            opcion = int(input("Opción: ").strip())
            if opcion == 1:
                return SinDescuento()
            elif opcion == 2:
                return DescuentoRegular()
            elif opcion == 3:
                return DescuentoEstudiante()
            elif opcion == 4:
                return DescuentoEmpleado()
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def main():
    print("======= SISTEMA DE GESTIÓN DE PEDIDOS PARA CAFETERÍA =======")
    cliente = input("Ingrese su nombre: ").strip() or "Cliente Anónimo"
    pedido = Pedido(cliente)
    while True:
        print("\nSeleccione una bebida:")
        print("1. Café")
        print("2. Té")
        print("3. Chocolate Caliente")
        print("4. Terminar pedido")
        try:
            opcion_bebida = int(input("Opción: ").strip())
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")
            continue

        if opcion_bebida == 4:
            if not pedido.items:
                print("El pedido está vacío. Agregue al menos una bebida.")
                continue
            break

        tamaño = seleccionar_tamaño()
        try:
            bebida = BebidaFactory.crear_bebida(opcion_bebida, tamaño)
        except ValueError:
            print("Selección inválida. Intente nuevamente.")
            continue

        bebida = agregar_ingredientes(bebida)
        pedido.agregar_bebida(bebida)
        print(f"\nBebida agregada: {bebida.get_descripcion()} - Bs {bebida.get_precio():.2f}")

    # Seleccionar estrategia de descuento
    estrategia_descuento = seleccionar_descuento()
    pedido.cambiar_estrategia_descuento(estrategia_descuento)

    # Mostrar recibo
    print("\nProcesando pedido...")
    print(pedido.generar_recibo())
    print("\n======= PEDIDO FINALIZADO =======")

if __name__ == "__main__":
    main()