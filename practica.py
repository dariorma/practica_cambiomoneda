"""
Cambio de monedas y billetes con existencias limitadas.

Recorre las denominaciones de mayor a menor. Si con las existencias no se
puede alcanzar la cantidad exacta, se sube a la cantidad mas cercana por arriba.
Todos los importes se manejan en centimos (enteros) para evitar errores de decimales.
"""


STOCK = {
    50000: 2,   
    20000: 3,   
    10000: 5,   
    5000: 5,    
    2000: 10,   
    1000: 10,   
    500: 10,    
    200: 20,    
    100: 20,    
    50: 20,     
    20: 20,     
    10: 20,     
    5: 20,      
    2: 20,      
    1: 20,      
}


def a_centimos(texto):
    """Convierte '12,34' o '12.34' a centimos (1234). Lanza ValueError si no es valido."""
    texto = texto.strip().replace(",", ".")
    if texto.count(".") > 1:
        raise ValueError("formato incorrecto")
    entero, _, decimales = texto.partition(".")
    if len(decimales) > 2:
        raise ValueError("maximo 2 decimales")
    if not (entero or decimales) or not (entero + decimales).isdigit():
        raise ValueError("formato incorrecto")
    return int(entero or 0) * 100 + int((decimales + "00")[:2])


def formatear(centimos):
    """1234 -> '12,34 EUR'"""
    return f"{centimos // 100},{centimos % 100:02d} EUR"


def calcular_cambio(cantidad, stock):
    """
    Devuelve (entregado, total) o None si no hay existencias suficientes.
    entregado: {denominacion: unidades}
    total: importe realmente alcanzado (>= cantidad)
    """
    entregado = {}
    restante = cantidad

    # 1. De mayor a menor, tomando lo que quepa y lo que haya en caja
    for d in sorted(stock, reverse=True):
        n = min(restante // d, stock[d])
        if n > 0:
            entregado[d] = n
            restante -= n * d

    # 2. Si sobra algo, se sube a la cantidad mas cercana por arriba:
    #    la menor denominacion disponible que cubra lo que falta
    if restante > 0:
        candidatas = [
            d for d in stock
            if d >= restante and stock[d] - entregado.get(d, 0) > 0
        ]
        if not candidatas:
            return None
        d = min(candidatas)
        entregado[d] = entregado.get(d, 0) + 1
        restante -= d  # queda negativo: es lo que se pasa

    total = cantidad - restante
    return entregado, total


def nombre(d):
    tipo = "billete" if d >= 500 else "moneda"
    return f"{tipo} de {formatear(d)}"


def main():
    print("Cambio de monedas y billetes")
    while True:
        entrada = input("\nIntroduce una cantidad en euros o salir para salir del código: ")
        if entrada.strip().lower() in ("salir", "s", "q"):
            print("Hasta luego.")
            break

        try:
            cantidad = a_centimos(entrada)
        except ValueError as e:
            print(f"Cantidad no valida ({e}). Ejemplo: 137,45")
            continue

        if cantidad == 0:
            print("La cantidad debe ser mayor que 0.")
            continue

        resultado = calcular_cambio(cantidad, STOCK)
        if resultado is None:
            print("No hay existencias suficientes para alcanzar esa cantidad.")
            continue

        entregado, total = resultado
        print(f"\nCantidad pedida: {formatear(cantidad)}")
        for d in sorted(entregado, reverse=True):
            print(f"  {entregado[d]} x {nombre(d)}")
        print(f"Total de piezas: {sum(entregado.values())}")
        print(f"Total entregado: {formatear(total)}")
        if total != cantidad:
            print(f"(No se pudo dar la cantidad exacta; se alcanza la mas cercana por arriba, "
                  f"+{formatear(total - cantidad)})")


if __name__ == "__main__":
    main()