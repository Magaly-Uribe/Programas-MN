"""
Métodos Numéricos para EDOs - Parte 2
ESCOM - IPN

Incluye: RKF45 (adaptativo), Adams-Bashforth
"""

import numpy as np
from typing import Callable, List, Tuple


class ODEAdvancedMethods:
    """Métodos avanzados para EDOs."""
    
    def __init__(self, precision: int = 6):
        self.precision = precision
        self.steps = []
    
    def _add_results_table(self, t_vals, y_vals):
        """Tabla de resultados."""
        self.steps.append("\n" + "=" * 50)
        self.steps.append("TABLA DE RESULTADOS")
        self.steps.append("=" * 50)
        self.steps.append(f"{'λ':>4} {'t_λ':>12} {'w_λ':>15}")
        self.steps.append("-" * 35)
        for i, (t, y) in enumerate(zip(t_vals, y_vals)):
            self.steps.append(f"{i:>4} {t:>12.{self.precision}f} {y:>15.{self.precision}f}")
    
    def rkf45(self, f: Callable, t0: float, y0: float, t_end: float, 
              h: float, tol: float = 1e-6) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Runge-Kutta-Fehlberg 4-5 (Adaptativo).
        
        Fórmulas según PDF 45MN, 46MN:
        K₁ = h·f(t, w)
        K₂ = h·f(t + h/4, w + K₁/4)
        K₃ = h·f(t + 3h/8, w + 3K₁/32 + 9K₂/32)
        K₄ = h·f(t + 12h/13, w + 1932K₁/2197 - 7200K₂/2197 + 7296K₃/2197)
        K₅ = h·f(t + h, w + 439K₁/216 - 8K₂ + 3680K₃/513 - 845K₄/4104)
        K₆ = h·f(t + h/2, w - 8K₁/27 + 2K₂ - 3544K₃/2565 + 1859K₄/4104 - 11K₅/40)
        
        w⁽⁴⁾ = w + 25K₁/216 + 1408K₃/2565 + 2197K₄/4104 - K₅/5
        w̃⁽⁵⁾ = w + 16K₁/135 + 6656K₃/12825 + 28561K₄/56430 - 9K₅/50 + 2K₆/55
        
        R = |w̃ - w|/h, q = 0.84·(ε/R)^(1/4)
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("RUNGE-KUTTA-FEHLBERG 4-5 (Adaptativo)")
        self.steps.append("=" * 60)
        self.steps.append("Control de error: R = |w̃⁽⁵⁾ - w⁽⁴⁾|/h ≤ ε")
        self.steps.append("Ajuste de paso: q = 0.84·(ε/R)^(1/4)")
        self.steps.append(f"\nCondiciones: t₀={t0}, y₀={y0}, h={h}, tol={tol}")
        
        t_vals, y_vals = [t0], [y0]
        t, y = t0, y0
        step = 0
        h_min, h_max = 1e-8, 1.0
        
        while t < t_end - 1e-10:
            if t + h > t_end:
                h = t_end - t
            
            self.steps.append(f"\n{'─'*50}")
            self.steps.append(f"Paso {step+1}: t={t:.6f}, h={h:.6f}")
            
            # Calcular K's
            K1 = h * f(t, y)
            K2 = h * f(t + h/4, y + K1/4)
            K3 = h * f(t + 3*h/8, y + 3*K1/32 + 9*K2/32)
            K4 = h * f(t + 12*h/13, y + 1932*K1/2197 - 7200*K2/2197 + 7296*K3/2197)
            K5 = h * f(t + h, y + 439*K1/216 - 8*K2 + 3680*K3/513 - 845*K4/4104)
            K6 = h * f(t + h/2, y - 8*K1/27 + 2*K2 - 3544*K3/2565 + 1859*K4/4104 - 11*K5/40)
            
            self.steps.append(f"  K₁={K1:.6f}, K₂={K2:.6f}, K₃={K3:.6f}")
            self.steps.append(f"  K₄={K4:.6f}, K₅={K5:.6f}, K₆={K6:.6f}")
            
            # Aproximaciones orden 4 y 5
            w4 = y + 25*K1/216 + 1408*K3/2565 + 2197*K4/4104 - K5/5
            w5 = y + 16*K1/135 + 6656*K3/12825 + 28561*K4/56430 - 9*K5/50 + 2*K6/55
            
            # Error
            R = abs(w5 - w4) / h if h > 0 else 0
            self.steps.append(f"  w⁽⁴⁾={w4:.6f}, w̃⁽⁵⁾={w5:.6f}, R={R:.2e}")
            
            if R <= tol:
                self.steps.append(f"  ✓ R ≤ ε → ACEPTAR")
                t = t + h
                y = w5
                t_vals.append(t)
                y_vals.append(y)
                step += 1
            else:
                self.steps.append(f"  ✗ R > ε → RECHAZAR")
            
            # Nuevo h
            if R > 0:
                q = 0.84 * (tol / R) ** 0.25
                q = max(0.1, min(q, 4.0))
                h = max(h_min, min(q * h, h_max))
                self.steps.append(f"  q={q:.4f}, h_nuevo={h:.6f}")
        
        self._add_results_table(t_vals, y_vals)
        return np.array(t_vals), np.array(y_vals), self.steps
    
    def adams_bashforth(self, f: Callable, t0: float, y0: float,
                        t_end: float, h: float) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Adams-Bashforth orden 4 (Explícito).
        
        Fórmula según PDF 49MN:
        w_{λ+1} = w_λ + (h/24)[55f_λ - 59f_{λ-1} + 37f_{λ-2} - 9f_{λ-3}]
        
        Inicialización con RK4 para obtener w₀, w₁, w₂, w₃.
        """
        self.steps = []
        self.steps.append("=" * 60)
        self.steps.append("ADAMS-BASHFORTH ORDEN 4 (Explícito)")
        self.steps.append("=" * 60)
        self.steps.append("w_(λ+1) = w_λ + (h/24)[55f_λ - 59f_(λ-1) + 37f_(λ-2) - 9f_(λ-3)]")
        self.steps.append(f"\nCondiciones: t₀={t0}, y₀={y0}, h={h}")
        
        # Inicializar con RK4
        self.steps.append("\n--- Inicialización con RK4 ---")
        t_vals, y_vals = [t0], [y0]
        f_vals = [f(t0, y0)]
        t, y = t0, y0
        
        for i in range(3):
            K1 = f(t, y)
            K2 = f(t + h/2, y + (h/2) * K1)
            K3 = f(t + h/2, y + (h/2) * K2)
            K4 = f(t + h, y + h * K3)
            y = y + (h/6) * (K1 + 2*K2 + 2*K3 + K4)
            t = t + h
            t_vals.append(t)
            y_vals.append(y)
            f_vals.append(f(t, y))
            self.steps.append(f"  RK4: t_{i+1}={t:.6f}, w_{i+1}={y:.6f}")
        
        # Adams-Bashforth
        self.steps.append("\n--- Adams-Bashforth ---")
        n = 3
        while t < t_end - 1e-10:
            y_new = y_vals[-1] + (h/24) * (
                55 * f_vals[-1] - 59 * f_vals[-2] + 37 * f_vals[-3] - 9 * f_vals[-4]
            )
            t = t + h
            t_vals.append(t)
            y_vals.append(y_new)
            f_vals.append(f(t, y_new))
            
            self.steps.append(f"  λ={n}: t={t:.6f}, w={y_new:.6f}")
            n += 1
        
        self._add_results_table(t_vals, y_vals)
        return np.array(t_vals), np.array(y_vals), self.steps
    
    def adams_moulton(self, *args, **kwargs):
        raise NotImplementedError(
            "Adams–Moulton no se programa según las restricciones."
        )

