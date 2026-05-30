import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import os
import subprocess


 

INTEGRANTES = """
Integrantes del grupo:

1. Nombre: JOSE ROBERTO SANDOVAL OVALLE
   Carnet: 9490 - 23 - 9630
   Sección: A
"""




class NodoLista:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamano = 0

    def agregar(self, dato):
        nuevo = NodoLista(dato)

        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo

        self.tamano += 1

    def esta_vacia(self):
        return self.primero is None

    def recorrer(self):
        actual = self.primero

        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def limpiar(self):
        self.primero = None
        self.ultimo = None
        self.tamano = 0



class PesosMovimiento:
    def __init__(self):
        self.p0 = 1
        self.p1 = 1
        self.p2 = 1
        self.p3 = 1
        self.p4 = 1
        self.p5 = 1
        self.p6 = 1
        self.p7 = 1
        self.p8 = 1

    def obtener(self, indice):
        if indice == 0:
            return self.p0
        if indice == 1:
            return self.p1
        if indice == 2:
            return self.p2
        if indice == 3:
            return self.p3
        if indice == 4:
            return self.p4
        if indice == 5:
            return self.p5
        if indice == 6:
            return self.p6
        if indice == 7:
            return self.p7
        if indice == 8:
            return self.p8

        return 0

    def aumentar(self, indice, cantidad=1):
        if indice == 0:
            self.p0 += cantidad
        elif indice == 1:
            self.p1 += cantidad
        elif indice == 2:
            self.p2 += cantidad
        elif indice == 3:
            self.p3 += cantidad
        elif indice == 4:
            self.p4 += cantidad
        elif indice == 5:
            self.p5 += cantidad
        elif indice == 6:
            self.p6 += cantidad
        elif indice == 7:
            self.p7 += cantidad
        elif indice == 8:
            self.p8 += cantidad

    def disminuir(self, indice, cantidad=1):
        valor = self.obtener(indice)

        if valor <= 1:
            return

        if indice == 0:
            self.p0 -= cantidad
            if self.p0 < 1:
                self.p0 = 1
        elif indice == 1:
            self.p1 -= cantidad
            if self.p1 < 1:
                self.p1 = 1
        elif indice == 2:
            self.p2 -= cantidad
            if self.p2 < 1:
                self.p2 = 1
        elif indice == 3:
            self.p3 -= cantidad
            if self.p3 < 1:
                self.p3 = 1
        elif indice == 4:
            self.p4 -= cantidad
            if self.p4 < 1:
                self.p4 = 1
        elif indice == 5:
            self.p5 -= cantidad
            if self.p5 < 1:
                self.p5 = 1
        elif indice == 6:
            self.p6 -= cantidad
            if self.p6 < 1:
                self.p6 = 1
        elif indice == 7:
            self.p7 -= cantidad
            if self.p7 < 1:
                self.p7 = 1
        elif indice == 8:
            self.p8 -= cantidad
            if self.p8 < 1:
                self.p8 = 1

    def texto(self):
        return (
            f"[0:{self.p0}, 1:{self.p1}, 2:{self.p2}, "
            f"3:{self.p3}, 4:{self.p4}, 5:{self.p5}, "
            f"6:{self.p6}, 7:{self.p7}, 8:{self.p8}]"
        )


class RegistroAprendizaje:
    def __init__(self, estado):
        self.estado = estado
        self.pesos = PesosMovimiento()


class NodoAprendizaje:
    def __init__(self, registro):
        self.registro = registro
        self.siguiente = None


class TablaAprendizaje:
    def __init__(self):
        self.primero = None

    def buscar(self, estado):
        actual = self.primero

        while actual is not None:
            if actual.registro.estado == estado:
                return actual.registro

            actual = actual.siguiente

        return None

    def obtener_o_crear(self, estado):
        encontrado = self.buscar(estado)

        if encontrado is not None:
            return encontrado

        nuevo_registro = RegistroAprendizaje(estado)
        nuevo_nodo = NodoAprendizaje(nuevo_registro)

        if self.primero is None:
            self.primero = nuevo_nodo
        else:
            actual = self.primero

            while actual.siguiente is not None:
                actual = actual.siguiente

            actual.siguiente = nuevo_nodo

        return nuevo_registro

    def recorrer(self):
        actual = self.primero

        while actual is not None:
            yield actual.registro
            actual = actual.siguiente

    def limpiar(self):
        self.primero = None




