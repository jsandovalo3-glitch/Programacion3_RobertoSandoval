from typing import Callable, Dict, Tuple
import math

def convertir_a_binario(n: int) -> str:
    if n == 0:
        return "0"
    if n == 1:
        return "1"
    return convertir_a_binario(n // 2) + str(n % 2)

def contar_digitos(n: int) -> int:
    if n < 10:
        return 1
    return 1 + contar_digitos(n // 10)

def raiz_cuadrada_entera(n: int) -> int:
    if n < 0:
        raise ValueError("Ingresar un entero positivo, no negativo")
    if n < 2:
        return n  

    return calcular_raiz_cuadrada(n, 1, n // 2)


def calcular_raiz_cuadrada(n: int, low: int, high: int) -> int:
    if low > high:
        return high  

    mid = (low + high) // 2
    cuadrado = mid * mid

    if cuadrado == n:
        return mid
    elif cuadrado < n:
        return calcular_raiz_cuadrada(n, mid + 1, high)
    else:
        return calcular_raiz_cuadrada(n, low, mid - 1)
    
def suma_numeros_enteros(n:int) -> int:
    if n == 0:
        return 0
    return n + suma_numeros_enteros(n-1)
    

def pedir_numero_entero() -> int:
    while True:
        txt = input("Ingrese el numero con el que desea trabajar: ").strip()
        try:
            return int(txt)
        except ValueError:
            print("Entrada inválida. Ingrese un número entero (ej: 15).")

def limpiar():
    print("\n" * 50)

def pausa():
    input("\nPresione Enter para continuar...")

def main():
    def ingresarBinario():
        limpiar()
        print("=== Convertir numero entero a binario ===")
        numero = pedir_numero_entero()
        convertir = convertir_a_binario(numero)
        print(f"El numero {numero} convertido a binario es igual a: {convertir}")

    def contar_dig():
        limpiar()
        print("=== Contar los digitos de un numero entero ====")
        numero = pedir_numero_entero()
        contar = contar_digitos(numero)
        print(f"El numero {numero} cuenta con los digitos: {contar}")

    def raiz():
        limpiar()
        print("==== Calcular raiz cuadrada de un entero ====")
        n = pedir_numero_entero()
        r = raiz_cuadrada_entera(n)
        print(f"La raiz cuadra de {n} es igual a : {r}")

    def suma_enteros():
        limpiar()
        print("==== Suma de numeros enteros partiendo de numero ingresado ====")
        numero = pedir_numero_entero()
        suma = suma_numeros_enteros(numero)
        print(f"La suma de los enteros hasta el numero {numero} da un total de: {suma}")

    def salir():
        print("Cerrando aplicacion...")

    opciones_menu: Dict[str, Tuple[str, Callable[[], None]]] = {
        "1": ("Convertir un numero entero a binario", ingresarBinario),
        "2": ("Contar los digitos que tiene un numero entero", contar_dig),
        "3": ("Calcular raiz cuadrada de entero positivo", raiz),
        "4": ("Suma de enteros hasta numero ingresado", suma_enteros),
        "0": ("Salir y cerrar la aplicacion", salir)
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