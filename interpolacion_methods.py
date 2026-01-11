"""
Métodos Numéricos para Interpolación
ESCOM - IPN

Incluye:
- Diferencias Divididas de Newton
- Newton-Gregory (Equiespaciado)
- Método de Neville
- Polinomio de Taylor
"""

import numpy as np
import sympy as sp
from typing import List, Tuple, Optional
import math


class DiferenciasDivididas:
    """Interpolación por Diferencias Divididas de Newton."""
    
    def __init__(self, precision: int = 7):
        self.precision = precision
        self.steps = []
    
    def calcular_desde_funcion(self, funcion_str: str, x_datos: List[float]) -> Tuple[np.ndarray, List[str]]:
        """
        Calcular diferencias divididas desde una función.
        
        Args:
            funcion_str: String de la función
            x_datos: Lista de puntos x
        """
        x_sym = sp.symbols('x')
        expr = sp.sympify(funcion_str.replace('ln', 'log'), locals={'e': sp.E})
        f_func = sp.lambdify(x_sym, expr, modules=['math'])
        
        y_datos = [f_func(x) for x in x_datos]
        return self.calcular(x_datos, y_datos, f_func)
    
    def calcular(self, x_datos: List[float], y_datos: List[float], 
                 f_func: Optional[callable] = None) -> Tuple[np.ndarray, sp.Expr, List[str]]:
        """
        Calcular tabla de diferencias divididas y polinomio interpolante.
        
        Returns:
            matriz: Tabla de diferencias divididas
            polinomio: Expresión simbólica del polinomio
            steps: Procedimiento detallado
        """
        self.steps = []
        n = len(x_datos)
        
        self.steps.append("=" * 70)
        self.steps.append("DIFERENCIAS DIVIDIDAS DE NEWTON")
        self.steps.append("=" * 70)
        
        # Mostrar datos iniciales
        self.steps.append("\nDatos de entrada:")
        for i, (x, y) in enumerate(zip(x_datos, y_datos)):
            self.steps.append(f"  x_{i} = {x}, f(x_{i}) = {y:.{self.precision}f}")
        
        # Construir tabla
        matriz = np.zeros((n, n))
        matriz[:, 0] = y_datos
        
        self.steps.append("\n" + "-" * 70)
        self.steps.append("CÁLCULO DE DIFERENCIAS DIVIDIDAS")
        self.steps.append("-" * 70)
        self.steps.append("f[xᵢ, xⱼ] = [f[xᵢ₊₁,...,xⱼ] - f[xᵢ,...,xⱼ₋₁]] / (xⱼ - xᵢ)")
        
        for j in range(1, n):
            self.steps.append(f"\nOrden {j}:")
            for i in range(n - j):
                numerador = matriz[i+1, j-1] - matriz[i, j-1]
                denominador = x_datos[i+j] - x_datos[i]
                matriz[i, j] = numerador / denominador
                self.steps.append(f"  f[x_{i},...,x_{i+j}] = ({matriz[i+1,j-1]:.{self.precision}f} - {matriz[i,j-1]:.{self.precision}f}) / ({x_datos[i+j]} - {x_datos[i]})")
                self.steps.append(f"              = {matriz[i,j]:.{self.precision}f}")
        
        # Construir polinomio
        x_sym = sp.symbols('x')
        coefs = [matriz[0, j] for j in range(n)]
        
        polinomio = coefs[0]
        for j in range(1, n):
            termino = coefs[j]
            for k in range(j):
                termino *= (x_sym - x_datos[k])
            polinomio += termino
        
        polinomio_expandido = sp.expand(polinomio)
        
        self.steps.append("\n" + "-" * 70)
        self.steps.append("TABLA DE DIFERENCIAS DIVIDIDAS")
        self.steps.append("-" * 70)
        
        # Encabezado
        header = f"{'i':<4} {'xᵢ':<10} {'f[xᵢ]':<15}"
        for j in range(1, n):
            header += f" {'Orden '+str(j):<15}"
        self.steps.append(header)
        self.steps.append("-" * (30 + 15*(n-1)))
        
        for i in range(n):
            row = f"{i:<4} {x_datos[i]:<10.4f} {y_datos[i]:<15.{self.precision}f}"
            for j in range(1, n):
                if i <= n - j - 1:
                    row += f" {matriz[i,j]:<15.{self.precision}f}"
                else:
                    row += f" {'':<15}"
            self.steps.append(row)
        
        self.steps.append("\n" + "=" * 70)
        self.steps.append("POLINOMIO INTERPOLANTE")
        self.steps.append("=" * 70)
        
        # Forma de Newton
        pol_str = f"P(x) = {coefs[0]:.{self.precision}f}"
        for j in range(1, n):
            signo = " + " if coefs[j] >= 0 else " - "
            terminos_x = "·".join([f"(x - {x_datos[k]})" for k in range(j)])
            pol_str += f"{signo}{abs(coefs[j]):.{self.precision}f}·{terminos_x}"
        self.steps.append(f"\nForma de Newton:\n{pol_str}")
        
        self.steps.append(f"\nForma expandida:\nP(x) = {polinomio_expandido}")
        
        self.f_func = f_func
        self.polinomio = polinomio
        self.x_datos = x_datos
        
        return matriz, polinomio, self.steps
    
    def evaluar(self, x_val: float) -> Tuple[float, Optional[float], List[str]]:
        """Evaluar el polinomio en un punto."""
        x_sym = sp.symbols('x')
        f_eval = sp.lambdify(x_sym, self.polinomio)
        resultado = float(f_eval(x_val))
        
        steps = []
        steps.append(f"\nEvaluación en x = {x_val}:")
        steps.append(f"  P({x_val}) = {resultado:.{self.precision}f}")
        
        if self.f_func is not None:
            real = self.f_func(x_val)
            error = abs(real - resultado)
            steps.append(f"  Valor real: f({x_val}) = {real:.{self.precision}f}")
            steps.append(f"  Error absoluto: {error:.2e}")
            return resultado, real, steps
        
        return resultado, None, steps


