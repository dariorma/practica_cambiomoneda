STOCK = {
    50000:10000,   
    20000: 52222222,   
    10000: 9856666,   
    5000: 5555555,    
    2000: 10000,   
    1000: 666666,   
    500: 100000,    
    200: 200000,    
    100: 20,    
    50: 20,     
    20: 20,     
    10: 20,     
    5: 20,      
    2: 20,      
    1: 20,      
}


def a_centimos(texto):
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
    return f"{centimos // 100},{centimos % 100:02d} EUR"


def calcular_cambio(cantidad, stock):
    
    entregado = {}
    restante = cantidad

    for d in sorted(stock, reverse=True):
        n = min(restante // d, stock[d])
        if n > 0:
            entregado[d] = n
            restante -= n * d

    if restante > 0:
        candidatas = [
            d for d in stock
            if d >= restante and stock[d] - entregado.get(d, 0) > 0
        ]
        if not candidatas:
            return None
        d = min(candidatas)
        entregado[d] = entregado.get(d, 0) + 1
        restante -= d  

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
            print("Hasta luego Fausto.")
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