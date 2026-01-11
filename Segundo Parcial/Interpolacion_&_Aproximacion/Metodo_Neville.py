import numpy as np
import pandas as pd
import math

# --- 1. LÓGICA MATEMÁTICA (NEVILLE) ---
def metodo_neville(x_points, y_points, x_val):
    """
    Algoritmo de Neville. Retorna el valor aproximado y la tabla.
    """
    n = len(x_points)
    # Inicializamos matriz con ceros
    Q = np.zeros((n, n))
    
    # Columna 0 = Valores de y
    for i in range(n):
        Q[i][0] = y_points[i]
        
    # Llenado de la tabla (Programación Dinámica)
    for j in range(1, n): # j = columna (grado)
        for i in range(j, n): # i = fila (punto)
            numerador = ((x_val - x_points[i-j]) * Q[i][j-1] - 
                         (x_val - x_points[i]) * Q[i-1][j-1])
            
            denominador = x_points[i] - x_points[i-j]
            
            if denominador == 0:
                raise ValueError(f"¡Error! Puntos x repetidos o división por cero entre x={x_points[i]} y x={x_points[i-j]}")
                
            Q[i][j] = numerador / denominador

    resultado = Q[n-1][n-1]
    
    # Formato visual con Pandas
    columnas = [f"Grado {k}" for k in range(n)]
    df_tabla = pd.DataFrame(Q, columns=columnas, index=x_points)
    df_tabla.replace(0, np.nan, inplace=True) # Limpieza visual
    
    return resultado, df_tabla

# --- 2. CÁLCULO DE COTA DE ERROR ---
def calcular_cota_error(x_points, x_val, max_derivada):
    n_grado = len(x_points) - 1
    
    # Producto |(x-x0)(x-x1)...|
    producto_distancias = 1
    for xi in x_points:
        producto_distancias *= (x_val - xi)
    producto_distancias = abs(producto_distancias)
    
    factorial = math.factorial(n_grado + 1)
    error = (max_derivada / factorial) * producto_distancias
    
    return error

# --- 3. UTILIDADES DE ENTRADA ---
def evaluar_funcion_usuario(funcion_str, x):
    """Evalúa strings como 'sin(x)' de forma segura."""
    contexto = {
        "sin": np.sin, "cos": np.cos, "tan": np.tan,
        "exp": np.exp, "log": np.log, "ln": np.log,
        "sqrt": np.sqrt, "pi": np.pi, "e": np.e, "abs": np.abs,
        "x": x
    }
    funcion_limpia = funcion_str.replace("^", "**") # Soporte para ^
    try:
        return eval(funcion_limpia, {"__builtins__": {}}, contexto)
    except Exception as e:
        raise ValueError(f"Error matemático: {e}")

def solicitar_float(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("⚠️ Entrada inválida. Ingresa un número (ej. 2.5, -4).")

# --- 4. FUNCIÓN PRINCIPAL ---
def main():
    print("==========================================")
    print("      MÉTODO DE INTERPOLACIÓN DE NEVILLE  ")
    print("==========================================\n")

    # --- SELECCIÓN DE MODO ---
    print("¿Cómo deseas ingresar los datos?")
    print("  [1] MANUALMENTE (Ingresar pares x, y)")
    print("  [2] POR FUNCIÓN (Ingresar f(x) y calcular y)")
    
    modo = ""
    while modo not in ["1", "2"]:
        modo = input("Selecciona una opción (1 o 2): ")

    funcion_str = None
    
    # Si es modo función, la pedimos antes de nada
    if modo == "2":
        print("\n>> Ingresa la función en términos de 'x' (ej: exp(x), x^2, sin(x)):")
        while True:
            funcion_str = input("   f(x) = ")
            try:
                evaluar_funcion_usuario(funcion_str, 1.0) # Test rápido
                print("   ✅ Función válida.")
                break
            except Exception as e:
                print(f"   ❌ Error en la sintaxis: {e}")

    # --- RECOLECCIÓN DE PUNTOS ---
    while True:
        try:
            n = int(input("\n¿Cuántos puntos (nodos) vas a usar? "))
            if n >= 2: break
            print("Se requieren al menos 2 puntos.")
        except ValueError: pass

    x_points = []
    y_points = []

    print(f"\n--- Ingreso de {n} Puntos ---")
    for i in range(n):
        print(f"\nNodo {i}:")
        xi = solicitar_float(f"   x[{i}]: ")
        x_points.append(xi)

        if modo == "1":
            # Modo Manual: Pedimos Y
            yi = solicitar_float(f"   y[{i}]: ")
            y_points.append(yi)
        else:
            # Modo Función: Calculamos Y
            yi = evaluar_funcion_usuario(funcion_str, xi)
            y_points.append(yi)
            print(f"   -> y[{i}] calculado: {yi:.6f}")

    # --- EJECUCIÓN ---
    print("\n" + "-"*30)
    x_val = solicitar_float("¿Qué valor de 'x' deseas interpolar? ")

    try:
        resultado, tabla = metodo_neville(x_points, y_points, x_val)
        
        print("\n" + "="*45)
        print(f" RESULTADO FINAL: P({x_val}) ≈ {resultado:.8f}")
        print("="*45)
        print("\n--- TABLA DE DIFERENCIAS (NEVILLE) ---")
        print(tabla)

        # --- ANÁLISIS DE ERROR ---
        # 1. Error Real (si tenemos función o el usuario lo sabe)
        valor_real = None
        
        if modo == "2":
            valor_real = evaluar_funcion_usuario(funcion_str, x_val)
        else:
            print("\n¿Conoces el valor exacto para comparar? (s/n)")
            if input().lower() == 's':
                valor_real = solicitar_float(f"Ingresa el valor real de f({x_val}): ")

        if valor_real is not None:
            error_abs = abs(valor_real - resultado)
            print("\n--- EXACTITUD ---")
            print(f"Valor Real: {valor_real:.8f}")
            print(f"Error Real: {error_abs:.8e}")

        # 2. Cota de Error Teórica (Opcional)
        print("\n" + "-"*30)
        if input("¿Calcular COTA de Error Teórica? (s/n): ").lower() == 's':
            grado = n - 1
            print(f"\nℹ️ Requerido: Máximo de la derivada orden {grado+1} en el intervalo.")
            max_derivada = solicitar_float(f"   Ingresa máx |f^({grado+1})(x)|: ")
            
            cota = calcular_cota_error(x_points, x_val, max_derivada)
            print(f"   >>> Cota Teórica: {cota:.8e}")
            
            if valor_real is not None:
                if error_abs <= cota:
                    print("   ✅ El error real respeta la cota teórica.")
                else:
                    print("   ⚠️ El error real excede la cota (revisar derivada máxima).")

    except Exception as e:
        print(f"\n❌ Ocurrió un error: {e}")

if __name__ == "__main__":
    main()