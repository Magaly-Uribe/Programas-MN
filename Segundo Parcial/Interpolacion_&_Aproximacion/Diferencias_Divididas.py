import numpy as np
import sympy as sp
import pandas as pd
import math

def diferencias_divididas_formato_libro_corregido():
    print("\n=== GENERADOR DE TABLA (FORMATO IMAGEN 3.11) ===")
    x_sym = sp.symbols('x')
    
    # --- 1. Entrada de Datos ---
    print("Opciones:")
    print("  [1] Ingresar función y puntos (Calcula Y auto)")
    print("  [2] Ingresar Tabla manual (X e Y)")
    
    modo = input("Elige (1 o 2): ")
    
    f_func = None # Corregido: Usaremos f_func en todo el código
    
    if modo == '1':
        funcion_str = input("Función f(x) (ej. ln(x), 1/x): ")
        funcion_str = funcion_str.replace('ln', 'log')
        try:
            expr = sp.sympify(funcion_str)
            f_func = sp.lambdify(x_sym, expr, modules=['numpy', 'math'])
        except:
            print("Error en la función.")
            return

    try:
        n = int(input("Número de puntos: "))
        x_datos = []
        y_datos = []
        
        print("\nIngresa los datos:")
        for i in range(n):
            xi = float(input(f"  x_{i}: "))
            x_datos.append(xi)
            if modo == '1':
                y_datos.append(f_func(xi)) # Usamos f_func
            else:
                yi = float(input(f"  f(x_{i}): "))
                y_datos.append(yi)
                
    except ValueError:
        print("Error: Ingresa números válidos.")
        return

    # --- 2. Cálculos (Matriz lógica interna) ---
    matriz_calc = np.zeros((n, n))
    matriz_calc[:, 0] = y_datos

    for j in range(1, n):
        for i in range(n - j):
            numerador = matriz_calc[i+1, j-1] - matriz_calc[i, j-1]
            denominador = x_datos[i+j] - x_datos[i]
            matriz_calc[i, j] = numerador / denominador

    # --- 3. Construcción de la Tabla Visual ---
    headers = ["i", "xi", "f[xi]"]
    for k in range(1, n):
        if k == 1: headers.append(f"f[..., xi]") # Simplificado visualmente
        else: headers.append(f"Orden {k}")

    tabla_visual = []
    for i in range(n):
        fila = [i, x_datos[i], y_datos[i]]
        for j in range(1, n):
            if i >= j:
                valor = matriz_calc[i-j, j]
                fila.append(valor)
            else:
                fila.append(None)
        tabla_visual.append(fila)

    df = pd.DataFrame(tabla_visual, columns=headers)

    # --- 4. Mostrar Resultados ---
    print("\n" + "="*60)
    print(" TABLA DE DIFERENCIAS DIVIDIDAS (Estilo Libro) ")
    print("="*60)
    pd.options.display.float_format = '{:.7f}'.format
    print(df.fillna('').to_string(index=False))
    print("="*60)

    # --- 5. Construcción del Polinomio (Texto y Matemático) ---
    
    # Coeficientes de Newton (Diagonal superior de la matriz de cálculo)
    coefs_fwd = [matriz_calc[0, j] for j in range(n)]
    
    # 5.1 Construcción Texto (Para imprimir bonito)
    pol_str = f"{coefs_fwd[0]:.7f}"
    for j in range(1, n):
        signo = " + " if coefs_fwd[j] >= 0 else " - "
        val = abs(coefs_fwd[j])
        terminos_x = "".join([f"(x - {x_datos[k]})" for k in range(j)])
        pol_str += f"{signo}{val:.7f}{terminos_x}"

    print("\nPolinomio de Interpolación (Newton):")
    print(pol_str)

    # 5.2 Construcción Simbólica (AGREGADO: Necesario para evaluar)
    pol_sym = coefs_fwd[0]
    for j in range(1, n):
        termino = coefs_fwd[j]
        for k in range(j):
            termino *= (x_sym - x_datos[k])
        pol_sym += termino

    # --- 6. Evaluación ---
    try:
        x_input = input("\n¿En qué punto 'x' deseas interpolar/evaluar? (Enter para salir): ")
        if x_input:
            x_val = float(x_input)
            
            # Evaluamos usando el polinomio simbólico creado en 5.2
            f_eval = sp.lambdify(x_sym, pol_sym)
            res_aprox = f_eval(x_val)
            
            print(f"\nResultado en x = {x_val}: {res_aprox:.6f}")
            
            # Ahora f_func sí existe
            if f_func:
                res_real = f_func(x_val)
                err = abs(res_real - res_aprox)
                print(f"Valor Real:           {res_real:.6f}")
                print(f"Error Absoluto:       {err:.6e}")
            
    except Exception as e:
        print(f"Error en la evaluación: {e}")

if __name__ == "__main__":
    diferencias_divididas_formato_libro_corregido()