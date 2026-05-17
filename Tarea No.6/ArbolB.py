import csv
from graphviz import Source


class NodoB:
    def __init__(self, grado, hoja=True):
        self.grado = grado
        self.hoja = hoja
        self.claves = []
        self.hijos = []


class ArbolB:
    def __init__(self, grado):
        self.grado = grado
        self.raiz = NodoB(grado)

    def buscar(self, clave, nodo=None):
        if nodo is None:
            nodo = self.raiz

        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and clave == nodo.claves[i]:
            return True

        if nodo.hoja:
            return False

        return self.buscar(clave, nodo.hijos[i])

    def insertar(self, clave):
        raiz = self.raiz

        if len(raiz.claves) == (2 * self.grado) - 1:
            nueva_raiz = NodoB(self.grado, hoja=False)
            nueva_raiz.hijos.append(raiz)
            self.dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz

        self.insertar_no_lleno(self.raiz, clave)

    def insertar_no_lleno(self, nodo, clave):
        i = len(nodo.claves) - 1

        if nodo.hoja:
            nodo.claves.append(None)

            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1

            nodo.claves[i + 1] = clave
        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1

            i += 1

            if len(nodo.hijos[i].claves) == (2 * self.grado) - 1:
                self.dividir_hijo(nodo, i)

                if clave > nodo.claves[i]:
                    i += 1

            self.insertar_no_lleno(nodo.hijos[i], clave)

    def dividir_hijo(self, padre, indice):
        grado = self.grado
        hijo = padre.hijos[indice]
        nuevo = NodoB(grado, hijo.hoja)

        padre.claves.insert(indice, hijo.claves[grado - 1])
        padre.hijos.insert(indice + 1, nuevo)

        nuevo.claves = hijo.claves[grado:]
        hijo.claves = hijo.claves[:grado - 1]

        if not hijo.hoja:
            nuevo.hijos = hijo.hijos[grado:]
            hijo.hijos = hijo.hijos[:grado]


    def eliminar(self, clave):
        if not self.buscar(clave):
            print(f"La clave {clave} no existe en el árbol.")
            return

        self._eliminar(self.raiz, clave)


        if len(self.raiz.claves) == 0 and not self.raiz.hoja:
            self.raiz = self.raiz.hijos[0]

    def _eliminar(self, nodo, clave):
        t = self.grado
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and clave == nodo.claves[i]:
    
            if nodo.hoja:
                nodo.claves.pop(i)

          
            else:
                hijo_izq = nodo.hijos[i]
                hijo_der = nodo.hijos[i + 1]

                if len(hijo_izq.claves) >= t:
                    predecesor = self.obtener_predecesor(hijo_izq)
                    nodo.claves[i] = predecesor
                    self._eliminar(hijo_izq, predecesor)

                elif len(hijo_der.claves) >= t:
                    sucesor = self.obtener_sucesor(hijo_der)
                    nodo.claves[i] = sucesor
                    self._eliminar(hijo_der, sucesor)

                else:
                    self._fusionar(nodo, i)
                    self._eliminar(hijo_izq, clave)

        else:
            if nodo.hoja:
                return  

            if len(nodo.hijos[i].claves) < t:
                self._completar(nodo, i)
                i = 0
                while i < len(nodo.claves) and clave > nodo.claves[i]:
                    i += 1

            self._eliminar(nodo.hijos[i], clave)

    def _completar(self, padre, i):
        t = self.grado

        if i > 0 and len(padre.hijos[i - 1].claves) >= t:
            self._rotar_desde_izquierda(padre, i)

        elif i < len(padre.hijos) - 1 and len(padre.hijos[i + 1].claves) >= t:
            self._rotar_desde_derecha(padre, i)

        else:
            if i < len(padre.hijos) - 1:
                self._fusionar(padre, i)
            else:
                self._fusionar(padre, i - 1)

    def _rotar_desde_izquierda(self, padre, i):
        hijo = padre.hijos[i]
        hermano = padre.hijos[i - 1]

        hijo.claves.insert(0, padre.claves[i - 1])
        padre.claves[i - 1] = hermano.claves.pop()

        if not hermano.hoja:
            hijo.hijos.insert(0, hermano.hijos.pop())

    def _rotar_desde_derecha(self, padre, i):
        hijo = padre.hijos[i]
        hermano = padre.hijos[i + 1]

        hijo.claves.append(padre.claves[i])
        padre.claves[i] = hermano.claves.pop(0)

        if not hermano.hoja:
            hijo.hijos.append(hermano.hijos.pop(0))

    def _fusionar(self, padre, i):
        hijo_izq = padre.hijos[i]
        hijo_der = padre.hijos[i + 1]

        hijo_izq.claves.append(padre.claves.pop(i))
        padre.hijos.pop(i + 1)

        hijo_izq.claves.extend(hijo_der.claves)
        hijo_izq.hijos.extend(hijo_der.hijos)

    def obtener_predecesor(self, nodo):
        while not nodo.hoja:
            nodo = nodo.hijos[-1]
        return nodo.claves[-1]

    def obtener_sucesor(self, nodo):
        while not nodo.hoja:
            nodo = nodo.hijos[0]
        return nodo.claves[0]

 
    def cargar_csv(self, ruta):
        try:
            with open(ruta, newline="", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)

                for fila in lector:
                    for dato in fila:
                        if dato.strip().isdigit():
                            self.insertar(int(dato.strip()))

            print("Datos cargados correctamente.")
        except FileNotFoundError:
            print("No se encontró el archivo.")


    def mostrar(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz

        print("Nivel", nivel, nodo.claves)

        for hijo in nodo.hijos:
            self.mostrar(hijo, nivel + 1)


    def generar_graphviz(self, archivo="arbol_b"):
        dot = archivo + ".dot"
        png = archivo + ".png"

        with open(dot, "w", encoding="utf-8") as f:
            f.write("digraph ArbolB {\n")
            f.write('    node [shape=record fontname="Helvetica"];\n')
            f.write("    rankdir=TB;\n")
            self._graphviz_nodo(self.raiz, f)
            f.write("}\n")

        try:
            Source.from_file(dot).render(
                filename=archivo,
                format="png",
                cleanup=True
            )
            print(f"Imagen generada correctamente: {png}")
        except Exception as e:
            print("Se generó el archivo .dot, pero no se pudo crear la imagen.")
            print("Verifica que Graphviz esté instalado: https://graphviz.org/download/")
            print("Error:", e)

    def _graphviz_nodo(self, nodo, archivo):
        nodo_id = id(nodo)

        if nodo.claves:
            etiqueta = "|".join(str(clave) for clave in nodo.claves)
        else:
            etiqueta = " "

        archivo.write(f'    nodo{nodo_id} [label="{etiqueta}"];\n')

        for hijo in nodo.hijos:
            hijo_id = id(hijo)
            self._graphviz_nodo(hijo, archivo)
            archivo.write(f"    nodo{nodo_id} -> nodo{hijo_id};\n")



def menu():
    grado = int(input("Ingrese el grado mínimo del Árbol B: "))
    arbol = ArbolB(grado)

    while True:
        print("\n===== MENÚ ÁRBOL B =====")
        print("1. Insertar clave")
        print("2. Buscar clave")
        print("3. Eliminar clave")
        print("4. Cargar datos desde CSV")
        print("5. Mostrar árbol en consola")
        print("6. Generar imagen Graphviz")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clave = int(input("Ingrese la clave a insertar: "))
            arbol.insertar(clave)
            print("Clave insertada correctamente.")

        elif opcion == "2":
            clave = int(input("Ingrese la clave a buscar: "))
            if arbol.buscar(clave):
                print("La clave sí existe en el árbol.")
            else:
                print("La clave no existe en el árbol.")

        elif opcion == "3":
            clave = int(input("Ingrese la clave a eliminar: "))
            arbol.eliminar(clave)
            print("Proceso de eliminación finalizado.")

        elif opcion == "4":
            ruta = input("Ingrese el nombre del archivo CSV: ")
            arbol.cargar_csv(ruta)

        elif opcion == "5":
            arbol.mostrar()

        elif opcion == "6":
            nombre = input("Nombre del archivo de salida (sin extensión) [arbol_b]: ").strip()
            if not nombre:
                nombre = "arbol_b"
            arbol.generar_graphviz(nombre)

        elif opcion == "7":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
