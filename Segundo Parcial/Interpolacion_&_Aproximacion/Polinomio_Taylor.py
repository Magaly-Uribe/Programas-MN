import sympy as sp

def main():
    print("=== CALCULADORA DE POLINOMIO DE TAYLOR ===")
    
    # 1. Definir la variable simbólica
    x = sp.symbols('x')

    # 2. Solicitud de datos al usuario
    try:
        funcion_str = input("1. Ingresa la función (ej. sin(x), exp(x), x**2 + 1): ")
        # Mapeamos 'e' para que sea la constante de Euler (sp.E)
        transformaciones = {'e': sp.E} 
        f = sp.sympify(funcion_str, locals=transformaciones)
        
        n = int(input("2. Ingresa el grado del polinomio (n): "))
        
        x0 = float(input("3. Ingresa el punto centro (x0) donde evaluar derivadas: "))
        
        val_aprox = float(input("4. Ingresa el valor (x) que quieres aproximar: "))
        
    except (ValueError, sp.SympifyError):
        print("\nError: Asegúrate de ingresar una función válida y números correctos.")
        return

    # 3. Construcción del Polinomio
    polinomio = 0
    print(f"\n--- Construyendo el polinomio alrededor de x0 = {x0} ---")
    
    for k in range(n + 1):
        # Calcular derivada k-ésima
        derivada = f.diff(x, k)
        
        # Evaluar la derivada en x0
        derivada_en_x0 = derivada.subs(x, x0)
        
        # Crear el término: (f^(k)(x0) / k!) * (x - x0)^k
        termino = (derivada_en_x0 / sp.factorial(k)) * (x - x0)**k
        
        # Sumar al polinomio total
        polinomio += termino

    # 4. Mostrar Resultados
    print("\n" + "="*40)
    print(f"POLINOMIO RESULTANTE (Grado {n}):")
    # sp.pprint muestra la ecuación en formato 'bonito'
    sp.pprint(polinomio)
    print("="*40)

    # 5. Evaluación Numérica
    # Sustituimos la 'x' del polinomio por el valor que dio el usuario
    resultado_aprox = polinomio.subs(x, val_aprox)
    
    # Calculamos el valor real para comparar
    valor_real = f.subs(x, val_aprox)
    error = abs(valor_real - resultado_aprox)

    print(f"\nRESULTADOS DE LA APROXIMACIÓN PARA x = {val_aprox}:")
    print(f"Valor aproximado (Taylor): {float(resultado_aprox):.6f}")
    print(f"Valor real (Exacto):       {float(valor_real):.6f}")
    print(f"Error absoluto:            {float(error):.6f}")

if __name__ == "__main__":
    main()