import numpy as np
import sympy as sp
import pandas as pd
import math

def diferencias_finitas_equiespaciadas():
    print("\n=== INTERPOLACIÓN DE NEWTON-GREGORY (EQUIESPACIADA) ===")
    s_sym = sp.symbols('s') # Variable auxiliar adimensional
    x_sym = sp.symbols('x') # Variable real para mostrar al final
    
    # --- 1. Entrada de Datos ---
    print("Opciones:")
    print("  [1] Ingresar función y puntos (Calcula Y auto)")
    print("  [2] Ingresar Tabla manual (X e Y)")
    
    modo = input("Elige (1 o 2): ")
    
    f_func = None
    if modo == '1':
        funcion_str = input("Función f(x) (ej. sin(x), exp(x)): ")
        funcion_str = funcion_str.replace('ln', 'log')
        try:
            expr = sp.sympify(funcion_str)
            f_func = sp.lambdify(x_sym, expr, modules=['numpy', 'math'])
        except:
            print("Error en la función.")
            return

    try:
        n = int(input("Número de puntos: "))
        if n < 2:
            print("Se requieren al menos 2 puntos.")
            return
            
        x_datos = []
        y_datos = []
        
        print("\nIngresa los datos:")
        for i in range(n):
            xi = float(input(f"  x_{i}: "))
            x_datos.append(xi)
            if modo == '1':
                y_datos.append(f_func(xi))
            else:
                yi = float(input(f"  f(x_{i}): "))
                y_datos.append(yi)
                
    except ValueError:
        print("Error: Ingresa números válidos.")
        return

    # --- 2. Verificación de Equiespaciamiento (Paso h) ---
    h = x_datos[1] - x_datos[0]
    es_equi = True
    tolerancia = 1e-9 # Para errores de punto flotante
    
    for i in range(1, n - 1):
        diff = x_datos[i+1] - x_datos[i]
        if abs(diff - h) > tolerancia:
            es_equi = False
            break
            
    if not es_equi:
        print("\n[ALERTA] Los puntos NO son equiespaciados.")
        print(f"Diferencia detectada distinta a h={h}.")
        print("Este método requiere paso constante. Usa el programa anterior (Diferencias Divididas General).")
        return
    else:
        print(f"\n[OK] Puntos equiespaciados detectados. Paso h = {h:.6f}")

    # --- 3. Cálculo de Tabla de Diferencias Finitas (ADELANTE) ---
    # Aquí solo restamos y_{i+1} - y_i. NO dividimos entre h.
    matriz_delta = np.zeros((n, n))
    matriz_delta[:, 0] = y_datos

    for j in range(1, n):
        for i in range(n - j):
            # Delta simple: Valor de abajo menos valor actual
            matriz_delta[i, j] = matriz_delta[i+1, j-1] - matriz_delta[i, j-1]

    # --- 4. Mostrar Tabla (Estilo Delta) ---
    headers = ["i", "xi", "y(x)"] + [f"Delta^{k}" for k in range(1, n)]
    tabla_visual = []
    
    for i in range(n):
        fila = [i, x_datos[i], y_datos[i]]
        for j in range(1, n):
            if i < n - j: # Mostrar forma triangular superior invertida (estándar forward)
                fila.append(matriz_delta[i, j])
            else:
                fila.append(None)
        tabla_visual.append(fila)

    df = pd.DataFrame(tabla_visual, columns=headers)
    pd.options.display.float_format = '{:.6f}'.format
    
    print("\n" + "="*60)
    print(" TABLA DE DIFERENCIAS FINITAS (Forward) ")
    print("="*60)
    print(df.fillna('').to_string(index=False))
    print("="*60)

    # --- 5. Construcción del Polinomio (Newton-Gregory) ---
    # P(s) = y0 + s*Delta0 + s(s-1)/2! * Delta^2 + ...
    # donde s = (x - x0) / h
    
    coefs_delta = matriz_delta[0, :] # Primera fila (Diagonal superior)
    pol_s = coefs_delta[0]
    
    # Construcción simbólica en función de 's'
    termino_s = 1
    factorial = 1
    
    for k in range(1, n):
        termino_s *= (s_sym - (k-1)) # Genera s, s(s-1), s(s-1)(s-2)...
        factorial *= k # k!
        coef_k = coefs_delta[k]
        
        termino_actual = (coef_k / factorial) * termino_s
        pol_s += termino_actual

    # Convertimos s -> (x - x0)/h para mostrarlo en función de x
    x0 = x_datos[0]
    pol_x = pol_s.subs(s_sym, (x_sym - x0) / h)

    print("\nPolinomio en función de 's' (s = (x - x0)/h):")
    print(sp.pprint(pol_s))
    
    print("\nPolinomio expandido en función de 'x' (Simplificado):")
    pol_expandido = sp.expand(pol_x)
    print(sp.pprint(sp.Poly(pol_expandido, x_sym).as_expr()))

    # --- 6. Evaluación ---
    try:
        val_input = input("\n¿En qué punto 'x' deseas interpolar? (Enter para salir): ")
        if val_input:
            x_val = float(val_input)
            
            # Calculamos 's' para el punto deseado
            s_val = (x_val - x0) / h
            
            # Evaluamos usando la fórmula en s (es más estable numéricamente)
            f_eval_s = sp.lambdify(s_sym, pol_s)
            res_aprox = f_eval_s(s_val)
            
            print(f"\nResultados en x = {x_val} (s = {s_val:.4f}):")
            print(f"Interpolación:        {res_aprox:.6f}")
            
            if f_func:
                res_real = f_func(x_val)
                err = abs(res_real - res_aprox)
                print(f"Valor Real:           {res_real:.6f}")
                print(f"Error Absoluto:       {err:.6e}")
                
    except Exception as e:
        print(f"Error en la evaluación: {e}")

if __name__ == "__main__":
    diferencias_finitas_equiespaciadas()