import sympy as sp

def simpson_1_3():
    print("--- MÉTODO DE INTEGRACIÓN DE SIMPSON 1/3 ---")
    
    # 1. Definir la variable simbólica y pedir la función
    x = sp.symbols('x')
    
    try:
        funcion_str = input("Introduce la función f(x) (ej. x**2 + 1, exp(x), sin(x)): ")
        f = sp.sympify(funcion_str) # Convierte texto a función matemática
    except:
        print("Error: La función no es válida. Revisa la sintaxis (usa ** para potencias).")
        return

    # 2. Pedir límites de integración
    try:
        a = float(input("Límite inferior (a): "))
        b = float(input("Límite superior (b): "))
    except ValueError:
        print("Error: Los límites deben ser números.")
        return

    # 3. Selección del método
    print("\nSelecciona el método:")
    print("1. Simpson 1/3 Simple (n=2)")
    print("2. Simpson 1/3 Compuesto (n > 2)")
    opcion = input("Tu elección (1 o 2): ")

    if opcion == '1':
        n = 2
        tipo = "Simple"
    elif opcion == '2':
        try:
            n = int(input("Número de sub-intervalos (n debe ser PAR): "))
            if n % 2 != 0:
                print("Error: Para Simpson 1/3, 'n' DEBE ser par.")
                return
            if n < 2:
                print("Error: 'n' debe ser mayor o igual a 2.")
                return
            tipo = "Compuesto"
        except ValueError:
            print("Error: n debe ser un número entero.")
            return
    else:
        print("Opción no válida.")
        return

    # 4. Cálculos Iniciales
    h = (b - a) / n
    suma = 0
    
    print(f"\n--- Resultados ({tipo}) ---")
    print(f"Paso h = {h}")
    print(f"{'i':<5} | {'xi':<12} | {'f(xi)':<15} | {'Multiplicador':<13} | {'Término'}")
    print("-" * 65)

    # 5. Iteraciones (Tabla)
    # Convertimos la función simbólica a una función lambda para evaluar rápido
    f_num = sp.lambdify(x, f, "math")

    termino_acumulado = 0

    for i in range(n + 1):
        xi = a + i * h
        try:
            f_xi = f_num(xi)
        except ValueError: 
             # Manejo de errores matemáticos (ej. log(-1))
            print(f"Error evaluando la función en {xi}")
            return

        # Determinar el multiplicador (Coeficiente)
        if i == 0 or i == n:
            coef = 1
        elif i % 2 != 0: # Impar
            coef = 4
        else: # Par
            coef = 2
        
        termino = coef * f_xi
        suma += termino

        # Mostrar la fila de la "iteración"
        print(f"{i:<5} | {xi:<12.4f} | {f_xi:<15.4f} | {coef:<13} | {termino:.4f}")

    # 6. Cálculo Final
    resultado_aproximado = (h / 3) * suma

    # 7. Cálculo del Error Real (Comparando con la integral exacta)
    try:
        integral_exacta = float(sp.integrate(f, (x, a, b)))
        error_absoluto = abs(integral_exacta - resultado_aproximado)
        
        # Opcional: Cálculo del error porcentual relativo
        if integral_exacta != 0:
            error_relativo = (error_absoluto / abs(integral_exacta)) * 100
        else:
            error_relativo = 0
            
    except:
        integral_exacta = "No calculable simbólicamente"
        error_absoluto = "N/A"
        error_relativo = "N/A"

    print("-" * 65)
    print(f"Resultado Aproximado (Simpson): {resultado_aproximado:.6f}")
    
    if isinstance(integral_exacta, float):
        print(f"Resultado Exacto (Integral):    {integral_exacta:.6f}")
        print(f"Error Absoluto:                 {error_absoluto:.6e}")
        print(f"Error Relativo Porcentual:      {error_relativo:.4f}%")
    else:
        print("Nota: No se pudo calcular la integral exacta para comparar el error.")

# Ejecutar el programa
if __name__ == "__main__":
    simpson_1_3()