class NewtonGregory:
    """Interpolación de Newton-Gregory para datos equiespaciados."""
    
    def __init__(self, precision: int = 6):
        self.precision = precision
        self.steps = []
    
    def calcular(self, x_datos: List[float], y_datos: List[float], 
                 f_func: Optional[callable] = None) -> Tuple[np.ndarray, sp.Expr, List[str]]:
        """
        Interpolación Newton-Gregory (diferencias finitas hacia adelante).
        
        Returns:
            matriz: Tabla de diferencias finitas
            polinomio: Expresión simbólica
            steps: Procedimiento
        """
        self.steps = []
        n = len(x_datos)
        
        # Verificar equiespaciamiento
        h = x_datos[1] - x_datos[0]
        for i in range(1, n - 1):
            if abs((x_datos[i+1] - x_datos[i]) - h) > 1e-9:
                raise ValueError("Los puntos no son equiespaciados")
        
        self.steps.append("=" * 70)
        self.steps.append("NEWTON-GREGORY (DIFERENCIAS FINITAS)")
        self.steps.append("=" * 70)
        self.steps.append(f"Paso h = {h}")
        
        # Tabla de diferencias finitas
        matriz = np.zeros((n, n))
        matriz[:, 0] = y_datos
        
        for j in range(1, n):
            for i in range(n - j):
                matriz[i, j] = matriz[i+1, j-1] - matriz[i, j-1]
        
        self.steps.append("\n" + "-" * 70)
        self.steps.append("TABLA DE DIFERENCIAS FINITAS")
        self.steps.append("-" * 70)
        
        # Mostrar tabla
        header = f"{'i':<4} {'xᵢ':<10} {'yᵢ':<12}"
        for k in range(1, n):
            header += f" {'Δ^'+str(k)+'y':<12}"
        self.steps.append(header)
        self.steps.append("-" * (26 + 12*(n-1)))
        
        for i in range(n):
            row = f"{i:<4} {x_datos[i]:<10.4f} {y_datos[i]:<12.{self.precision}f}"
            for j in range(1, n):
                if i < n - j:
                    row += f" {matriz[i,j]:<12.{self.precision}f}"
            self.steps.append(row)
        
        # Construir polinomio en s
        s_sym = sp.symbols('s')
        x_sym = sp.symbols('x')
        x0 = x_datos[0]
        
        coefs = matriz[0, :]
        pol_s = coefs[0]
        
        termino_s = sp.Integer(1)
        factorial = 1
        
        for k in range(1, n):
            termino_s *= (s_sym - (k-1))
            factorial *= k
            pol_s += (coefs[k] / factorial) * termino_s
        
        # Convertir a x
        pol_x = pol_s.subs(s_sym, (x_sym - x0) / h)
        pol_expandido = sp.expand(pol_x)
        
        self.steps.append("\n" + "=" * 70)
        self.steps.append("POLINOMIO INTERPOLANTE")
        self.steps.append("=" * 70)
        self.steps.append(f"\nEn función de s (s = (x - {x0})/{h}):")
        self.steps.append(f"P(s) = {sp.expand(pol_s)}")
        self.steps.append(f"\nEn función de x:")
        self.steps.append(f"P(x) = {pol_expandido}")
        
        self.f_func = f_func
        self.polinomio = pol_x
        self.pol_s = pol_s
        self.h = h
        self.x0 = x0
        
        return matriz, pol_expandido, self.steps
    
    def evaluar(self, x_val: float) -> Tuple[float, Optional[float], List[str]]:
        """Evaluar el polinomio."""
        s_sym = sp.symbols('s')
        s_val = (x_val - self.x0) / self.h
        
        f_eval_s = sp.lambdify(s_sym, self.pol_s)
        resultado = float(f_eval_s(s_val))
        
        steps = []
        steps.append(f"\nEvaluación en x = {x_val} (s = {s_val:.4f}):")
        steps.append(f"  P({x_val}) = {resultado:.{self.precision}f}")
        
        if self.f_func is not None:
            real = self.f_func(x_val)
            error = abs(real - resultado)
            steps.append(f"  Valor real: {real:.{self.precision}f}")
            steps.append(f"  Error: {error:.2e}")
            return resultado, real, steps
        
        return resultado, None, steps


