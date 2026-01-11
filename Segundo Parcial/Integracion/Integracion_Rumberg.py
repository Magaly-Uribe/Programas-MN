import sympy as sp
import math

def metodo_romberg():
    print("--- INTEGRACIÓN DE ROMBERG CON CÁLCULO DE ERROR REAL ---")
    
    # 1. Configuración de variables simbólicas
    x = sp.symbols('x')
    
    # 2. Entrada de datos del usuario
    try:
        funcion_str = input("Introduce la función f(x) (ej. sin(x), x**2, exp(x)): ")
        a = float(input("Límite inferior (a): "))
        b = float(input("Límite superior (b): "))
        n = int(input("Número de filas (iteraciones) para la tabla de Romberg: "))
    except ValueError:
        print("Error: Asegúrate de ingresar números válidos.")
        return

    # 3. Convertir la entrada a una función matemática real
    # Usamos sympify para convertir el texto a ecuación simbólica
    try:
        funcion_sym = sp.sympify(funcion_str)
        # Creamos una función rápida para cálculos numéricos
        f = sp.lambdify(x, funcion_sym, "math") 
    except:
        print("Error: No se pudo interpretar la función.")
        return

    # 4. Calcular el Valor EXACTO (Solución Real)
    print("\nCalculando solución exacta...")
    valor_exacto_sym = sp.integrate(funcion_sym, (x, a, b))
    try:
        valor_exacto = float(valor_exacto_sym)
        print(f"Solución Analítica (Exacta): {valor_exacto:.10f}")
    except:
        print("No se pudo calcular un valor numérico exacto (posible integral no elemental).")
        valor_exacto = None

    # 5. Inicializar la Tabla de Romberg (Matriz R)
    # R[i][j] donde i es la fila (paso) y j es la columna (nivel de extrapolación)
    R = [[0 for _ in range(n)] for _ in range(n)]

    print("\n--- INICIANDO ITERACIONES ---")
    
    # 6. Primera columna: Regla del Trapecio (R[i][0])
    # Hacemos esto iterativamente para reutilizar puntos si quisiéramos, 
    # pero aquí usamos la fórmula directa del trapecio compuesto.
    for i in range(n):
        pasos = 2**i      # 1, 2, 4, 8, ... segmentos
        h = (b - a) / pasos
        
        # Sumatoria interna del trapecio: f(a) + 2*sum(f) + f(b)
        suma = f(a) + f(b)
        for k in range(1, pasos):
            suma += 2 * f(a + k * h)
            
        R[i][0] = (h / 2) * suma
        
    # 7. Aplicar la Fórmula de Extrapolación de Richardson
    # R[i][j] = R[i][j-1] + (R[i][j-1] - R[i-1][j-1]) / (4^j - 1)
    
    for j in range(1, n):             # Columnas (Nivel de mejora)
        for i in range(j, n):         # Filas (Tamaño de paso)
            
            # TU FÓRMULA ESTÁ AQUÍ:
            # R[i][j-1] es la estimación actual con paso h/2 (más preciso)
            # R[i-1][j-1] es la estimación previa con paso h (menos preciso)
            numerador = R[i][j-1] - R[i-1][j-1]
            denominador = 4**j - 1
            
            R[i][j] = R[i][j-1] + (numerador / denominador)

    # 8. Mostrar Resultados
    print("\n--- TABLA DE ROMBERG ---")
    print(f"{'Filas':<6} | {'Trapecio (j=0)':<18} | {'Richardson 1 (j=1)':<18} | ...")
    print("-" * 70)
    
    for i in range(n):
        fila_str = f"n={2**i:<2} | "
        for j in range(i + 1):
            fila_str += f"{R[i][j]:.10f}   "
        print(fila_str)

    # 9. Cálculo final del error
    resultado_final = R[n-1][n-1]
    print("\n--- RESULTADO FINAL ---")
    print(f"Aproximación de Romberg: {resultado_final:.10f}")
    
    if valor_exacto is not None:
        error_abs = abs(valor_exacto - resultado_final)
        # Evitar división por cero en error relativo
        if valor_exacto != 0:
            error_rel = (error_abs / abs(valor_exacto)) * 100
        else:
            error_rel = 0.0
            
        print(f"Error Absoluto: {error_abs:.2e}") # Notación científica
        print(f"Error Relativo: {error_rel:.10f}%")

# Ejecutar el programa
if __name__ == "__main__":
    metodo_romberg()