import math
import sympy as sp

def main():
    print("=== Generador de Tabla de Derivación (2, 3 y 5 Puntos) ===")
    
    # 1. Ingreso de Datos
    # Usamos sintaxis segura para 'e'
    f_str = input("Ingrese la función f(x) (ej: 3*x**3 + cos(2*x-8)*exp(x)): ")
    
    try:
        x0_str = input("Ingrese el valor inicial (x0): ")
        # Permitimos cosas como '0' o 'pi'
        x0 = float(eval(x0_str, {"pi": math.pi, "e": math.e}))
        
        h = float(input("Ingrese el paso (h): "))
        n = int(input("Ingrese el número de puntos (n): "))
    except ValueError:
        print("Error: Los valores numéricos no son válidos.")
        return

    # 2. Preparar la función real (Symbolic)
    x_sym = sp.symbols('x')
    try:
        # Corrección para que 'e' sea detectado como numero de Euler
        expr = sp.sympify(f_str, locals={'e': sp.E})
        f_num = sp.lambdify(x_sym, expr, "math")
        
        # Derivada analítica para la columna Real
        diff_expr = sp.diff(expr, x_sym)
        df_real = sp.lambdify(x_sym, diff_expr, "math")
    except Exception as e:
        print(f"Error al interpretar la función: {e}")
        return

    # 3. Generar la lista de datos
    X = []
    Y = []
    
    for i in range(n):
        xi = x0 + i * h
        try:
            yi = f_num(xi)
        except:
            yi = 0.0 # Manejo de error si la funcion se indefne
        X.append(xi)
        Y.append(yi)

    # 4. Construir la Tabla
    # Ajustamos el ancho para que quepan todas las columnas
    print("\n" + "="*130)
    print(f"{'i':<3} | {'xi':<8} | {'f(xi)':<12} | {'f\'(2 Pts)':<15} | {'f\'(3 Pts)':<15} | {'f\'(5 Pts)':<15} | {'Real':<15} | {'Err%(5p)':<10}")
    print("="*130)

    for i in range(n):
        xi = X[i]
        fi = Y[i]
        
        try:
            real_val = df_real(xi)
        except:
            real_val = 0.0
        
        # --- LÓGICA PARA 2 PUNTOS ---
        d2 = None
        # Prioridad: Adelante (i+1). Si es el ultimo, usar Atras (i-1)
        if i < n - 1:
            d2 = (Y[i+1] - Y[i]) / h # Adelante
        elif i > 0:
            d2 = (Y[i] - Y[i-1]) / h # Atrás (solo para la ultima fila)

        # --- LÓGICA PARA 3 PUNTOS ---
        d3 = None
        # 1. Centrada
        if i > 0 and i < n - 1:
            d3 = (Y[i+1] - Y[i-1]) / (2*h)
        # 2. Adelante (Inicio)
        elif i <= n - 3:
            d3 = (-3*Y[i] + 4*Y[i+1] - Y[i+2]) / (2*h)
        # 3. Atrás (Fin)
        elif i >= 2:
            d3 = (3*Y[i] - 4*Y[i-1] + Y[i-2]) / (2*h)

        # --- LÓGICA PARA 5 PUNTOS ---
        d5 = None
        # 1. Centrada
        if i >= 2 and i <= n - 3:
            d5 = (-Y[i+2] + 8*Y[i+1] - 8*Y[i-1] + Y[i-2]) / (12*h)
        # 2. Adelante (Borde Izquierdo Extremo)
        elif i <= n - 5:
            d5 = (-25*Y[i] + 48*Y[i+1] - 36*Y[i+2] + 16*Y[i+3] - 3*Y[i+4]) / (12*h)
        # 3. Atrás (Borde Derecho Extremo)
        elif i >= 4:
            d5 = (25*Y[i] - 48*Y[i-1] + 36*Y[i-2] - 16*Y[i-3] + 3*Y[i-4]) / (12*h)

        # --- Formateo de Salida ---
        s_d2 = f"{d2:.5f}" if d2 is not None else "---"
        s_d3 = f"{d3:.5f}" if d3 is not None else "---"
        s_d5 = f"{d5:.5f}" if d5 is not None else "---"
        
        # Error Relativo (Comparando la mejor aprox disponible (5pts) vs Real)
        # Si no hay 5pts, usamos 3pts para calcular el error visual
        val_comparacion = d5 if d5 is not None else d3
        
        if val_comparacion is not None and real_val != 0:
            err = abs((real_val - val_comparacion) / real_val) * 100
            s_err = f"{err:.4f}%"
        else:
            s_err = "---"

        print(f"{i:<3} | {xi:<8.4f} | {fi:<12.5f} | {s_d2:<15} | {s_d3:<15} | {s_d5:<15} | {real_val:<15.5f} | {s_err:<10}")

    print("="*130)

if __name__ == "__main__":
    main()