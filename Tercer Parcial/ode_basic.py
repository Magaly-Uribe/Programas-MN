"""
Métodos Numéricos para EDOs - Parte 1
ESCOM - IPN

Incluye: Euler, Taylor, RK2, RK3, RK4
"""

import numpy as np
from typing import Callable, List, Tuple
import sympy as sp
from sympy import symbols, diff, lambdify


class ODEBasicMethods:
    """Métodos básicos para EDOs."""
    
    def __init__(self, precision: int = 6):
        self.precision = precision
        self.steps = []
    
    def parse_equation(self, eq_str: str) -> Callable:
        """Convierte string a función."""
        eq_str = eq_str.replace('^', '**').replace('sen', 'sin')
        
        def f(t, y):
            local_vars = {
                't': t, 'y': y,
                'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
                'pi': np.pi, 'e': np.e, 'abs': np.abs
            }
            return eval(eq_str, {"__builtins__": {}}, local_vars)
        return f
    
    def _add_results_table(self, t_vals, y_vals):
        """Tabla de resultados."""
        self.steps.append("\n" + "=" * 50)
        self.steps.append("TABLA DE RESULTADOS")
        self.steps.append("=" * 50)
        self.steps.append(f"{'λ':>4} {'t_λ':>12} {'w_λ':>15}")
        self.steps.append("-" * 35)
        for i, (t, y) in enumerate(zip(t_vals, y_vals)):
            self.steps.append(f"{i:>4} {t:>12.{self.precision}f} {y:>15.{self.precision}f}")
    
    def euler(self, f: Callable, t0: float, y0: float, 
              t_end: float, h: float) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Método de Euler: w_{λ+1} = w_λ + h·f(t_λ, w_λ)
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("MÉTODO DE EULER")
        self.steps.append("=" * 60)
        self.steps.append(f"Fórmula: w_(λ+1) = w_λ + h·f(t_λ, w_λ)")
        self.steps.append(f"Condiciones: t₀={t0}, y₀={y0}, h={h}")
        
        t_vals, y_vals = [t0], [y0]
        t, y, n = t0, y0, 0
        
        while t < t_end - 1e-10:
            f_val = f(t, y)
            y_new = y + h * f_val
            self.steps.append(f"\nλ={n}: f({t:.4f},{y:.4f})={f_val:.6f}, w={y_new:.6f}")
            t, y = t + h, y_new
            t_vals.append(t)
            y_vals.append(y)
            n += 1
        
        self._add_results_table(t_vals, y_vals)
        return np.array(t_vals), np.array(y_vals), self.steps
    
    def taylor(self, eq_str: str, t0: float, y0: float,
               t_end: float, h: float, order: int = 2) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Método de Taylor orden n.
        w_{λ+1} = w_λ + h·f + (h²/2!)·f' + ... + (hⁿ/n!)·f^(n-1)
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append(f"MÉTODO DE TAYLOR ORDEN {order}")
        self.steps.append("=" * 60)
        
        t_sym, y_sym = symbols('t y')
        eq_parsed = eq_str.replace('^', '**').replace('sen', 'sin')
        f_sym = sp.sympify(eq_parsed)
        
        # Calcular derivadas
        derivs_sym = [f_sym]
        self.steps.append(f"f = {f_sym}")
        for i in range(1, order):
            df_dt = diff(derivs_sym[-1], t_sym)
            df_dy = diff(derivs_sym[-1], y_sym)
            f_next = sp.simplify(df_dt + f_sym * df_dy)
            derivs_sym.append(f_next)
            self.steps.append(f"f^({i}) = {f_next}")
        
        f_funcs = [lambdify((t_sym, y_sym), d, 'numpy') for d in derivs_sym]
        
        t_vals, y_vals = [t0], [y0]
        t, y, n = t0, y0, 0
        
        while t < t_end - 1e-10:
            y_new = y
            for i, func in enumerate(f_funcs):
                coef = (h ** (i + 1)) / np.math.factorial(i + 1)
                y_new += coef * float(func(t, y))
            
            self.steps.append(f"\nλ={n}: t={t:.4f}, w={y_new:.6f}")
            t, y = t + h, y_new
            t_vals.append(t)
            y_vals.append(y)
            n += 1
        
        self._add_results_table(t_vals, y_vals)
        return np.array(t_vals), np.array(y_vals), self.steps
    
    def rk2(self, f: Callable, t0: float, y0: float,
            t_end: float, h: float) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        RK2 (Punto Medio):
        K₁ = f(t, w), K₂ = f(t+h/2, w+(h/2)K₁)
        w_{λ+1} = w_λ + h·K₂
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("RUNGE-KUTTA ORDEN 2 (Punto Medio)")
        self.steps.append("=" * 60)
        self.steps.append("K₁=f(t,w), K₂=f(t+h/2,w+(h/2)K₁), w=w+h·K₂")
        
        t_vals, y_vals = [t0], [y0]
        t, y, n = t0, y0, 0
        
        while t < t_end - 1e-10:
            K1 = f(t, y)
            K2 = f(t + h/2, y + (h/2) * K1)
            y_new = y + h * K2
            self.steps.append(f"\nλ={n}: K₁={K1:.6f}, K₂={K2:.6f}, w={y_new:.6f}")
            t, y = t + h, y_new
            t_vals.append(t)
            y_vals.append(y)
            n += 1
        
        self._add_results_table(t_vals, y_vals)
        return np.array(t_vals), np.array(y_vals), self.steps
    
    def rk3(self, f: Callable, t0: float, y0: float,
            t_end: float, h: float) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        RK3:
        k₁ = h·f(t,y), k₂ = h·f(t+h/2,y+k₁/2), k₃ = h·f(t+h,y-k₁+2k₂)
        w_{λ+1} = w_λ + (k₁+4k₂+k₃)/6
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("RUNGE-KUTTA ORDEN 3")
        self.steps.append("=" * 60)
        
        t_vals, y_vals = [t0], [y0]
        t, y, n = t0, y0, 0
        
        while t < t_end - 1e-10:
            k1 = h * f(t, y)
            k2 = h * f(t + h/2, y + k1/2)
            k3 = h * f(t + h, y - k1 + 2*k2)
            y_new = y + (k1 + 4*k2 + k3) / 6
            self.steps.append(f"\nλ={n}: k₁={k1:.6f}, k₂={k2:.6f}, k₃={k3:.6f}, w={y_new:.6f}")
            t, y = t + h, y_new
            t_vals.append(t)
            y_vals.append(y)
            n += 1
        
        self._add_results_table(t_vals, y_vals)
        return np.array(t_vals), np.array(y_vals), self.steps
    
    def rk4(self, f: Callable, t0: float, y0: float,
            t_end: float, h: float) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        RK4 Clásico:
        K₁ = f(t,w), K₂ = f(t+h/2,w+(h/2)K₁)
        K₃ = f(t+h/2,w+(h/2)K₂), K₄ = f(t+h,w+hK₃)
        w_{λ+1} = w_λ + (h/6)(K₁+2K₂+2K₃+K₄)
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("RUNGE-KUTTA ORDEN 4 (Clásico)")
        self.steps.append("=" * 60)
        self.steps.append("Φ = (K₁+2K₂+2K₃+K₄)/6, w = w + h·Φ")
        
        t_vals, y_vals = [t0], [y0]
        t, y, n = t0, y0, 0
        
        while t < t_end - 1e-10:
            K1 = f(t, y)
            K2 = f(t + h/2, y + (h/2) * K1)
            K3 = f(t + h/2, y + (h/2) * K2)
            K4 = f(t + h, y + h * K3)
            phi = (K1 + 2*K2 + 2*K3 + K4) / 6
            y_new = y + h * phi
            
            self.steps.append(f"\nλ={n}: K₁={K1:.6f}, K₂={K2:.6f}, K₃={K3:.6f}, K₄={K4:.6f}")
            self.steps.append(f"  Φ={phi:.6f}, w={y_new:.6f}")
            
            t, y = t + h, y_new
            t_vals.append(t)
            y_vals.append(y)
            n += 1
        
        self._add_results_table(t_vals, y_vals)
        return np.array(t_vals), np.array(y_vals), self.steps
