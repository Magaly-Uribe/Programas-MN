"""
Métodos Numéricos para Integración
ESCOM - IPN

Incluye:
- Regla del Trapecio (Simple y Compuesta)
- Regla de Simpson 1/3 (Simple y Compuesta)
- Regla de Simpson 3/8 (Simple y Compuesta)
- Integración de Romberg
- Cuadratura Gaussiana
- Cuadratura Adaptativa
- Integración Múltiple (Doble)
"""

import numpy as np
import sympy as sp
from typing import List, Tuple, Callable, Optional
import math


class IntegracionNumerica:
    """Clase para métodos de integración numérica."""
    
    def __init__(self, precision: int = 6):
        self.precision = precision
        self.steps = []
        self.x_sym = sp.symbols('x')
        self.funcion_str = ""
        self.expr = None
        self.f_num = None
    
    def set_funcion(self, funcion_str: str):
        """Configurar función a integrar."""
        self.funcion_str = funcion_str
        try:
            self.expr = sp.sympify(funcion_str, locals={'e': sp.E})
            self.f_num = sp.lambdify(self.x_sym, self.expr, "math")
        except Exception as e:
            raise ValueError(f"Error al interpretar la función: {e}")
    
    def evaluar(self, x: float) -> float:
        """Evaluar función en un punto."""
        try:
            return self.f_num(x)
        except:
            return 0.0
    
    def valor_exacto(self, a: float, b: float) -> Optional[float]:
        """Calcular integral exacta usando SymPy."""
        try:
            integral = sp.integrate(self.expr, (self.x_sym, a, b))
            return float(integral)
        except:
            return None
    
    def trapecio_simple(self, a: float, b: float) -> Tuple[float, List[str]]:
        """
        Regla del Trapecio Simple.
        I ≈ (h/2)[f(a) + f(b)]
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("REGLA DEL TRAPECIO SIMPLE")
        self.steps.append("=" * 60)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Intervalo: [{a}, {b}]")
        
        h = b - a
        fa = self.evaluar(a)
        fb = self.evaluar(b)
        
        self.steps.append(f"\nh = b - a = {b} - {a} = {h}")
        self.steps.append(f"f(a) = f({a}) = {fa:.{self.precision}f}")
        self.steps.append(f"f(b) = f({b}) = {fb:.{self.precision}f}")
        
        resultado = (h / 2) * (fa + fb)
        
        self.steps.append(f"\nI ≈ (h/2)[f(a) + f(b)]")
        self.steps.append(f"I ≈ ({h}/2)[{fa:.{self.precision}f} + {fb:.{self.precision}f}]")
        self.steps.append(f"I ≈ {resultado:.{self.precision}f}")
        
        # Valor exacto
        exacto = self.valor_exacto(a, b)
        if exacto is not None:
            error = abs(exacto - resultado)
            error_rel = (error / abs(exacto)) * 100 if exacto != 0 else 0
            self.steps.append(f"\nValor exacto: {exacto:.{self.precision}f}")
            self.steps.append(f"Error absoluto: {error:.{self.precision}f}")
            self.steps.append(f"Error relativo: {error_rel:.4f}%")
        
        return resultado, self.steps
    
    def trapecio_compuesto(self, a: float, b: float, n: int) -> Tuple[float, List[str]]:
        """
        Regla del Trapecio Compuesta.
        I ≈ (h/2)[f(x₀) + 2Σf(xᵢ) + f(xₙ)]
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("REGLA DEL TRAPECIO COMPUESTA")
        self.steps.append("=" * 60)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Intervalo: [{a}, {b}], n = {n}")
        
        h = (b - a) / n
        self.steps.append(f"\nh = (b-a)/n = ({b}-{a})/{n} = {h}")
        
        self.steps.append(f"\n{'i':<5} {'xᵢ':<12} {'f(xᵢ)':<15} {'Coef.':<8} {'Término':<15}")
        self.steps.append("-" * 60)
        
        suma_interna = 0
        f_x0 = self.evaluar(a)
        f_xn = self.evaluar(b)
        
        self.steps.append(f"{0:<5} {a:<12.{self.precision}f} {f_x0:<15.{self.precision}f} {'1':<8} {f_x0:<15.{self.precision}f}")
        
        for i in range(1, n):
            xi = a + i * h
            fxi = self.evaluar(xi)
            suma_interna += fxi
            self.steps.append(f"{i:<5} {xi:<12.{self.precision}f} {fxi:<15.{self.precision}f} {'2':<8} {2*fxi:<15.{self.precision}f}")
        
        self.steps.append(f"{n:<5} {b:<12.{self.precision}f} {f_xn:<15.{self.precision}f} {'1':<8} {f_xn:<15.{self.precision}f}")
        
        resultado = (h / 2) * (f_x0 + 2 * suma_interna + f_xn)
        
        self.steps.append("-" * 60)
        self.steps.append(f"\nI ≈ (h/2)[f(x₀) + 2·Σf(xᵢ) + f(xₙ)]")
        self.steps.append(f"I ≈ ({h}/2)[{f_x0:.{self.precision}f} + 2·{suma_interna:.{self.precision}f} + {f_xn:.{self.precision}f}]")
        self.steps.append(f"I ≈ {resultado:.{self.precision}f}")
        
        # Valor exacto
        exacto = self.valor_exacto(a, b)
        if exacto is not None:
            error = abs(exacto - resultado)
            error_rel = (error / abs(exacto)) * 100 if exacto != 0 else 0
            self.steps.append(f"\nValor exacto: {exacto:.{self.precision}f}")
            self.steps.append(f"Error absoluto: {error:.{self.precision}f}")
            self.steps.append(f"Error relativo: {error_rel:.4f}%")
        
        return resultado, self.steps
    
    def simpson_1_3_simple(self, a: float, b: float) -> Tuple[float, List[str]]:
        """
        Regla de Simpson 1/3 Simple.
        I ≈ (h/3)[f(a) + 4f(m) + f(b)]
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("REGLA DE SIMPSON 1/3 SIMPLE")
        self.steps.append("=" * 60)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Intervalo: [{a}, {b}]")
        
        h = (b - a) / 2
        m = (a + b) / 2
        
        fa = self.evaluar(a)
        fm = self.evaluar(m)
        fb = self.evaluar(b)
        
        self.steps.append(f"\nh = (b-a)/2 = {h}")
        self.steps.append(f"m = (a+b)/2 = {m}")
        self.steps.append(f"\nf(a) = f({a}) = {fa:.{self.precision}f}")
        self.steps.append(f"f(m) = f({m}) = {fm:.{self.precision}f}")
        self.steps.append(f"f(b) = f({b}) = {fb:.{self.precision}f}")
        
        resultado = (h / 3) * (fa + 4*fm + fb)
        
        self.steps.append(f"\nI ≈ (h/3)[f(a) + 4f(m) + f(b)]")
        self.steps.append(f"I ≈ ({h}/3)[{fa:.{self.precision}f} + 4·{fm:.{self.precision}f} + {fb:.{self.precision}f}]")
        self.steps.append(f"I ≈ {resultado:.{self.precision}f}")
        
        # Valor exacto
        exacto = self.valor_exacto(a, b)
        if exacto is not None:
            error = abs(exacto - resultado)
            error_rel = (error / abs(exacto)) * 100 if exacto != 0 else 0
            self.steps.append(f"\nValor exacto: {exacto:.{self.precision}f}")
            self.steps.append(f"Error absoluto: {error:.{self.precision}f}")
            self.steps.append(f"Error relativo: {error_rel:.4f}%")
        
        return resultado, self.steps
    
    def simpson_1_3_compuesto(self, a: float, b: float, n: int) -> Tuple[float, List[str]]:
        """
        Regla de Simpson 1/3 Compuesta.
        n debe ser par.
        """
        if n % 2 != 0:
            n += 1
        
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("REGLA DE SIMPSON 1/3 COMPUESTA")
        self.steps.append("=" * 60)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Intervalo: [{a}, {b}], n = {n}")
        
        h = (b - a) / n
        self.steps.append(f"\nh = (b-a)/n = {h}")
        
        self.steps.append(f"\n{'i':<5} {'xᵢ':<12} {'f(xᵢ)':<15} {'Coef.':<8} {'Término':<15}")
        self.steps.append("-" * 60)
        
        suma = 0
        for i in range(n + 1):
            xi = a + i * h
            fxi = self.evaluar(xi)
            
            if i == 0 or i == n:
                coef = 1
            elif i % 2 != 0:
                coef = 4
            else:
                coef = 2
            
            termino = coef * fxi
            suma += termino
            self.steps.append(f"{i:<5} {xi:<12.{self.precision}f} {fxi:<15.{self.precision}f} {coef:<8} {termino:<15.{self.precision}f}")
        
        resultado = (h / 3) * suma
        
        self.steps.append("-" * 60)
        self.steps.append(f"\nI ≈ (h/3)·Σ")
        self.steps.append(f"I ≈ ({h}/3)·{suma:.{self.precision}f}")
        self.steps.append(f"I ≈ {resultado:.{self.precision}f}")
        
        # Valor exacto
        exacto = self.valor_exacto(a, b)
        if exacto is not None:
            error = abs(exacto - resultado)
            error_rel = (error / abs(exacto)) * 100 if exacto != 0 else 0
            self.steps.append(f"\nValor exacto: {exacto:.{self.precision}f}")
            self.steps.append(f"Error absoluto: {error:.{self.precision}f}")
            self.steps.append(f"Error relativo: {error_rel:.4f}%")
        
        return resultado, self.steps
    
    def simpson_3_8_simple(self, a: float, b: float) -> Tuple[float, List[str]]:
        """
        Regla de Simpson 3/8 Simple.
        I ≈ (3h/8)[f(x₀) + 3f(x₁) + 3f(x₂) + f(x₃)]
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("REGLA DE SIMPSON 3/8 SIMPLE")
        self.steps.append("=" * 60)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Intervalo: [{a}, {b}]")
        
        h = (b - a) / 3
        coefs = [1, 3, 3, 1]
        
        self.steps.append(f"\nh = (b-a)/3 = {h}")
        self.steps.append(f"\n{'i':<5} {'xᵢ':<12} {'f(xᵢ)':<15} {'Coef.':<8} {'Término':<15}")
        self.steps.append("-" * 60)
        
        suma = 0
        for i in range(4):
            xi = a + i * h
            fxi = self.evaluar(xi)
            termino = coefs[i] * fxi
            suma += termino
            self.steps.append(f"{i:<5} {xi:<12.{self.precision}f} {fxi:<15.{self.precision}f} {coefs[i]:<8} {termino:<15.{self.precision}f}")
        
        resultado = (3 * h / 8) * suma
        
        self.steps.append("-" * 60)
        self.steps.append(f"\nI ≈ (3h/8)·Σ")
        self.steps.append(f"I ≈ (3·{h}/8)·{suma:.{self.precision}f}")
        self.steps.append(f"I ≈ {resultado:.{self.precision}f}")
        
        # Valor exacto
        exacto = self.valor_exacto(a, b)
        if exacto is not None:
            error = abs(exacto - resultado)
            error_rel = (error / abs(exacto)) * 100 if exacto != 0 else 0
            self.steps.append(f"\nValor exacto: {exacto:.{self.precision}f}")
            self.steps.append(f"Error absoluto: {error:.{self.precision}f}")
            self.steps.append(f"Error relativo: {error_rel:.4f}%")
        
        return resultado, self.steps
    
    def simpson_3_8_compuesto(self, a: float, b: float, n: int) -> Tuple[float, List[str]]:
        """
        Regla de Simpson 3/8 Compuesta.
        n debe ser múltiplo de 3.
        """
        if n % 3 != 0:
            n = ((n // 3) + 1) * 3
        
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("REGLA DE SIMPSON 3/8 COMPUESTA")
        self.steps.append("=" * 60)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Intervalo: [{a}, {b}], n = {n}")
        
        h = (b - a) / n
        self.steps.append(f"\nh = (b-a)/n = {h}")
        
        self.steps.append(f"\n{'i':<5} {'xᵢ':<12} {'f(xᵢ)':<15} {'Coef.':<8} {'Término':<15}")
        self.steps.append("-" * 60)
        
        suma = 0
        for i in range(n + 1):
            xi = a + i * h
            fxi = self.evaluar(xi)
            
            if i == 0 or i == n:
                coef = 1
            elif i % 3 == 0:
                coef = 2
            else:
                coef = 3
            
            termino = coef * fxi
            suma += termino
            self.steps.append(f"{i:<5} {xi:<12.{self.precision}f} {fxi:<15.{self.precision}f} {coef:<8} {termino:<15.{self.precision}f}")
        
        resultado = (3 * h / 8) * suma
        
        self.steps.append("-" * 60)
        self.steps.append(f"\nI ≈ (3h/8)·Σ")
        self.steps.append(f"I ≈ (3·{h}/8)·{suma:.{self.precision}f}")
        self.steps.append(f"I ≈ {resultado:.{self.precision}f}")
        
        # Valor exacto
        exacto = self.valor_exacto(a, b)
        if exacto is not None:
            error = abs(exacto - resultado)
            error_rel = (error / abs(exacto)) * 100 if exacto != 0 else 0
            self.steps.append(f"\nValor exacto: {exacto:.{self.precision}f}")
            self.steps.append(f"Error absoluto: {error:.{self.precision}f}")
            self.steps.append(f"Error relativo: {error_rel:.4f}%")
        
        return resultado, self.steps


class IntegracionRomberg:
    """Integración de Romberg."""
    
    def __init__(self, precision: int = 10):
        self.precision = precision
        self.steps = []
    
    def set_funcion(self, funcion_str: str):
        """Configurar función."""
        self.funcion_str = funcion_str
        self.x_sym = sp.symbols('x')
        self.expr = sp.sympify(funcion_str, locals={'e': sp.E})
        self.f_num = sp.lambdify(self.x_sym, self.expr, "math")
    
    def evaluar(self, x: float) -> float:
        try:
            return self.f_num(x)
        except:
            return 0.0
    
    def calcular(self, a: float, b: float, n: int) -> Tuple[np.ndarray, float, List[str]]:
        """
        Integración de Romberg.
        
        Args:
            a, b: Límites de integración
            n: Número de niveles
            
        Returns:
            R: Matriz de Romberg
            resultado: Mejor aproximación
            steps: Procedimiento
        """
        self.steps = []
        self.steps.append("=" * 70)
        self.steps.append("INTEGRACIÓN DE ROMBERG")
        self.steps.append("=" * 70)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Intervalo: [{a}, {b}]")
        self.steps.append(f"Niveles: n = {n}")
        
        # Valor exacto
        try:
            exacto = float(sp.integrate(self.expr, (self.x_sym, a, b)))
            self.steps.append(f"Valor exacto (analítico): {exacto:.{self.precision}f}")
        except:
            exacto = None
            self.steps.append("No se pudo calcular el valor exacto analíticamente")
        
        R = np.zeros((n, n))
        
        # Primera columna: Trapecio
        self.steps.append("\n" + "-" * 70)
        self.steps.append("COLUMNA 0: REGLA DEL TRAPECIO")
        self.steps.append("-" * 70)
        
        for i in range(n):
            pasos = 2**i
            h = (b - a) / pasos
            
            suma = self.evaluar(a) + self.evaluar(b)
            for k in range(1, pasos):
                suma += 2 * self.evaluar(a + k * h)
            
            R[i, 0] = (h / 2) * suma
            self.steps.append(f"  n={pasos:>3}, h={h:.6f} → R[{i},0] = {R[i,0]:.{self.precision}f}")
        
        # Extrapolación
        self.steps.append("\n" + "-" * 70)
        self.steps.append("EXTRAPOLACIÓN DE RICHARDSON")
        self.steps.append("-" * 70)
        self.steps.append("R[i,j] = R[i,j-1] + [R[i,j-1] - R[i-1,j-1]] / (4^j - 1)")
        
        for j in range(1, n):
            for i in range(j, n):
                numerador = R[i, j-1] - R[i-1, j-1]
                denominador = 4**j - 1
                R[i, j] = R[i, j-1] + (numerador / denominador)
            self.steps.append(f"  Columna {j}: R[{j}:{n-1},{j}] calculado")
        
        resultado = R[n-1, n-1]
        
        self.steps.append("\n" + "=" * 70)
        self.steps.append("TABLA DE ROMBERG")
        self.steps.append("=" * 70)
        
        # Mostrar tabla
        header = f"{'n':<6}"
        for j in range(n):
            header += f"{'R[·,'+str(j)+']':<15}"
        self.steps.append(header)
        self.steps.append("-" * (6 + 15*n))
        
        for i in range(n):
            row = f"{2**i:<6}"
            for j in range(i + 1):
                row += f"{R[i,j]:<15.{self.precision}f}"
            self.steps.append(row)
        
        self.steps.append("\n" + "=" * 70)
        self.steps.append("RESULTADO FINAL")
        self.steps.append("=" * 70)
        self.steps.append(f"Aproximación: {resultado:.{self.precision}f}")
        
        if exacto is not None:
            error_abs = abs(exacto - resultado)
            error_rel = (error_abs / abs(exacto)) * 100 if exacto != 0 else 0
            self.steps.append(f"Error absoluto: {error_abs:.2e}")
            self.steps.append(f"Error relativo: {error_rel:.{self.precision}f}%")
        
        return R, resultado, self.steps


class CuadraturaGaussiana:
    """Cuadratura Gaussiana con polinomios de Legendre."""
    
    # Coeficientes de Gauss-Legendre
    COEFICIENTES = {
        2: {
            'nodos': [-0.5773502692, 0.5773502692],
            'pesos': [1.0, 1.0]
        },
        3: {
            'nodos': [-0.7745966692, 0.0, 0.7745966692],
            'pesos': [0.5555555556, 0.8888888889, 0.5555555556]
        },
        4: {
            'nodos': [-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116],
            'pesos': [0.3478548451, 0.6521451549, 0.6521451549, 0.3478548451]
        },
        5: {
            'nodos': [-0.9061798459, -0.5384693101, 0.0, 0.5384693101, 0.9061798459],
            'pesos': [0.2369268851, 0.4786286705, 0.5688888889, 0.4786286705, 0.2369268851]
        }
    }
    
    def __init__(self, precision: int = 10):
        self.precision = precision
        self.steps = []
    
    def set_funcion(self, funcion_str: str):
        """Configurar función."""
        self.funcion_str = funcion_str
        x = sp.symbols('x')
        self.expr = sp.sympify(funcion_str, locals={'e': sp.E})
        self.f_num = sp.lambdify(x, self.expr, "math")
    
    def evaluar(self, x: float) -> float:
        try:
            return self.f_num(x)
        except:
            return 0.0
    
    def transformar_punto(self, t: float, a: float, b: float) -> float:
        """Transformar de [-1,1] a [a,b]."""
        return ((b - a) * t + (a + b)) / 2
    
    def calcular(self, a: float, b: float, n_intervalos: int, grado: int) -> Tuple[float, List[str]]:
        """
        Cuadratura Gaussiana compuesta.
        
        Args:
            a, b: Límites de integración
            n_intervalos: Número de subintervalos
            grado: Grado del polinomio de Legendre (2, 3, 4 o 5)
        """
        self.steps = []
        self.steps.append("=" * 70)
        self.steps.append("CUADRATURA GAUSSIANA (GAUSS-LEGENDRE)")
        self.steps.append("=" * 70)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Intervalo: [{a}, {b}]")
        self.steps.append(f"Subintervalos: {n_intervalos}")
        self.steps.append(f"Grado: {grado} (exacto para polinomios hasta grado {2*grado-1})")
        
        if grado not in self.COEFICIENTES:
            raise ValueError(f"Grado {grado} no soportado. Use 2, 3, 4 o 5.")
        
        coef = self.COEFICIENTES[grado]
        nodos = coef['nodos']
        pesos = coef['pesos']
        
        self.steps.append("\nPuntos y pesos de Gauss-Legendre:")
        for i in range(grado):
            self.steps.append(f"  ξ_{i+1} = {nodos[i]:.{self.precision}f}, w_{i+1} = {pesos[i]:.{self.precision}f}")
        
        h = (b - a) / n_intervalos
        resultado_total = 0.0
        
        self.steps.append(f"\nh = (b-a)/n = {h}")
        self.steps.append("\n" + "-" * 70)
        self.steps.append("CÁLCULO POR SUBINTERVALOS")
        self.steps.append("-" * 70)
        
        for i in range(n_intervalos):
            ai = a + i * h
            bi = ai + h
            
            integral_intervalo = 0.0
            self.steps.append(f"\nSubintervalo {i+1}: [{ai:.4f}, {bi:.4f}]")
            
            for j in range(grado):
                x_trans = self.transformar_punto(nodos[j], ai, bi)
                fx = self.evaluar(x_trans)
                contrib = pesos[j] * fx
                integral_intervalo += contrib
                self.steps.append(f"  x = {x_trans:.6f}, f(x) = {fx:.6f}, w·f = {contrib:.6f}")
            
            integral_intervalo *= (bi - ai) / 2
            resultado_total += integral_intervalo
            self.steps.append(f"  Integral parcial: {integral_intervalo:.{self.precision}f}")
        
        self.steps.append("\n" + "=" * 70)
        self.steps.append("RESULTADO FINAL")
        self.steps.append("=" * 70)
        self.steps.append(f"Integral ≈ {resultado_total:.{self.precision}f}")
        
        return resultado_total, self.steps


class CuadraturaAdaptativa:
    """Cuadratura Adaptativa usando Simpson."""
    
    def __init__(self, precision: int = 10):
        self.precision = precision
        self.steps = []
        self.niveles_usados = 0
    
    def set_funcion(self, funcion_str: str):
        """Configurar función."""
        self.funcion_str = funcion_str
        x = sp.symbols('x')
        self.expr = sp.sympify(funcion_str, locals={'e': sp.E})
        self.f_num = sp.lambdify(x, self.expr, "math")
    
    def evaluar(self, x: float) -> float:
        try:
            return self.f_num(x)
        except:
            return 0.0
    
    def simpson_simple(self, a: float, b: float) -> float:
        """Simpson simple."""
        h = (b - a) / 2
        return (h / 3) * (self.evaluar(a) + 4*self.evaluar(a + h) + self.evaluar(b))
    
    def _adaptativo_rec(self, a: float, b: float, tol: float, nivel: int, max_nivel: int) -> float:
        """Recursión adaptativa."""
        if nivel > max_nivel:
            return self.simpson_simple(a, b)
        
        self.niveles_usados = max(self.niveles_usados, nivel)
        
        I1 = self.simpson_simple(a, b)
        m = (a + b) / 2
        I2 = self.simpson_simple(a, m) + self.simpson_simple(m, b)
        
        error_est = abs(I2 - I1) / 15
        
        if error_est <= tol:
            return I2 + (I2 - I1) / 15  # Corrección de Richardson
        else:
            return (self._adaptativo_rec(a, m, tol/2, nivel+1, max_nivel) +
                    self._adaptativo_rec(m, b, tol/2, nivel+1, max_nivel))
    
    def calcular(self, a: float, b: float, tol: float, max_nivel: int = 20) -> Tuple[float, int, List[str]]:
        """
        Cuadratura adaptativa.
        
        Returns:
            resultado: Valor de la integral
            niveles: Máximo nivel de recursión alcanzado
            steps: Procedimiento
        """
        self.steps = []
        self.steps.append("=" * 70)
        self.steps.append("CUADRATURA ADAPTATIVA (SIMPSON)")
        self.steps.append("=" * 70)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Intervalo: [{a}, {b}]")
        self.steps.append(f"Tolerancia: {tol}")
        self.steps.append(f"Nivel máximo: {max_nivel}")
        
        self.steps.append("\nMétodo: División recursiva hasta alcanzar tolerancia")
        self.steps.append("Criterio: |I₂ - I₁|/15 ≤ ε")
        
        self.niveles_usados = 0
        resultado = self._adaptativo_rec(a, b, tol, 0, max_nivel)
        
        self.steps.append("\n" + "=" * 70)
        self.steps.append("RESULTADO")
        self.steps.append("=" * 70)
        self.steps.append(f"Integral ≈ {resultado:.{self.precision}f}")
        self.steps.append(f"Niveles de recursión usados: {self.niveles_usados}")
        
        return resultado, self.niveles_usados, self.steps


class IntegracionDoble:
    """Integración doble (múltiple)."""
    
    def __init__(self, precision: int = 6):
        self.precision = precision
        self.steps = []
    
    def set_funcion(self, funcion_str: str):
        """Configurar función de dos variables."""
        self.funcion_str = funcion_str
        self.x_sym, self.y_sym = sp.symbols('x y')
        self.expr = sp.sympify(funcion_str, locals={'e': sp.E})
        self.f_num = sp.lambdify((self.x_sym, self.y_sym), self.expr, "math")
    
    def evaluar(self, x: float, y: float) -> float:
        try:
            return self.f_num(x, y)
        except:
            return 0.0
    
    def trapecio_doble(self, x0: float, xn: float, y0: float, yn: float, 
                       n: int, m: int) -> Tuple[float, List[str]]:
        """Trapecio compuesto doble."""
        self.steps = []
        self.steps.append("=" * 70)
        self.steps.append("INTEGRACIÓN DOBLE - TRAPECIO")
        self.steps.append("=" * 70)
        self.steps.append(f"Función: f(x,y) = {self.funcion_str}")
        self.steps.append(f"x ∈ [{x0}, {xn}], y ∈ [{y0}, {yn}]")
        self.steps.append(f"n = {n}, m = {m}")
        
        hx = (xn - x0) / n
        hy = (yn - y0) / m
        
        self.steps.append(f"\nhx = {hx}, hy = {hy}")
        
        suma_total = 0
        for i in range(n + 1):
            for j in range(m + 1):
                xi = x0 + i * hx
                yj = y0 + j * hy
                val = self.evaluar(xi, yj)
                
                es_borde_x = (i == 0 or i == n)
                es_borde_y = (j == 0 or j == m)
                
                if es_borde_x and es_borde_y:
                    peso = 1
                elif not es_borde_x and not es_borde_y:
                    peso = 4
                else:
                    peso = 2
                
                suma_total += peso * val
        
        resultado = (hx * hy / 4) * suma_total
        
        self.steps.append(f"\nResultado: {resultado:.{self.precision}f}")
        
        # Valor exacto
        try:
            exacto = float(sp.integrate(self.expr, (self.x_sym, x0, xn), (self.y_sym, y0, yn)))
            error = abs(exacto - resultado)
            self.steps.append(f"Valor exacto: {exacto:.{self.precision}f}")
            self.steps.append(f"Error: {error:.{self.precision}f}")
        except:
            pass
        
        return resultado, self.steps
    
    def simpson_doble(self, x0: float, xn: float, y0: float, yn: float,
                      n: int, m: int) -> Tuple[float, List[str]]:
        """Simpson 1/3 compuesto doble."""
        if n % 2 != 0:
            n += 1
        if m % 2 != 0:
            m += 1
        
        self.steps = []
        self.steps.append("=" * 70)
        self.steps.append("INTEGRACIÓN DOBLE - SIMPSON 1/3")
        self.steps.append("=" * 70)
        self.steps.append(f"Función: f(x,y) = {self.funcion_str}")
        self.steps.append(f"x ∈ [{x0}, {xn}], y ∈ [{y0}, {yn}]")
        self.steps.append(f"n = {n}, m = {m}")
        
        hx = (xn - x0) / n
        hy = (yn - y0) / m
        
        self.steps.append(f"\nhx = {hx}, hy = {hy}")
        
        suma_total = 0
        for i in range(n + 1):
            for j in range(m + 1):
                xi = x0 + i * hx
                yj = y0 + j * hy
                val = self.evaluar(xi, yj)
                
                # Peso en X
                if i == 0 or i == n:
                    wx = 1
                elif i % 2 != 0:
                    wx = 4
                else:
                    wx = 2
                
                # Peso en Y
                if j == 0 or j == m:
                    wy = 1
                elif j % 2 != 0:
                    wy = 4
                else:
                    wy = 2
                
                peso = wx * wy
                suma_total += peso * val
        
        resultado = (hx * hy / 9) * suma_total
        
        self.steps.append(f"\nResultado: {resultado:.{self.precision}f}")
        
        # Valor exacto
        try:
            exacto = float(sp.integrate(self.expr, (self.x_sym, x0, xn), (self.y_sym, y0, yn)))
            error = abs(exacto - resultado)
            self.steps.append(f"Valor exacto: {exacto:.{self.precision}f}")
            self.steps.append(f"Error: {error:.{self.precision}f}")
        except:
            pass
        
        return resultado, self.steps
