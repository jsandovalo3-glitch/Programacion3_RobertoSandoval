import csv
import os
from typing import Optional


class NodoAVL:
    def __init__(self, valor: int):
        self.valor = valor
        self.izq: Optional["NodoAVL"] = None
        self.der: Optional["NodoAVL"] = None
        self.altura = 1


class ArbolAVL:
    def __init__(self):
        self.raiz: Optional[NodoAVL] = None

    def obtener_altura(self, nodo: Optional[NodoAVL]) -> int:
        if nodo is None:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo: Optional[NodoAVL]) -> int:
        if nodo is None:
            return 0
        return self.obtener_altura(nodo.izq) - self.obtener_altura(nodo.der)

    def actualizar_altura(self, nodo: NodoAVL) -> None:
        nodo.altura = 1 + max(self.obtener_altura(nodo.izq), self.obtener_altura(nodo.der))

    def rotar_derecha(self, y: NodoAVL) -> NodoAVL:
        x = y.izq
        t2 = x.der

        x.der = y
        y.izq = t2

        self.actualizar_altura(y)
        self.actualizar_altura(x)

        return x

    def rotar_izquierda(self, x: NodoAVL) -> NodoAVL:
        y = x.der
        t2 = y.izq

        y.izq = x
        x.der = t2

        self.actualizar_altura(x)
        self.actualizar_altura(y)

        return y

    def insertar(self, valor: int) -> None:
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo: Optional[NodoAVL], valor: int) -> NodoAVL:
        if nodo is None:
            return NodoAVL(valor)

        if valor < nodo.valor:
            nodo.izq = self._insertar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._insertar(nodo.der, valor)
        else:
            return nodo

        self.actualizar_altura(nodo)
        balance = self.obtener_balance(nodo)

        if balance > 1 and valor < nodo.izq.valor:
            return self.rotar_derecha(nodo)

        if balance < -1 and valor > nodo.der.valor:
            return self.rotar_izquierda(nodo)

        if balance > 1 and valor > nodo.izq.valor:
            nodo.izq = self.rotar_izquierda(nodo.izq)
            return self.rotar_derecha(nodo)

        if balance < -1 and valor < nodo.der.valor:
            nodo.der = self.rotar_derecha(nodo.der)
            return self.rotar_izquierda(nodo)

        return nodo

    def buscar(self, valor: int) -> bool:
        return self._buscar(self.raiz, valor)

    def _buscar(self, nodo: Optional[NodoAVL], valor: int) -> bool:
        if nodo is None:
            return False

        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar(nodo.izq, valor)
        else:
            return self._buscar(nodo.der, valor)

    def eliminar(self, valor: int) -> None:
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo: Optional[NodoAVL], valor: int) -> Optional[NodoAVL]:
        if nodo is None:
            return nodo

        if valor < nodo.valor:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq

            temp = self.obtener_minimo(nodo.der)
            nodo.valor = temp.valor
            nodo.der = self._eliminar(nodo.der, temp.valor)

        if nodo is None:
            return nodo

        self.actualizar_altura(nodo)
        balance = self.obtener_balance(nodo)

        if balance > 1 and self.obtener_balance(nodo.izq) >= 0:
            return self.rotar_derecha(nodo)

        if balance > 1 and self.obtener_balance(nodo.izq) < 0:
            nodo.izq = self.rotar_izquierda(nodo.izq)
            return self.rotar_derecha(nodo)

        if balance < -1 and self.obtener_balance(nodo.der) <= 0:
            return self.rotar_izquierda(nodo)

        if balance < -1 and self.obtener_balance(nodo.der) > 0:
            nodo.der = self.rotar_derecha(nodo.der)
            return self.rotar_izquierda(nodo)

        return nodo

    def obtener_minimo(self, nodo: NodoAVL) -> NodoAVL:
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual


    def inorden(self) -> list[int]:
        elementos = []
        self._inorden(self.raiz, elementos)
        return elementos

    def _inorden(self, nodo: Optional[NodoAVL], elementos: list[int]) -> None:
        if nodo:
            self._inorden(nodo.izq, elementos)
            elementos.append(nodo.valor)
            self._inorden(nodo.der, elementos)


    def cargar_desde_csv(self, ruta_archivo: str) -> None:
        with open(ruta_archivo, mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                for dato in fila:
                    dato = dato.strip()
                    if dato:
                        try:
                            numero = int(dato)
                            self.insertar(numero)
                        except ValueError:
                            print(f"Se ignoró un valor no válido: {dato}")

  
    def generar_dot(self, nombre_archivo: str = "arbol_avl") -> str:
        contenido = ["digraph AVL {", "node [shape=circle];"]

        if self.raiz is None:
            contenido.append('vacio [label="Árbol vacío"];')
        else:
            self._generar_dot_nodos(self.raiz, contenido)

        contenido.append("}")
        ruta_dot = f"{nombre_archivo}.dot"

        with open(ruta_dot, "w", encoding="utf-8") as archivo:
            archivo.write("\n".join(contenido))

        return ruta_dot

    def _generar_dot_nodos(self, nodo: Optional[NodoAVL], contenido: list[str]) -> None:
        if nodo is None:
            return

        contenido.append(f'nodo_{id(nodo)} [label="{nodo.valor}"];')

        if nodo.izq:
            contenido.append(f"nodo_{id(nodo)} -> nodo_{id(nodo.izq)};")
            self._generar_dot_nodos(nodo.izq, contenido)

        if nodo.der:
            contenido.append(f"nodo_{id(nodo)} -> nodo_{id(nodo.der)};")
            self._generar_dot_nodos(nodo.der, contenido)

    def visualizar_graphviz(self, nombre_archivo: str = "arbol_avl") -> None:
        ruta_dot = self.generar_dot(nombre_archivo)
        ruta_png = f"{nombre_archivo}.png"

        comando = f'dot -Tpng "{ruta_dot}" -o "{ruta_png}"'
        resultado = os.system(comando)

        if resultado == 0:
            print(f"\nImagen generada correctamente: {ruta_png}")
        else:
            print("\nNo se pudo generar la imagen.")
            print("Asegúrate de tener Graphviz instalado y que el comando 'dot' funcione en tu sistema.")
            print(f"Archivo .dot generado: {ruta_dot}")


def pedir_entero(mensaje: str) -> Optional[int]:
    try:
        return int(input(mensaje).strip())
    except ValueError:
        print("Debe ingresar un número entero válido.")
        return None


def mostrar_menu() -> None:
    print("\n==== MENÚ ÁRBOL AVL ====")
    print("1) Insertar un número")
    print("2) Buscar un número")
    print("3) Eliminar un número")
    print("4) Cargar árbol desde archivo CSV")
    print("5) Visualizar árbol con Graphviz")
    print("6) Mostrar recorrido inorden")
    print("7) Salir")


def main():
    arbol = ArbolAVL()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            numero = pedir_entero("Ingrese el número a insertar: ")
            if numero is not None:
                arbol.insertar(numero)
                print(f"Se insertó el número {numero} correctamente.")

        elif opcion == "2":
            numero = pedir_entero("Ingrese el número a buscar: ")
            if numero is not None:
                encontrado = arbol.buscar(numero)
                if encontrado:
                    print(f"El número {numero} SÍ existe en el árbol.")
                else:
                    print(f"El número {numero} NO existe en el árbol.")

        elif opcion == "3":
            numero = pedir_entero("Ingrese el número a eliminar: ")
            if numero is not None:
                if arbol.buscar(numero):
                    arbol.eliminar(numero)
                    print(f"Se eliminó el número {numero} correctamente.")
                else:
                    print(f"El número {numero} no existe en el árbol.")

        elif opcion == "4":
            ruta = input("Ingrese la ruta del archivo CSV: ").strip()
            try:
                arbol.cargar_desde_csv(ruta)
                print("Datos cargados correctamente desde el archivo CSV.")
            except FileNotFoundError:
                print("No se encontró el archivo indicado.")
            except Exception as e:
                print(f"Ocurrió un error al cargar el archivo: {e}")

        elif opcion == "5":
            nombre = input("Ingrese el nombre base del archivo (sin extensión): ").strip()
            if not nombre:
                nombre = "arbol_avl"
            arbol.visualizar_graphviz(nombre)

        elif opcion == "6":
            recorrido = arbol.inorden()
            print("Recorrido inorden:", recorrido)

        elif opcion == "7":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
