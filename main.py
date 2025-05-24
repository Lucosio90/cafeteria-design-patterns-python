from presentacion.ui import CafeteriaUI
from negocio.servicio import ServicioCafeteria
from datos.repositorio import RepositorioPedidos

def main():
    print("======= SISTEMA DE GESTIÓN DE PEDIDOS PARA CAFETERÍA =======")
    repositorio = RepositorioPedidos()
    servicio = ServicioCafeteria(repositorio)
    ui = CafeteriaUI(servicio)
    ui.mostrar_menu()

if __name__ == "__main__":
    main()