class RegistroPartida:
    def __init__(self, id_partida, resumen, tablero, resultado):
        self.id_partida = id_partida
        self.resumen = resumen
        self.tablero = tablero
        self.resultado = resultado

    def __str__(self):
        return (
            f"Partida #{self.id_partida}\n"
            f"Resultado: {self.resultado}\n"
            f"Resumen: {self.resumen}\n"
            f"Tablero final:\n{formatear_tablero(self.tablero)}\n"
        )


class NodoB:
    def __init__(self, grado, hoja=True):
        self.grado = grado
        self.hoja = hoja
        self.claves = []
        self.hijos = []


class ArbolB:
    def __init__(self, grado):
        self.grado = grado
        self.raiz = NodoB(grado, True)

    def insertar(self, registro):
        raiz = self.raiz

        if len(raiz.claves) == (2 * self.grado) - 1:
            nueva_raiz = NodoB(self.grado, False)
            nueva_raiz.hijos.append(raiz)
            self.dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz
            self.insertar_no_lleno(nueva_raiz, registro)
        else:
            self.insertar_no_lleno(raiz, registro)

    def insertar_no_lleno(self, nodo, registro):
        i = len(nodo.claves) - 1

        if nodo.hoja:
            nodo.claves.append(None)

            while i >= 0 and registro.id_partida < nodo.claves[i].id_partida:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1

            nodo.claves[i + 1] = registro
        else:
            while i >= 0 and registro.id_partida < nodo.claves[i].id_partida:
                i -= 1

            i += 1

            if len(nodo.hijos[i].claves) == (2 * self.grado) - 1:
                self.dividir_hijo(nodo, i)

                if registro.id_partida > nodo.claves[i].id_partida:
                    i += 1

            self.insertar_no_lleno(nodo.hijos[i], registro)

    def dividir_hijo(self, padre, indice):
        grado = self.grado
        hijo = padre.hijos[indice]
        nuevo = NodoB(grado, hijo.hoja)

        padre.claves.insert(indice, hijo.claves[grado - 1])
        padre.hijos.insert(indice + 1, nuevo)

        nuevo.claves = hijo.claves[grado:(2 * grado) - 1]
        hijo.claves = hijo.claves[0:grado - 1]

        if not hijo.hoja:
            nuevo.hijos = hijo.hijos[grado:(2 * grado)]
            hijo.hijos = hijo.hijos[0:grado]

    def buscar(self, id_partida, nodo=None):
        if nodo is None:
            nodo = self.raiz

        i = 0

        while i < len(nodo.claves) and id_partida > nodo.claves[i].id_partida:
            i += 1

        if i < len(nodo.claves) and id_partida == nodo.claves[i].id_partida:
            return nodo.claves[i]

        if nodo.hoja:
            return None

        return self.buscar(id_partida, nodo.hijos[i])

    def recorrer(self):
        resultado = []
        self._recorrer_nodo(self.raiz, resultado)
        return resultado

    def _recorrer_nodo(self, nodo, resultado):
        i = 0

        while i < len(nodo.claves):
            if not nodo.hoja:
                self._recorrer_nodo(nodo.hijos[i], resultado)

            resultado.append(nodo.claves[i])
            i += 1

        if not nodo.hoja:
            self._recorrer_nodo(nodo.hijos[i], resultado)

    def generar_dot(self, ruta):
        contenido = "digraph ArbolB {\n"
        contenido += 'node [shape=record, style=filled, fillcolor="#EFEFEF"];\n'
        contenido += self._dot_nodo(self.raiz)
        contenido += "}\n"

        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

    def _dot_nodo(self, nodo):
        nombre = f"nodo{id(nodo)}"
        etiquetas = ""

        for registro in nodo.claves:
            etiquetas += f"Partida {registro.id_partida}\\n{registro.resultado}|"

        if etiquetas.endswith("|"):
            etiquetas = etiquetas[:-1]

        texto = f'{nombre} [label="{etiquetas}"];\n'

        if not nodo.hoja:
            for hijo in nodo.hijos:
                texto += self._dot_nodo(hijo)
                texto += f"{nombre} -> nodo{id(hijo)};\n"

        return texto




def tablero_vacio():
    return "---------"


