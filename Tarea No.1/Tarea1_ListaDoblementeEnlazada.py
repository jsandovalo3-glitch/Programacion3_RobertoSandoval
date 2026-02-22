from typing import Callable, Dict
from graphviz import Digraph
import os

class Nodo:
    def __init__(self, nombre: str, apellido: str, carnet: str):
        self.nombre = nombre
        self.apellido = apellido
        self.carnet = carnet
        self.sig = None
        self.ant = None


class ListaDobleEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregarI(self, nombre: str, apellido: str, carnet: str):
        nuevo = Nodo(nombre, apellido, carnet)

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.sig = self.cabeza
            self.cabeza.ant = nuevo
            self.cabeza = nuevo


    def agregarF(self, nombre: str, apellido: str, carnet: str):
        nuevo = Nodo(nombre, apellido, carnet)

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            self.cola.sig = nuevo
            nuevo.ant = self.cola
            self.cola = nuevo

    def eliminarV(self):
        self.cabeza.sig = None

    def mostrar(self):
        actual = self.cabeza
        if actual is None:
            print("Todavia no existen registros en la Lista")
            return

        while actual is not None:
            print(f"Nombre:   {actual.nombre}")
            print(f"Apellido: {actual.apellido}")
            print(f"Carnet:   {actual.carnet}")
            print("-" * 30)
            actual = actual.sig


def pausa():
    input("\nPresione Enter para continuar...")


def limpiar():
    print("\n" * 50)


def pedir_datos():
    nombre = input("Ingrese el nombre del alumno: ").strip()
    apellido = input("Ingrese el apellido del alumno: ").strip()
    carnet = input("Ingrese el carnet del alumno: ").strip()
    return nombre, apellido, carnet


def motorMenu(titulo: str, opciones: Dict[str, tuple[str, Callable[[], None]]]):
    while True:
        limpiar()
        print(f"==== {titulo} ====")
        for key, (texto, _) in opciones.items():
            print(f"{key}) {texto}")

        op = input("Elija la accion que desea realizar con la lista: ").strip()

        if op in opciones:
            _, accion = opciones[op]
            accion()
            pausa()
        else:
            print("No ha elegido una opción existente.")
            pausa()


def main():
    lista = ListaDobleEnlazada()

    def insertarP():
        print("=== Agregar al Inicio de la Lista ===")
        nombre, apellido, carnet = pedir_datos()
        lista.agregarI(nombre, apellido, carnet)
        print("Registro al principio de la lista realizado exitosamente")

    def insertarF():
        print("=== Agregar al Final de la Lista ===")
        nombre, apellido, carnet = pedir_datos()
        lista.agregarF(nombre, apellido, carnet)
        print("Registro al final de la lista realizado exitosamente")

    def eliminar():
        print("=== Eliminar el Primer nodo de la Lista ===")
        lista.eliminarV()
        print("Primer nodo eliminado correctamente")

    def mostrar():
        print("=== Contenido de la lista ===")
        lista.mostrar()

    def salir():
        print("Cerrando...")

    opciones_menu = {
        "1": ("Insertar valor al principio de la lista", insertarP),
        "2": ("Insertar valor al final de la lista", insertarF),
        "3": ("Eliminar primer nodo de la lista", eliminar),
        "4": ("Mostrar lista", mostrar),
        "0": ("Salir", salir),
    }


    while True:
        limpiar()
        print("==== MENU ====")
        for k, (txt, _) in opciones_menu.items():
            print(f"{k}) {txt}")

        op = input("Que accion desea realizar el dia de hoy: ").strip()
        if op in opciones_menu:
            _, accion = opciones_menu[op]
            accion()
            pausa()
            if op == "0":
                break
        else:
            print("No ha elegido una opción existente.")
            pausa()


if __name__ == "__main__":
    main()