class MetodoNeville:
    """Método de interpolación de Neville."""
    
    def __init__(self, precision: int = 8):
        self.precision = precision
        self.steps = []
    
    def calcular(self, x_datos: List[float], y_datos: List[float], 
                 x_val: float) -> Tuple[float, np.ndarray, List[str]]:
        """
        Método de Neville para interpolación.
        
        Args:
            x_datos, y_datos: Puntos conocidos
            x_val: Punto a interpolar
            
        Returns:
            resultado: Valor interpolado
            Q: Tabla de Neville
            steps: Procedimiento
        """
        self.steps = []
        n = len(x_datos)
        
        self.steps.append("=" * 70)
        self.steps.append("MÉTODO DE NEVILLE")
        self.steps.append("=" * 70)
        self.steps.append(f"Punto a interpolar: x = {x_val}")
        
        self.steps.append("\nDatos:")
        for i, (x, y) in enumerate(zip(x_datos, y_datos)):
            self.steps.append(f"  x_{i} = {x}, y_{i} = {y:.{self.precision}f}")
        
        # Inicializar tabla
        Q = np.zeros((n, n))
        Q[:, 0] = y_datos
        
        self.steps.append("\n" + "-" * 70)
        self.steps.append("FÓRMULA DE NEVILLE")
        self.steps.append("-" * 70)
        self.steps.append("Q[i,j] = [(x-xᵢ₋ⱼ)·Q[i,j-1] - (x-xᵢ)·Q[i-1,j-1]] / (xᵢ - xᵢ₋ⱼ)")
        
        # Llenar tabla
        for j in range(1, n):
            self.steps.append(f"\nGrado {j}:")
            for i in range(j, n):
                numerador = ((x_val - x_datos[i-j]) * Q[i, j-1] - 
                            (x_val - x_datos[i]) * Q[i-1, j-1])
                denominador = x_datos[i] - x_datos[i-j]
                
                if abs(denominador) < 1e-15:
                    raise ValueError(f"Puntos repetidos: x_{i-j} = x_{i}")
                
                Q[i, j] = numerador / denominador
                self.steps.append(f"  Q[{i},{j}] = [({x_val}-{x_datos[i-j]})·{Q[i,j-1]:.6f} - ({x_val}-{x_datos[i]})·{Q[i-1,j-1]:.6f}] / ({x_datos[i]}-{x_datos[i-j]})")
                self.steps.append(f"         = {Q[i,j]:.{self.precision}f}")
        
        resultado = Q[n-1, n-1]
        
        # Mostrar tabla completa
        self.steps.append("\n" + "-" * 70)
        self.steps.append("TABLA DE NEVILLE")
        self.steps.append("-" * 70)
        
        header = f"{'xᵢ':<10}"
        for j in range(n):
            header += f" {'Q[·,'+str(j)+']':<15}"
        self.steps.append(header)
        self.steps.append("-" * (10 + 15*n))
        
        for i in range(n):
            row = f"{x_datos[i]:<10.4f}"
            for j in range(n):
                if j <= i:
                    row += f" {Q[i,j]:<15.{self.precision}f}"
                else:
                    row += f" {'':<15}"
            self.steps.append(row)
        
        self.steps.append("\n" + "=" * 70)
        self.steps.append("RESULTADO")
        self.steps.append("=" * 70)
        self.steps.append(f"P({x_val}) ≈ {resultado:.{self.precision}f}")
        
        return resultado, Q, self.steps