def obtener_celda(tablero, indice):
    return tablero[indice]


def colocar(tablero, indice, ficha):
    return tablero[:indice] + ficha + tablero[indice + 1:]


def tablero_lleno(tablero):
    for caracter in tablero:
        if caracter == "-":
            return False

    return True


def formatear_tablero(tablero):
    texto = ""

    for i in range(9):
        celda = tablero[i]

        if celda == "-":
            celda = " "

        texto += f" {celda} "

        if i == 2 or i == 5:
            texto += "\n---+---+---\n"
        elif i != 8:
            texto += "|"

    return texto


def verificar_ganador(tablero):
    lineas = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    for a, b, c in lineas:
        if tablero[a] != "-" and tablero[a] == tablero[b] and tablero[b] == tablero[c]:
            return tablero[a]

    if tablero_lleno(tablero):
        return "EMPATE"

    return None


def movimientos_disponibles(tablero):
    lista = ListaEnlazada()

    for i in range(9):
        if tablero[i] == "-":
            lista.agregar(i)

    return lista


def movimiento_ganador(tablero, ficha):
    disponibles = movimientos_disponibles(tablero)

    for indice in disponibles.recorrer():
        prueba = colocar(tablero, indice, ficha)

        if verificar_ganador(prueba) == ficha:
            return indice

    return None




class MotorAprendizaje:
    def __init__(self):
        self.tabla = TablaAprendizaje()
        self.instanciar_estados(tablero_vacio(), "X")

    def instanciar_estados(self, tablero, turno):
        self.tabla.obtener_o_crear(tablero)

        if verificar_ganador(tablero) is not None:
            return

        disponibles = movimientos_disponibles(tablero)

        for indice in disponibles.recorrer():
            nuevo_tablero = colocar(tablero, indice, turno)

            siguiente_turno = "O"
            if turno == "O":
                siguiente_turno = "X"

            self.instanciar_estados(nuevo_tablero, siguiente_turno)

    def elegir_movimiento_programa(self, tablero):
        ganar = movimiento_ganador(tablero, "O")

        if ganar is not None:
            return ganar

        bloquear = movimiento_ganador(tablero, "X")

        if bloquear is not None:
            return bloquear

        registro = self.tabla.obtener_o_crear(tablero)
        disponibles = movimientos_disponibles(tablero)

        mejor_indice = None
        mejor_peso = -1

        for indice in disponibles.recorrer():
            peso = registro.pesos.obtener(indice)

            if peso > mejor_peso:
                mejor_peso = peso
                mejor_indice = indice
            elif peso == mejor_peso:
                if random.randint(0, 1) == 1:
                    mejor_indice = indice

        return mejor_indice

    def reforzar(self, movimientos_programa):
        for jugada in movimientos_programa.recorrer():
            estado = jugada.estado
            indice = jugada.indice

            registro = self.tabla.obtener_o_crear(estado)
            registro.pesos.aumentar(indice, 2)

    def castigar(self, movimientos_programa):
        for jugada in movimientos_programa.recorrer():
            estado = jugada.estado
            indice = jugada.indice

            registro = self.tabla.obtener_o_crear(estado)
            registro.pesos.disminuir(indice, 1)

    def limpiar(self):
        self.tabla.limpiar()
        self.instanciar_estados(tablero_vacio(), "X")


class JugadaPrograma:
    def __init__(self, estado, indice):
        self.estado = estado
        self.indice = indice




