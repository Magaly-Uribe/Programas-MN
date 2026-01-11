import numpy as np
import math

def richardson_derivada():
    print("=== EXTRAPOLACIÓN DE RICHARDSON PARA DERIVADAS ===")
    print("Este programa calcula la derivada de una función f(x) en un punto")
    print("usando Diferencias Centradas y refinamiento de Richardson.\n")

    # --- 1. Entrada de Datos ---
    func_str = input("Ingrese la función f(x) (ej. 'x * exp(x)', 'sin(x)'): ")
    x_val = float(input("Ingrese el punto x a evaluar: "))
    h = float(input("Ingrese el paso inicial h: "))
    n = int(input("Ingrese el número de niveles (filas) de la tabla: "))

    # Definir la función de forma segura usando lambda
    # Usamos un diccionario local para permitir funciones matemáticas comunes
    allowed_funcs = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    f = lambda x: eval(func_str, {"__builtins__": None}, allowed_funcs | {'x': x})

    # --- 2. Inicialización ---
    # Matriz para guardar la tabla (n x n)
    # R[fila, columna]
    R = np.zeros((n, n))

    # --- 3. Columna 0: Diferencias Centradas (Base) ---
    # Fórmula: D(h) = (f(x+h) - f(x-h)) / 2h
    # Error inicial: O(h^2)
    for i in range(n):
        # En cada fila 'i', el paso se reduce a la mitad: h / 2^i
        current_h = h / (2**i)
        R[i, 0] = (f(x_val + current_h) - f(x_val - current_h)) / (2 * current_h)

    # --- 4. Extrapolación (Columnas siguientes) ---
    # Aquí aplicamos TU FÓRMULA:
    # M = N(h/2) + [N(h/2) - N(h)] / (2^j - 1)
    
    for k in range(1, n):  # k es el índice de la columna actual (1, 2, 3...)
        # j es el orden del error que estamos eliminando.
        # Diferencia centrada tiene errores h^2, h^4, h^6... 
        # Por tanto, para la columna k, j = 2*k
        j = 2 * k  
        factor = 1 / (2**j - 1)
        
        for i in range(k, n):  # i es la fila (siempre >= k para formar el triángulo)
            # R[i, k-1]   es la aproximación con paso más fino (h/2) -> 'N(h/2)'
            # R[i-1, k-1] es la aproximación con paso grueso (h)   -> 'N(h)'
            
            N_h2 = R[i, k-1]
            N_h  = R[i-1, k-1]
            
            # Aplicación de la fórmula
            R[i, k] = N_h2 + factor * (N_h2 - N_h)

    # --- 5. Mostrar Resultados ---
    print("\n" + "="*80)
    print(f"{'Pasos (h)':<12} | {'Dif. Centrada':<18} | {'Richardson 1':<18} | {'Richardson 2':<18} ...")
    print("-" * 80)

    for i in range(n):
        current_h = h / (2**i)
        # Formatear el valor de h
        row_str = f"h={current_h:.5f}  | "
        
        # Agregar los valores calculados de la fila
        for k in range(i + 1):
            row_str += f"{R[i, k]:.9f}        | "
        print(row_str)

    # --- 6. Análisis de Error ---
    resultado_final = R[n-1, n-1]
    print("="*80)
    print(f"\n>>> RESULTADO FINAL APROXIMADO: {resultado_final:.12f}")
    
    # Estimación del error (diferencia entre las dos últimas mejoras)
    if n > 1:
        error_est = abs(R[n-1, n-1] - R[n-1, n-2])
        print(f">>> ERROR ESTIMADO (relativo): {error_est:.5e}")

# Ejecutar el programa
if __name__ == "__main__":
    richardson_derivada()