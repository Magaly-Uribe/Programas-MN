"""
Métodos Numéricos para Derivación
ESCOM - IPN

Incluye:
- Derivación numérica (2, 3 y 5 puntos)
- Extrapolación de Richardson
"""

import numpy as np
import sympy as sp
from typing import List, Tuple, Callable, Optional
import math


class DerivacionNumerica:
    """Clase para métodos de derivación numérica."""
    
    def __init__(self, precision: int = 6):
        self.precision = precision
        self.steps = []
    
    def set_funcion(self, funcion_str: str):
        """Configurar función a derivar."""
        self.funcion_str = funcion_str
        self.x_sym = sp.symbols('x')
        try:
            self.expr = sp.sympify(funcion_str, locals={'e': sp.E})
            self.f_num = sp.lambdify(self.x_sym, self.expr, "math")
            # Derivada analítica
            self.diff_expr = sp.diff(self.expr, self.x_sym)
            self.df_real = sp.lambdify(self.x_sym, self.diff_expr, "math")
        except Exception as e:
            raise ValueError(f"Error al interpretar la función: {e}")
    
    def evaluar(self, x: float) -> float:
        """Evaluar función en un punto."""
        try:
            return self.f_num(x)
        except:
            return 0.0
    
    def derivada_real(self, x: float) -> float:
        """Calcular derivada analítica en un punto."""
        try:
            return self.df_real(x)
        except:
            return 0.0
    
    def derivacion_tabla(self, x0: float, h: float, n: int) -> Tuple[List[dict], List[str]]:
        """
        Genera tabla de derivación con fórmulas de 2, 3 y 5 puntos.
        
        Args:
            x0: Valor inicial
            h: Paso
            n: Número de puntos
            
        Returns:
            resultados: Lista de diccionarios con los valores
            steps: Lista de strings con el procedimiento
        """
        self.steps = []
        self.steps.append("=" * 70)
        self.steps.append("DERIVACIÓN NUMÉRICA (2, 3 y 5 PUNTOS)")
        self.steps.append("=" * 70)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Derivada analítica: f'(x) = {self.diff_expr}")
        self.steps.append(f"x₀ = {x0}, h = {h}, n = {n}")
        
        # Generar datos
        X = [x0 + i * h for i in range(n)]
        Y = [self.evaluar(xi) for xi in X]
        
        self.steps.append("\n" + "-" * 70)
        self.steps.append("TABLA DE VALORES")
        self.steps.append("-" * 70)
        for i, (xi, yi) in enumerate(zip(X, Y)):
            self.steps.append(f"  x_{i} = {xi:.6f}, f(x_{i}) = {yi:.6f}")
        
        self.steps.append("\n" + "-" * 70)
        self.steps.append("FÓRMULAS UTILIZADAS")
        self.steps.append("-" * 70)
        self.steps.append("2 Puntos:")
        self.steps.append("  Adelante: f'(x) ≈ [f(x+h) - f(x)] / h")
        self.steps.append("  Atrás:    f'(x) ≈ [f(x) - f(x-h)] / h")
        self.steps.append("\n3 Puntos:")
        self.steps.append("  Centrada: f'(x) ≈ [f(x+h) - f(x-h)] / 2h")
        self.steps.append("  Adelante: f'(x) ≈ [-3f(x) + 4f(x+h) - f(x+2h)] / 2h")
        self.steps.append("  Atrás:    f'(x) ≈ [3f(x) - 4f(x-h) + f(x-2h)] / 2h")
        self.steps.append("\n5 Puntos:")
        self.steps.append("  Centrada: f'(x) ≈ [-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)] / 12h")
        
        resultados = []
        
        for i in range(n):
            xi = X[i]
            fi = Y[i]
            real_val = self.derivada_real(xi)
            
            # 2 Puntos
            d2 = None
            d2_tipo = ""
            if i < n - 1:
                d2 = (Y[i+1] - Y[i]) / h
                d2_tipo = "Adelante"
            elif i > 0:
                d2 = (Y[i] - Y[i-1]) / h
                d2_tipo = "Atrás"
            
            # 3 Puntos
            d3 = None
            d3_tipo = ""
            if i > 0 and i < n - 1:
                d3 = (Y[i+1] - Y[i-1]) / (2*h)
                d3_tipo = "Centrada"
            elif i <= n - 3:
                d3 = (-3*Y[i] + 4*Y[i+1] - Y[i+2]) / (2*h)
                d3_tipo = "Adelante"
            elif i >= 2:
                d3 = (3*Y[i] - 4*Y[i-1] + Y[i-2]) / (2*h)
                d3_tipo = "Atrás"
            
            # 5 Puntos
            d5 = None
            d5_tipo = ""
            if i >= 2 and i <= n - 3:
                d5 = (-Y[i+2] + 8*Y[i+1] - 8*Y[i-1] + Y[i-2]) / (12*h)
                d5_tipo = "Centrada"
            elif i <= n - 5:
                d5 = (-25*Y[i] + 48*Y[i+1] - 36*Y[i+2] + 16*Y[i+3] - 3*Y[i+4]) / (12*h)
                d5_tipo = "Adelante"
            elif i >= 4:
                d5 = (25*Y[i] - 48*Y[i-1] + 36*Y[i-2] - 16*Y[i-3] + 3*Y[i-4]) / (12*h)
                d5_tipo = "Atrás"
            
            # Error relativo
            val_comp = d5 if d5 is not None else d3
            error = None
            if val_comp is not None and real_val != 0:
                error = abs((real_val - val_comp) / real_val) * 100
            
            resultados.append({
                'i': i,
                'xi': xi,
                'f(xi)': fi,
                'd2': d2,
                'd2_tipo': d2_tipo,
                'd3': d3,
                'd3_tipo': d3_tipo,
                'd5': d5,
                'd5_tipo': d5_tipo,
                'real': real_val,
                'error': error
            })
        
        self.steps.append("\n" + "=" * 70)
        self.steps.append("RESULTADOS")
        self.steps.append("=" * 70)
        
        return resultados, self.steps