class PolinomioTaylor:
    """Aproximación por polinomio de Taylor."""
    
    def __init__(self, precision: int = 6):
        self.precision = precision
        self.steps = []
    
    def calcular(self, funcion_str: str, x0: float, n: int, 
                 x_eval: Optional[float] = None) -> Tuple[sp.Expr, Optional[float], List[str]]:
        """
        Construir polinomio de Taylor de grado n.
        
        Args:
            funcion_str: Función a aproximar
            x0: Punto central
            n: Grado del polinomio
            x_eval: Punto donde evaluar (opcional)
            
        Returns:
            polinomio: Expresión simbólica
            resultado: Valor en x_eval (si se proporciona)
            steps: Procedimiento
        """
        self.steps = []
        x = sp.symbols('x')
        
        # Parsear función
        transformaciones = {'e': sp.E}
        f = sp.sympify(funcion_str, locals=transformaciones)
        
        self.steps.append("=" * 70)
        self.steps.append("POLINOMIO DE TAYLOR")
        self.steps.append("=" * 70)
        self.steps.append(f"Función: f(x) = {f}")
        self.steps.append(f"Centro: x₀ = {x0}")
        self.steps.append(f"Grado: n = {n}")
        
        self.steps.append("\n" + "-" * 70)
        self.steps.append("CÁLCULO DE DERIVADAS Y TÉRMINOS")
        self.steps.append("-" * 70)
        self.steps.append("T(x) = Σ [f⁽ᵏ⁾(x₀)/k!] · (x - x₀)ᵏ")
        
        polinomio = sp.Integer(0)
        derivada_actual = f
        
        for k in range(n + 1):
            # Evaluar derivada en x0
            valor_derivada = derivada_actual.subs(x, x0)
            
            # Calcular término
            factorial = sp.factorial(k)
            termino = (valor_derivada / factorial) * (x - x0)**k
            
            self.steps.append(f"\nk = {k}:")
            self.steps.append(f"  f⁽{k}⁾(x) = {derivada_actual}")
            self.steps.append(f"  f⁽{k}⁾({x0}) = {valor_derivada}")
            self.steps.append(f"  Término: [{valor_derivada}]/{k}! · (x-{x0})^{k} = {sp.simplify(termino)}")
            
            polinomio += termino
            
            # Siguiente derivada
            if k < n:
                derivada_actual = sp.diff(derivada_actual, x)
        
        polinomio_simplificado = sp.expand(polinomio)
        
        self.steps.append("\n" + "=" * 70)
        self.steps.append("POLINOMIO RESULTANTE")
        self.steps.append("=" * 70)
        self.steps.append(f"T_{n}(x) = {polinomio_simplificado}")
        
        resultado = None
        if x_eval is not None:
            # Evaluar
            resultado_taylor = float(polinomio.subs(x, x_eval))
            resultado_real = float(f.subs(x, x_eval))
            error = abs(resultado_real - resultado_taylor)
            
            self.steps.append(f"\n" + "-" * 70)
            self.steps.append(f"EVALUACIÓN EN x = {x_eval}")
            self.steps.append("-" * 70)
            self.steps.append(f"T_{n}({x_eval}) = {resultado_taylor:.{self.precision}f}")
            self.steps.append(f"f({x_eval}) = {resultado_real:.{self.precision}f}")
            self.steps.append(f"Error absoluto: {error:.{self.precision}f}")
            
            resultado = resultado_taylor
        
        return polinomio_simplificado, resultado, self.steps
