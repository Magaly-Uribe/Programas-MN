"""
Sistemas de EDOs y Conversión de Orden Superior
ESCOM - IPN

Incluye:
- Euler para sistemas
- RK4 para sistemas  
- Conversión de EDO de orden superior a sistema de primer orden
"""

import numpy as np
from typing import Callable, List, Tuple


class ODESystemSolver:
    """Solver para sistemas de EDOs."""
    
    def __init__(self, precision: int = 6):
        self.precision = precision
        self.steps = []
    
    def parse_system(self, equations: List[str], t_var: str, 
                     y_vars: List[str]) -> List[Callable]:
        """Convierte lista de strings a funciones."""
        functions = []
        
        for eq in equations:
            eq = eq.replace('^', '**').replace('sen', 'sin')
            
            def make_f(eq_str):
                def f(t, y_vals):
                    local_vars = {
                        t_var: t,
                        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
                        'pi': np.pi, 'e': np.e
                    }
                    for i, var in enumerate(y_vars):
                        local_vars[var] = y_vals[i]
                    return eval(eq_str, {"__builtins__": {}}, local_vars)
                return f
            
            functions.append(make_f(eq))
        return functions
    
    def system_euler(self, f_list: List[Callable], t0: float, 
                     y0: List[float], t_end: float, h: float) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Método de Euler para sistemas.
        
        Para cada i: w_{i,λ+1} = w_{i,λ} + h·f_i(t_λ, w_λ)
        """
        self.steps = []
        n = len(f_list)
        
        self.steps.append("=" * 60)
        self.steps.append("EULER PARA SISTEMAS DE EDOs")
        self.steps.append("=" * 60)
        self.steps.append(f"Sistema de {n} ecuaciones")
        self.steps.append(f"h = {h}, intervalo [{t0}, {t_end}]")
        
        t_vals = [t0]
        y_vals = [np.array(y0)]
        
        t = t0
        y = np.array(y0, dtype=float)
        step = 0
        
        while t < t_end - 1e-10:
            self.steps.append(f"\n--- Paso {step} (t={t:.4f}) ---")
            
            # Evaluar f_i para cada ecuación
            f_evals = np.array([f_i(t, y) for f_i in f_list])
            
            for i in range(n):
                self.steps.append(f"  f_{i+1} = {f_evals[i]:.6f}")
            
            # Actualizar
            y_new = y + h * f_evals
            
            for i in range(n):
                self.steps.append(f"  w_{i+1} = {y[i]:.6f} + {h}·{f_evals[i]:.6f} = {y_new[i]:.6f}")
            
            t = t + h
            y = y_new
            t_vals.append(t)
            y_vals.append(y.copy())
            step += 1
        
        # Tabla de resultados
        self.steps.append("\n" + "=" * 60)
        self.steps.append("TABLA DE RESULTADOS")
        self.steps.append("=" * 60)
        header = f"{'λ':>4} {'t':>10}"
        for i in range(n):
            header += f" {'w'+str(i+1):>12}"
        self.steps.append(header)
        self.steps.append("-" * (20 + 13*n))
        
        for i, (t, y) in enumerate(zip(t_vals, y_vals)):
            row = f"{i:>4} {t:>10.4f}"
            for yi in y:
                row += f" {yi:>12.6f}"
            self.steps.append(row)
        
        return np.array(t_vals), np.array(y_vals), self.steps
    
    def system_rk4(self, f_list: List[Callable], t0: float,
                   y0: List[float], t_end: float, h: float) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Método RK4 para sistemas (según PDF 47MN).
        
        Para cada i = 1, 2, ..., n:
        K_{i,1} = h·f_i(t_λ, w_λ)
        K_{i,2} = h·f_i(t_λ + h/2, w_λ + K_1/2)
        K_{i,3} = h·f_i(t_λ + h/2, w_λ + K_2/2)
        K_{i,4} = h·f_i(t_λ + h, w_λ + K_3)
        w_{i,λ+1} = w_{i,λ} + (K_{i,1} + 2K_{i,2} + 2K_{i,3} + K_{i,4})/6
        """
        self.steps = []
        n = len(f_list)
        
        self.steps.append("=" * 60)
        self.steps.append("RUNGE-KUTTA 4 PARA SISTEMAS DE EDOs")
        self.steps.append("=" * 60)
        self.steps.append(f"Sistema de {n} ecuaciones")
        self.steps.append(f"h = {h}, intervalo [{t0}, {t_end}]")
        
        t_vals = [t0]
        y_vals = [np.array(y0)]
        
        t = t0
        y = np.array(y0, dtype=float)
        step = 0
        
        while t < t_end - 1e-10:
            self.steps.append(f"\n--- Paso {step} (t={t:.4f}) ---")
            
            # K1
            K1 = np.array([h * f_i(t, y) for f_i in f_list])
            self.steps.append(f"  K₁ = {K1}")
            
            # K2
            y_temp = y + K1/2
            K2 = np.array([h * f_i(t + h/2, y_temp) for f_i in f_list])
            self.steps.append(f"  K₂ = {K2}")
            
            # K3
            y_temp = y + K2/2
            K3 = np.array([h * f_i(t + h/2, y_temp) for f_i in f_list])
            self.steps.append(f"  K₃ = {K3}")
            
            # K4
            y_temp = y + K3
            K4 = np.array([h * f_i(t + h, y_temp) for f_i in f_list])
            self.steps.append(f"  K₄ = {K4}")
            
            # Actualizar
            y_new = y + (K1 + 2*K2 + 2*K3 + K4) / 6
            
            for i in range(n):
                self.steps.append(f"  w_{i+1,new} = {y_new[i]:.6f}")
            
            t = t + h
            y = y_new
            t_vals.append(t)
            y_vals.append(y.copy())
            step += 1
        
        # Tabla de resultados
        self.steps.append("\n" + "=" * 60)
        self.steps.append("TABLA DE RESULTADOS")
        self.steps.append("=" * 60)
        header = f"{'λ':>4} {'t':>10}"
        for i in range(n):
            header += f" {'w'+str(i+1):>12}"
        self.steps.append(header)
        self.steps.append("-" * (20 + 13*n))
        
        for i, (t, y) in enumerate(zip(t_vals, y_vals)):
            row = f"{i:>4} {t:>10.4f}"
            for yi in y:
                row += f" {yi:>12.6f}"
            self.steps.append(row)
        
        return np.array(t_vals), np.array(y_vals), self.steps