class ExtrapolacionRichardson:
    """Extrapolación de Richardson para derivadas."""
    
    def __init__(self, precision: int = 9):
        self.precision = precision
        self.steps = []
    
    def set_funcion(self, funcion_str: str):
        """Configurar función."""
        self.funcion_str = funcion_str
        allowed_funcs = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        self.f = lambda x: eval(funcion_str, {"__builtins__": None}, allowed_funcs | {'x': x})
    
    def calcular(self, x_val: float, h: float, n: int) -> Tuple[np.ndarray, float, List[str]]:
        """
        Calcular derivada usando extrapolación de Richardson.
        
        Args:
            x_val: Punto donde evaluar la derivada
            h: Paso inicial
            n: Número de niveles (filas)
            
        Returns:
            R: Matriz de Richardson
            resultado: Mejor aproximación
            steps: Procedimiento detallado
        """
        self.steps = []
        self.steps.append("=" * 70)
        self.steps.append("EXTRAPOLACIÓN DE RICHARDSON PARA DERIVADAS")
        self.steps.append("=" * 70)
        self.steps.append(f"Función: f(x) = {self.funcion_str}")
        self.steps.append(f"Punto: x = {x_val}")
        self.steps.append(f"Paso inicial: h = {h}")
        self.steps.append(f"Niveles: n = {n}")
        
        self.steps.append("\nFórmula base (Diferencias Centradas):")
        self.steps.append("  D(h) = [f(x+h) - f(x-h)] / 2h")
        self.steps.append("\nFórmula de extrapolación:")
        self.steps.append("  R[i,k] = R[i,k-1] + [R[i,k-1] - R[i-1,k-1]] / (4^k - 1)")
        
        # Inicializar matriz
        R = np.zeros((n, n))
        
        # Columna 0: Diferencias Centradas
        self.steps.append("\n" + "-" * 70)
        self.steps.append("COLUMNA 0: DIFERENCIAS CENTRADAS")
        self.steps.append("-" * 70)
        
        for i in range(n):
            current_h = h / (2**i)
            f_plus = self.f(x_val + current_h)
            f_minus = self.f(x_val - current_h)
            R[i, 0] = (f_plus - f_minus) / (2 * current_h)
            self.steps.append(f"  h_{i} = {current_h:.6f}")
            self.steps.append(f"  R[{i},0] = [f({x_val}+{current_h:.6f}) - f({x_val}-{current_h:.6f})] / {2*current_h:.6f}")
            self.steps.append(f"         = [{f_plus:.6f} - {f_minus:.6f}] / {2*current_h:.6f} = {R[i,0]:.9f}")
        
        # Extrapolación
        self.steps.append("\n" + "-" * 70)
        self.steps.append("EXTRAPOLACIÓN DE RICHARDSON")
        self.steps.append("-" * 70)
        
        for k in range(1, n):
            j = 2 * k
            factor = 1 / (2**j - 1)
            self.steps.append(f"\nColumna {k}: j = {j}, factor = 1/(4^{k} - 1) = {factor:.6f}")
            
            for i in range(k, n):
                N_h2 = R[i, k-1]
                N_h = R[i-1, k-1]
                R[i, k] = N_h2 + factor * (N_h2 - N_h)
                self.steps.append(f"  R[{i},{k}] = {N_h2:.9f} + {factor:.6f}×({N_h2:.9f} - {N_h:.9f})")
                self.steps.append(f"         = {R[i,k]:.9f}")
        
        resultado = R[n-1, n-1]
        
        self.steps.append("\n" + "=" * 70)
        self.steps.append("RESULTADO FINAL")
        self.steps.append("=" * 70)
        self.steps.append(f"f'({x_val}) ≈ {resultado:.12f}")
        
        if n > 1:
            error_est = abs(R[n-1, n-1] - R[n-1, n-2])
            self.steps.append(f"Error estimado: {error_est:.2e}")
        
        return R, resultado, self.steps
