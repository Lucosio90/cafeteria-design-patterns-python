from abc import ABC, abstractmethod

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