class HigherOrderConverter:
    """
    Convierte EDOs de orden superior a sistemas de primer orden.
    
    Según PDF 47MN:
    Para y^(m) = f(t, y, y', ..., y^(m-1))
    
    Se define:
    u_1 = y
    u_2 = y'
    u_3 = y''
    ...
    u_m = y^(m-1)
    
    Sistema resultante:
    u_1' = u_2
    u_2' = u_3
    ...
    u_{m-1}' = u_m
    u_m' = f(t, u_1, u_2, ..., u_m)
    """
    
    def __init__(self):
        self.steps = []
    
    def convert_to_system(self, order: int, f_str: str) -> Tuple[List[str], List[str]]:
        """
        Convierte EDO de orden m a sistema.
        
        Args:
            order: Orden de la EDO (m)
            f_str: Expresión para y^(m) en términos de t, u1, u2, ..., um
        
        Returns:
            equations: Lista de ecuaciones del sistema
            variables: Lista de nombres de variables [u1, u2, ...]
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append(f"CONVERSIÓN EDO ORDEN {order} → SISTEMA")
        self.steps.append("=" * 60)
        
        variables = [f"u{i+1}" for i in range(order)]
        equations = []
        
        self.steps.append("\nTransformación:")
        self.steps.append(f"  u₁ = y")
        for i in range(1, order):
            self.steps.append(f"  u_{i+1} = y^({i})")
        
        self.steps.append("\nSistema resultante:")
        for i in range(order - 1):
            eq = f"u{i+2}"  # u_i' = u_{i+1}
            equations.append(eq)
            self.steps.append(f"  u_{i+1}' = u_{i+2}")
        
        # Última ecuación: u_m' = f(t, u1, ..., um)
        equations.append(f_str)
        self.steps.append(f"  u_{order}' = {f_str}")
        
        return equations, variables
    
    def example_third_order(self):
        """
        Ejemplo del PDF 48MN:
        y''' + 2y'' - y' - 2y = e^(-t)
        
        Despejando: y''' = e^(-t) - 2y'' + y' + 2y
        
        Con u₁=y, u₂=y', u₃=y'':
        u₁' = u₂
        u₂' = u₃
        u₃' = exp(-t) - 2*u3 + u2 + 2*u1
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("EJEMPLO: y''' + 2y'' - y' - 2y = e^(-t)")
        self.steps.append("=" * 60)
        
        self.steps.append("\nDespejando y''':")
        self.steps.append("  y''' = e^(-t) - 2y'' + y' + 2y")
        
        self.steps.append("\nSustitución:")
        self.steps.append("  u₁ = y")
        self.steps.append("  u₂ = y'")
        self.steps.append("  u₃ = y''")
        
        self.steps.append("\nSistema:")
        equations = [
            "u2",
            "u3",
            "exp(-t) - 2*u3 + u2 + 2*u1"
        ]
        
        for i, eq in enumerate(equations):
            self.steps.append(f"  u_{i+1}' = {eq}")
        
        variables = ["u1", "u2", "u3"]
        
        return equations, variables, self.steps
    
    def example_second_order(self):
        """
        Ejemplo del PDF 40MN:
        y'' - 2y' + y = t·e^t - t
        
        Despejando: y'' = t·e^t - t + 2y' - y
        
        Con u₁=y, u₂=y':
        u₁' = u₂
        u₂' = t*exp(t) - t + 2*u2 - u1
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("EJEMPLO: y'' - 2y' + y = t·e^t - t")
        self.steps.append("=" * 60)
        
        self.steps.append("\nDespejando y'':")
        self.steps.append("  y'' = t·e^t - t + 2y' - y")
        
        self.steps.append("\nSustitución:")
        self.steps.append("  u₁ = y")
        self.steps.append("  u₂ = y'")
        
        self.steps.append("\nSistema:")
        equations = [
            "u2",
            "t*exp(t) - t + 2*u2 - u1"
        ]
        
        for i, eq in enumerate(equations):
            self.steps.append(f"  u_{i+1}' = {eq}")
        
        variables = ["u1", "u2"]
        
        return equations, variables, self.steps
