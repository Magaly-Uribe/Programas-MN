import sympy as sp

def simpson_3_8_simple(expr, x_sym, a, b):
    print("\n--- Ejecutando Simpson 3/8 SIMPLE ---")
    n = 3
    h = (b - a) / n
    
    print(f"\nDatos: a={a}, b={b}, n={n}, h={h}")
    print(f"{'i':<5} | {'x':<10} | {'f(x)':<15} | {'Coef.':<5} | {'Término':<15}")
    print("-" * 65)
    
    suma = 0
    coeficientes = [1, 3, 3, 1]
    
    for i in range(n + 1):
        xi = a + i * h
        # Evaluamos la expresión de sympy y convertimos a flotante
        yi = float(expr.subs(x_sym, xi))
        c = coeficientes[i]
        termino = c * yi
        suma += termino
        print(f"{i:<5} | {xi:<10.4f} | {yi:<15.4f} | {c:<5} | {termino:<15.4f}")
        
    resultado = (3 * h / 8) * suma
    return resultado

def simpson_3_8_compuesta(expr, x_sym, a, b, n):
    print("\n--- Ejecutando Simpson 3/8 COMPUESTA ---")
    
    if n % 3 != 0:
        print(f"⚠️ Error: Para Simpson 3/8, 'n' debe ser múltiplo de 3. (Tu n={n})")
        return None

    h = (b - a) / n
    print(f"\nDatos: a={a}, b={b}, n={n}, h={h}")
    print(f"{'i':<5} | {'x':<10} | {'f(x)':<15} | {'Coef.':<5} | {'Término':<15}")
    print("-" * 65)

    suma = 0
    
    for i in range(n + 1):
        xi = a + i * h
        yi = float(expr.subs(x_sym, xi))
        
        if i == 0 or i == n:
            c = 1
        elif i % 3 == 0:
            c = 2
        else:
            c = 3
            
        termino = c * yi
        suma += termino
        print(f"{i:<5} | {xi:<10.4f} | {yi:<15.4f} | {c:<5} | {termino:<15.4f}")

    resultado = (3 * h / 8) * suma
    return resultado

def main():
    print("=== MÉTODO DE INTEGRACIÓN SIMPSON 3/8 (CON SYMPY) ===")
    
    # Definimos el símbolo 'x' para que sympy lo reconozca
    x = sp.symbols('x')
    
    try:
        funcion_str = input("Introduce la función f(x) (ej. sin(x) + x**2): ")
        # Convertimos el string a una expresión matemática real
        expresion = sp.sympify(funcion_str)
        
        a = float(input("Límite inferior (a): "))
        b = float(input("Límite superior (b): "))
        
        opcion = input("\nSelecciona el método:\n1. Simple\n2. Compuesta\n> ")
        
        resultado_aprox = 0
        
        if opcion == "1":
            resultado_aprox = simpson_3_8_simple(expresion, x, a, b)
        elif opcion == "2":
            n = int(input("Número de intervalos (n debe ser múltiplo de 3): "))
            resultado_aprox = simpson_3_8_compuesta(expresion, x, a, b, n)
        else:
            print("Opción no válida.")
            return

        if resultado_aprox is not None:
            # --- CÁLCULO DEL VALOR EXACTO ---
            print("\nCalculando integral exacta con SymPy...")
            valor_exacto = float(sp.integrate(expresion, (x, a, b)))
            
            # Cálculo del error
            error_rel = abs((valor_exacto - resultado_aprox) / valor_exacto) * 100
            
            print("\n" + "="*40)
            print(f"RESULTADOS FINALES")
            print("="*40)
            print(f"Valor Aproximado (Simpson):  {resultado_aprox:.8f}")
            print(f"Valor Exacto (Analítico):    {valor_exacto:.8f}")
            print("-" * 40)
            print(f"Error Relativo Porcentual:     {error_rel:.6f}%")
            print("="*40)

    except sp.SympifyError:
        print("Error: La función introducida no es válida. Revisa la sintaxis (ej. usa 'x**2' no 'x^2').")
    except ValueError:
        print("Error: Asegúrate de introducir números válidos.")
    except ZeroDivisionError:
        print("Error: División por cero detectada. Revisa los límites o la función.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()