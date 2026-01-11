import sympy as sp

def obtener_datos():
    """
    Pide la función y los límites, y devuelve:
    - La expresión simbólica (para integrar exacto)
    - La función numérica (para evaluar en el trapecio)
    - Los límites a y b
    """
    x = sp.symbols('x')  # Definimos x como variable simbólica
    
    print("\n--- CONFIGURACIÓN ---")
    expr_str = input("Introduce la función f(x) (ej. x**2, sin(x), exp(x)): ")
    
    try:
        # 1. Convertir texto a expresión matemática simbólica
        expresion = sp.sympify(expr_str)
        
        # 2. Crear una función de Python para cálculos numéricos
        # 'modules'=['math'] permite que entienda sin, cos, etc.
        f_num = sp.lambdify(x, expresion, modules=['math'])
        
        a = float(input("Límite inferior (a): "))
        b = float(input("Límite superior (b): "))
        
        return x, expresion, f_num, a, b
    except Exception as e:
        print(f"Error al procesar la función: {e}")
        return None

def trapecio_simple(f, a, b):
    h = b - a
    fa = f(a)
    fb = f(b)
    
    print("\n--- Iteraciones (Método Simple) ---")
    print(f"x0 = {a:.4f} | f(x0) = {fa:.6f}")
    print(f"x1 = {b:.4f} | f(x1) = {fb:.6f}")
    
    return (h / 2) * (fa + fb)

def trapecio_compuesto(f, a, b, n):
    h = (b - a) / n
    suma_interna = 0
    
    print(f"\n--- Tabla de Iteraciones (n={n}, h={h:.4f}) ---")
    print(f"{'i':<5} | {'x_i':<10} | {'f(x_i)':<12} | {'Peso'}")
    print("-" * 45)
    
    # x0
    f_x0 = f(a)
    print(f"{0:<5} | {a:<10.4f} | {f_x0:<12.6f} | 1")
    
    # x1 hasta x_n-1
    for i in range(1, n):
        x_i = a + i * h
        f_xi = f(x_i)
        suma_interna += f_xi
        print(f"{i:<5} | {x_i:<10.4f} | {f_xi:<12.6f} | 2")
        
    # xn
    f_xn = f(b)
    print(f"{n:<5} | {b:<10.4f} | {f_xn:<12.6f} | 1")
    
    return (h / 2) * (f_x0 + 2 * suma_interna + f_xn)

def main():
    print("=== CALCULADORA INTEGRAL: TRAPECIO VS EXACTA ===")
    
    datos = obtener_datos()
    if not datos:
        return
        
    x, expresion, f_num, a, b = datos
    
    # --- MENÚ ---
    print("\nSelecciona el método numérico:")
    print("1. Trapecio Simple")
    print("2. Trapecio Compuesto")
    opcion = input("Opción: ")
    
    val_aprox = 0
    
    if opcion == "1":
        val_aprox = trapecio_simple(f_num, a, b)
    elif opcion == "2":
        n = int(input("Número de segmentos (n): "))
        val_aprox = trapecio_compuesto(f_num, a, b, n)
    else:
        print("Opción inválida")
        return

    # --- CÁLCULO EXACTO Y ERROR ---
    print("\n" + "="*40)
    print(" RESULTADOS Y COMPARACIÓN")
    print("="*40)
    
    # 1. Calcular valor exacto usando integración simbólica
    valor_exacto_sym = sp.integrate(expresion, (x, a, b))
    valor_exacto = float(valor_exacto_sym) # Convertir a decimal
    
    # 2. Calcular errores
    error_abs = abs(valor_exacto - val_aprox)
    if valor_exacto != 0:
        error_rel = (error_abs / abs(valor_exacto)) * 100
    else:
        error_rel = 0.0 # Evitar división por cero

    print(f"Integral Exacta (Analítica):  {valor_exacto:.8f}")
    print(f"Aproximación (Trapecio):      {val_aprox:.8f}")
    print("-" * 40)
    print(f"Error Absoluto:               {error_abs:.8f}")
    print(f"Error Relativo (%):           {error_rel:.6f}%")

if __name__ == "__main__":
    main()