def generar_visualizacion_partida(id_partida, movimientos_programa, tablero_final, resultado):
    carpeta = "graphviz_partidas"

    if not os.path.exists(carpeta):
        os.mkdir(carpeta)

    ruta_dot = os.path.join(carpeta, f"partida_{id_partida}.dot")
    ruta_png = os.path.join(carpeta, f"partida_{id_partida}.png")

    contenido = "digraph Partida {\n"
    contenido += 'rankdir=LR;\n'
    contenido += 'node [shape=box, style=filled, fillcolor="#E8F0FE"];\n'
    contenido += f'inicio [label="Partida #{id_partida}\\nResultado: {resultado}"];\n'

    anterior = "inicio"
    contador = 1

    for jugada in movimientos_programa.recorrer():
        nombre = f"j{contador}"
        etiqueta = (
            f"Estado antes del movimiento:\\n"
            f"{jugada.estado[0:3]}\\n{jugada.estado[3:6]}\\n{jugada.estado[6:9]}\\n"
            f"Movimiento elegido por programa: {jugada.indice}"
        )

        contenido += f'{nombre} [label="{etiqueta}"];\n'
        contenido += f"{anterior} -> {nombre};\n"

        anterior = nombre
        contador += 1

    final = (
        f"Tablero final:\\n"
        f"{tablero_final[0:3]}\\n{tablero_final[3:6]}\\n{tablero_final[6:9]}"
    )

    contenido += f'final [label="{final}", fillcolor="#DFF0D8"];\n'
    contenido += f"{anterior} -> final;\n"
    contenido += "}\n"

    with open(ruta_dot, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    try:
        subprocess.run(
            ["dot", "-Tpng", ruta_dot, "-o", ruta_png],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass


def generar_visualizacion_arbol(arbol):
    carpeta = "graphviz_partidas"

    if not os.path.exists(carpeta):
        os.mkdir(carpeta)

    ruta_dot = os.path.join(carpeta, "historial_arbol_b.dot")
    ruta_png = os.path.join(carpeta, "historial_arbol_b.png")

    arbol.generar_dot(ruta_dot)

    try:
        subprocess.run(
            ["dot", "-Tpng", ruta_dot, "-o", ruta_png],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass




class JuegoTresEnRaya:
    def __init__(self, root):
        self.root = root
        self.root.title("Totito")
        self.root.geometry("720x600")

        self.grado_arbol = simpledialog.askinteger(
            "Configuración inicial",
            "Ingrese el grado del Árbol B:",
            minvalue=2,
            maxvalue=10
        )

        if self.grado_arbol is None:
            self.grado_arbol = 2

        self.motor = MotorAprendizaje()
        self.historial = ArbolB(self.grado_arbol)

        self.contador_partidas = 0
        self.victorias_programa = 0
        self.primera_victoria_programa = None

        self.tablero = tablero_vacio()
        self.botones = []
        self.movimientos_programa_actual = ListaEnlazada()

        self.contenedor = tk.Frame(self.root)
        self.contenedor.pack(fill="both", expand=True)

        self.mostrar_menu()

    def limpiar_pantalla(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_menu(self):
        self.limpiar_pantalla()

        titulo = tk.Label(
            self.contenedor,
            text="TOTITO CONTRA LA MAQUINA",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=20)

        info = tk.Label(
            self.contenedor,
            text=f"Partidas jugadas: {self.contador_partidas} | Victorias del programa: {self.victorias_programa}",
            font=("Arial", 12)
        )
        info.pack(pady=10)

        opciones = (
            ("Entrenar manualmente", self.iniciar_partida_manual),
            ("Entrenar automáticamente", self.entrenamiento_automatico),
            ("Visualizar historial de partidas", self.mostrar_historial),
            ("Consultar iteraciones para alcanzar victoria", self.mostrar_iteraciones_victoria),
            ("Limpiar estructura de datos", self.limpiar_estructuras),
            ("Integrantes del grupo", self.mostrar_integrantes),
            ("Salir", self.root.quit),
        )

        for texto, comando in opciones:
            boton = tk.Button(
                self.contenedor,
                text=texto,
                width=40,
                height=2,
                command=comando
            )
            boton.pack(pady=5)

    def iniciar_partida_manual(self):
        self.limpiar_pantalla()

        self.tablero = tablero_vacio()
        self.movimientos_programa_actual = ListaEnlazada()
        self.botones = []

        titulo = tk.Label(
            self.contenedor,
            text="Entrenamiento Manual: Tú eres X, el programa es O",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=15)

        marco_tablero = tk.Frame(self.contenedor)
        marco_tablero.pack(pady=20)

        for i in range(9):
            boton = tk.Button(
                marco_tablero,
                text="",
                font=("Arial", 30, "bold"),
                width=4,
                height=2,
                command=lambda indice=i: self.jugada_humana(indice)
            )

            fila = i // 3
            columna = i % 3
            boton.grid(row=fila, column=columna, padx=5, pady=5)
            self.botones.append(boton)

        boton_menu = tk.Button(
            self.contenedor,
            text="Volver al menú",
            command=self.mostrar_menu
        )
        boton_menu.pack(pady=10)

    def jugada_humana(self, indice):
        if self.tablero[indice] != "-":
            return

        self.tablero = colocar(self.tablero, indice, "X")
        self.actualizar_botones()

        resultado = verificar_ganador(self.tablero)

        if resultado is not None:
            self.finalizar_partida(resultado)
            return

        estado_antes = self.tablero
        movimiento_programa = self.motor.elegir_movimiento_programa(self.tablero)

        if movimiento_programa is not None:
            self.movimientos_programa_actual.agregar(
                JugadaPrograma(estado_antes, movimiento_programa)
            )
            self.tablero = colocar(self.tablero, movimiento_programa, "O")

        self.actualizar_botones()

        resultado = verificar_ganador(self.tablero)

        if resultado is not None:
            self.finalizar_partida(resultado)

    def actualizar_botones(self):
        for i in range(9):
            valor = self.tablero[i]

            if valor == "-":
                self.botones[i].config(text="")
            else:
                self.botones[i].config(text=valor)

    def finalizar_partida(self, resultado):
        self.contador_partidas += 1

        if resultado == "O":
            texto_resultado = "Ganó el programa"
            self.victorias_programa += 1

            if self.primera_victoria_programa is None:
                self.primera_victoria_programa = self.contador_partidas

            self.motor.reforzar(self.movimientos_programa_actual)

        elif resultado == "X":
            texto_resultado = "Ganó el jugador"
            self.motor.castigar(self.movimientos_programa_actual)

        else:
            texto_resultado = "Empate"

        resumen = f"Partida manual finalizada. {texto_resultado}."
        registro = RegistroPartida(
            self.contador_partidas,
            resumen,
            self.tablero,
            texto_resultado
        )

        self.historial.insertar(registro)

        generar_visualizacion_partida(
            self.contador_partidas,
            self.movimientos_programa_actual,
            self.tablero,
            texto_resultado
        )

        generar_visualizacion_arbol(self.historial)

        messagebox.showinfo(
            "Resultado",
            f"{texto_resultado}\n\nEl programa regresará al menú principal."
        )

        self.mostrar_menu()

    def entrenamiento_automatico(self):
        cantidad = simpledialog.askinteger(
            "Entrenamiento automático",
            "Ingrese el número de partidas a simular:",
            minvalue=1,
            maxvalue=10000
        )

        if cantidad is None:
            return

        reporte = ""
        victorias_programa = 0
        victorias_jugador = 0
        empates = 0

        for _ in range(cantidad):
            resultado = self.simular_partida_automatica()

            if resultado == "Ganó el programa":
                victorias_programa += 1
            elif resultado == "Ganó el jugador automático":
                victorias_jugador += 1
            else:
                empates += 1

        reporte += "REPORTE DE ENTRENAMIENTO AUTOMÁTICO\n\n"
        reporte += f"Partidas simuladas: {cantidad}\n"
        reporte += f"Victorias del programa: {victorias_programa}\n"
        reporte += f"Victorias del jugador automático: {victorias_jugador}\n"
        reporte += f"Empates: {empates}\n"
        reporte += f"Total de partidas registradas: {self.contador_partidas}\n\n"
        reporte += "El sistema ajustó los pesos de los movimientos del programa.\n"
        reporte += "Las partidas fueron almacenadas en el Árbol B del historial.\n"

        self.mostrar_reporte(reporte)

    def simular_partida_automatica(self):
        tablero_actual = tablero_vacio()
        movimientos_programa = ListaEnlazada()

        turno = "X"

        while verificar_ganador(tablero_actual) is None:
            disponibles = movimientos_disponibles(tablero_actual)

            if turno == "X":
                cantidad = disponibles.tamano
                elegido_numero = random.randint(1, cantidad)
                contador = 1
                movimiento = None

                for indice in disponibles.recorrer():
                    if contador == elegido_numero:
                        movimiento = indice
                        break
                    contador += 1

                tablero_actual = colocar(tablero_actual, movimiento, "X")
                turno = "O"

            else:
                estado_antes = tablero_actual
                movimiento = self.motor.elegir_movimiento_programa(tablero_actual)

                if movimiento is not None:
                    movimientos_programa.agregar(
                        JugadaPrograma(estado_antes, movimiento)
                    )

                    tablero_actual = colocar(tablero_actual, movimiento, "O")

                turno = "X"

        resultado = verificar_ganador(tablero_actual)

        self.contador_partidas += 1

        if resultado == "O":
            texto_resultado = "Ganó el programa"
            self.victorias_programa += 1

            if self.primera_victoria_programa is None:
                self.primera_victoria_programa = self.contador_partidas

            self.motor.reforzar(movimientos_programa)

        elif resultado == "X":
            texto_resultado = "Ganó el jugador automático"
            self.motor.castigar(movimientos_programa)

        else:
            texto_resultado = "Empate"

        resumen = f"Partida automática simulada. {texto_resultado}."

        registro = RegistroPartida(
            self.contador_partidas,
            resumen,
            tablero_actual,
            texto_resultado
        )

        self.historial.insertar(registro)

        generar_visualizacion_partida(
            self.contador_partidas,
            movimientos_programa,
            tablero_actual,
            texto_resultado
        )

        generar_visualizacion_arbol(self.historial)

        return texto_resultado

    def mostrar_reporte(self, texto):
        self.limpiar_pantalla()

        titulo = tk.Label(
            self.contenedor,
            text="Reporte de entrenamiento automático",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        caja = tk.Text(self.contenedor, width=80, height=25)
        caja.pack(pady=10)
        caja.insert("1.0", texto)
        caja.config(state="disabled")

        boton = tk.Button(
            self.contenedor,
            text="Volver al menú",
            command=self.mostrar_menu
        )
        boton.pack(pady=10)

    def mostrar_historial(self):
        self.limpiar_pantalla()

        titulo = tk.Label(
            self.contenedor,
            text="Historial de partidas - Árbol B",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        caja = tk.Text(self.contenedor, width=80, height=25)
        caja.pack(pady=10)

        registros = self.historial.recorrer()

        if len(registros) == 0:
            caja.insert("1.0", "No hay partidas registradas todavía.")
        else:
            for registro in registros:
                caja.insert("end", str(registro))
                caja.insert("end", "\n" + "=" * 60 + "\n\n")

        caja.config(state="disabled")

        marco = tk.Frame(self.contenedor)
        marco.pack(pady=10)

        tk.Button(
            marco,
            text="Buscar partida por ID",
            command=self.buscar_partida
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            marco,
            text="Volver al menú",
            command=self.mostrar_menu
        ).grid(row=0, column=1, padx=5)

    def buscar_partida(self):
        id_partida = simpledialog.askinteger(
            "Buscar partida",
            "Ingrese el ID de la partida:"
        )

        if id_partida is None:
            return

        registro = self.historial.buscar(id_partida)

        if registro is None:
            messagebox.showwarning(
                "No encontrado",
                "No se encontró una partida con ese ID."
            )
        else:
            messagebox.showinfo(
                "Partida encontrada",
                str(registro)
            )

    def mostrar_iteraciones_victoria(self):
        if self.primera_victoria_programa is None:
            mensaje = (
                "El programa aún no ha alcanzado una victoria registrada.\n"
                "Realice entrenamiento manual o automático para generar aprendizaje."
            )
        else:
            mensaje = (
                f"El programa alcanzó su primera victoria en la partida "
                f"#{self.primera_victoria_programa}."
            )

        messagebox.showinfo("Iteraciones para victoria", mensaje)

    def limpiar_estructuras(self):
        confirmar = messagebox.askyesno(
            "Confirmar limpieza",
            "¿Desea reiniciar el aprendizaje, historial y contador de partidas?"
        )

        if not confirmar:
            return

        self.motor.limpiar()
        self.historial = ArbolB(self.grado_arbol)

        self.contador_partidas = 0
        self.victorias_programa = 0
        self.primera_victoria_programa = None

        messagebox.showinfo(
            "Limpieza completada",
            "Las estructuras de datos fueron reiniciadas correctamente."
        )

        self.mostrar_menu()

    def mostrar_integrantes(self):
        self.limpiar_pantalla()

        titulo = tk.Label(
            self.contenedor,
            text="Integrantes del grupo",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        caja = tk.Text(self.contenedor, width=80, height=20)
        caja.pack(pady=10)
        caja.insert("1.0", INTEGRANTES)
        caja.config(state="disabled")

        boton = tk.Button(
            self.contenedor,
            text="Volver al menú",
            command=self.mostrar_menu
        )
        boton.pack(pady=10)




if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoTresEnRaya(root)
    root.mainloop()
