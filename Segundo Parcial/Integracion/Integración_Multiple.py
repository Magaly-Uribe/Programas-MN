import sympy as sp

def obtener_funcion_y_simbolos():
    """
    Pide la función y prepara las expresiones simbólicas.
    """
    print("=== CONFIGURACIÓN DE LA FUNCIÓN ===")
    f_str = input("Introduce la función f(x, y) (ej: x**2 + y*x): ")
    
    # Definimos símbolos matemáticos
    x, y = sp.symbols('x y')
    
    try:
        # Convertimos texto a expresión matemática simbólica
        expr = sp.sympify(f_str)
        # Convertimos la expresión a una función rápida para cálculos numéricos
        f_num = sp.lambdify((x, y), expr, "math")
        return expr, f_num, x, y
    except Exception as e:
        print(f"Error al interpretar la función: {e}")
        return None, None, None, None

def calcular_exacta(expr, x, y, x0, xn, y0, yn):
    """
    Resuelve la integral definida analíticamente usando SymPy.
    """
    print("\nCalculando valor exacto (analítico)... por favor espera.")
    try:
        # Integramos primero respecto a x, luego respecto a y
        valor_exacto = sp.integrate(expr, (x, x0, xn), (y, y0, yn))
        return float(valor_exacto)
    except Exception as e:
        print(f"No se pudo calcular la integral exacta simbólicamente: {e}")
        return None

def trapecio_doble(f_func, x0, xn, y0, yn, n, m):
    hx = (xn - x0) / n
    hy = (yn - y0) / m
    
    print(f"\n--- Ejecutando Trapecio (n={n}, m={m}) ---")
    suma_total = 0
    
    for i in range(n + 1):
        for j in range(m + 1):
            xi = x0 + i * hx
            yj = y0 + j * hy
            
            try:
                val = f_func(xi, yj)
            except ValueError: # Captura errores de dominio math
                 val = 0

            # Lógica de Pesos Trapecio 2D:
            # Esquinas = 1, Bordes = 2, Interior = 4
            
            es_borde_x = (i == 0 or i == n)
            es_borde_y = (j == 0 or j == m)
            
            if es_borde_x and es_borde_y:
                peso = 1
            elif not es_borde_x and not es_borde_y:
                peso = 4
            else:
                peso = 2
            
            termino = peso * val
            suma_total += termino
            
            # Mostrar solo primeras y últimas iteraciones
            if (i < 2 and j < 2) or (i > n-2 and j > m-2):
                 print(f"Iter (i={i}, j={j}): f({xi:.2f}, {yj:.2f}) * W({peso}) = {termino:.4f}")

    return (hx * hy / 4) * suma_total

def simpson_doble(f_func, x0, xn, y0, yn, n, m):
    # Ajuste forzoso a par
    if n % 2 != 0: n += 1
    if m % 2 != 0: m += 1

    hx = (xn - x0) / n
    hy = (yn - y0) / m
    
    print(f"\n--- Ejecutando Simpson 1/3 (n={n}, m={m}) ---")
    suma_total = 0
    
    # Matriz de pesos base 1D: 1, 4, 2, 4 ... 1
    
    for i in range(n + 1):
        for j in range(m + 1):
            xi = x0 + i * hx
            yj = y0 + j * hy
            
            try:
                val = f_func(xi, yj)
            except ValueError:
                val = 0
            
            # Peso en X
            if i == 0 or i == n: wx = 1
            elif i % 2 != 0: wx = 4
            else: wx = 2
            
            # Peso en Y
            if j == 0 or j == m: wy = 1
            elif j % 2 != 0: wy = 4
            else: wy = 2
            
            peso = wx * wy
            termino = peso * val
            suma_total += termino

            if (i < 2 and j < 2) or (i > n-2 and j > m-2):
                print(f"Iter (i={i}, j={j}): f({xi:.2f}, {yj:.2f}) * W({peso}) = {termino:.4f}")

    return (hx * hy / 9) * suma_total

def main():
    # 1. Obtener función y compilarla
    expr, f_num, x_sym, y_sym = obtener_funcion_y_simbolos()
    if not expr: return

    # 2. Pedir límites
    try:
        x0 = float(input("Límite inferior x (a): "))
        xn = float(input("Límite superior x (b): "))
        y0 = float(input("Límite inferior y (c): "))
        yn = float(input("Límite superior y (d): "))
    except ValueError:
        print("Error en los límites.")
        return

    # 3. Calcular EXACTA
    valor_real = calcular_exacta(expr, x_sym, y_sym, x0, xn, y0, yn)
    if valor_real is not None:
        print(f"-> Valor EXACTO calculado: {valor_real:.6f}")
    
    # 4. Seleccionar Método Numérico
    print("\nSelecciona Método Numérico:")
    print("1. Trapecio")
    print("2. Simpson 1/3")
    opcion = input("Opción: ")
    
    print("Variante:")
    print("S. Simple")
    print("C. Compuesta")
    variante = input("Opción (S/C): ").upper()

    # Definir intervalos
    n, m = 0, 0
    if opcion == '1': # Trapecio
        if variante == 'S': n, m = 1, 1
        else:
            n = int(input("Intervalos en X: "))
            m = int(input("Intervalos en Y: "))
        resultado = trapecio_doble(f_num, x0, xn, y0, yn, n, m)
        
    elif opcion == '2': # Simpson
        if variante == 'S': n, m = 2, 2
        else:
            n = int(input("Intervalos en X (par): "))
            m = int(input("Intervalos en Y (par): "))
        resultado = simpson_doble(f_num, x0, xn, y0, yn, n, m)
    else:
        print("Opción inválida.")
        return

    # 5. Resultados y Errores
    print("\n" + "="*40)
    print(f"RESULTADOS FINALES")
    print("="*40)
    print(f"Integral Exacta:     {valor_real:.6f}")
    print(f"Integral Numérica:   {resultado:.6f}")
    
    if valor_real is not None and valor_real != 0:
        error_abs = abs(valor_real - resultado)
        error_rel = (error_abs / abs(valor_real)) * 100
        print(f"Error Absoluto:      {error_abs:.6f}")
        print(f"Error Relativo (%):  {error_rel:.6f}%")
    else:
        print("Error: No se pudo calcular (Valor real es 0 o no disponible).")
    print("="*40)

if __name__ == "__main__":
    main()