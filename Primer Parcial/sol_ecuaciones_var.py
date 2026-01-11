import math
import sympy as sp
import numpy as np

class SolEcuaciones:
    """Clase para resolver ecuaciones de una variable"""
    
    def __init__(self, a=0, b=0, max_iter=100, tolerancia=1e-6):
        """
        Inicializar solver
        
        Args:
            a: límite inferior o valor inicial
            b: límite superior o segundo valor
            max_iter: máximo de iteraciones
            tolerancia: error máximo permitido
        """
        self.a = a
        self.b = b
        self.max_iter = max_iter
        self.tolerancia = tolerancia
        self.funcion_str = ""
        self.funcion = None
        self.x = sp.symbols('x')
    
    def set_funcion(self, funcion_str):
        """Establecer la función a evaluar"""
        self.funcion_str = funcion_str
        try:
            # Convertir string a expresión sympy
            self.funcion = sp.sympify(funcion_str)
        except:
            raise ValueError(f"Función inválida: {funcion_str}")
    
    def evaluar(self, x):
        """Evaluar la función en un punto x"""
        if self.funcion is None:
            raise ValueError("No se ha establecido la función")
        
        # Sustituir x en la expresión
        expr = self.funcion.subs(self.x, x)
        # Evaluar numéricamente
        return float(expr.evalf())
    
    def derivada_numerica(self, x, h=1e-6):
        """Calcular derivada numérica"""
        return (self.evaluar(x + h) - self.evaluar(x - h)) / (2 * h)
    
    def biseccion(self):
        """Método de bisección"""
        if self.funcion is None:
            raise ValueError("No se ha establecido la función")
        
        a = self.a
        b = self.b
        fa = self.evaluar(a)
        fb = self.evaluar(b)
        
        # Verificar cambio de signo
        if fa * fb > 0:
            raise ValueError("No hay cambio de signo en el intervalo [a, b]")
        
        resultados = []
        for i in range(self.max_iter):
            c = (a + b) / 2
            fc = self.evaluar(c)
            
            resultados.append({
                'iteracion': i + 1,
                'a': a,
                'c': c,
                'b': b,
                'f(a)': fa,
                'f(c)': fc,
                'f(b)': fb,
                'error': abs(b - a)
            })
            
            # Verificar convergencia
            if abs(fc) < self.tolerancia or abs(b - a) < self.tolerancia:
                return c, resultados
            
            # Actualizar intervalo
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
        
        raise ValueError(f"No convergió en {self.max_iter} iteraciones")
    
    def falsa_posicion(self):
        """Método de falsa posición"""
        if self.funcion is None:
            raise ValueError("No se ha establecido la función")
        
        a = self.a
        b = self.b
        fa = self.evaluar(a)
        fb = self.evaluar(b)
        
        # Verificar cambio de signo
        if fa * fb > 0:
            raise ValueError("No hay cambio de signo en el intervalo [a, b]")
        
        resultados = []
        for i in range(self.max_iter):
            # Calcular c por falsa posición
            c = (a * fb - b * fa) / (fb - fa)
            fc = self.evaluar(c)
            
            resultados.append({
                'iteracion': i + 1,
                'a': a,
                'c': c,
                'b': b,
                'f(a)': fa,
                'f(c)': fc,
                'f(b)': fb,
                'error': abs(c - a)
            })
            
            # Verificar convergencia
            if abs(fc) < self.tolerancia:
                return c, resultados
            
            # Actualizar intervalo
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
        
        raise ValueError(f"No convergió en {self.max_iter} iteraciones")
    
    def secante(self):
        """Método de la secante"""
        if self.funcion is None:
            raise ValueError("No se ha establecido la función")
        
        x0 = self.a
        x1 = self.b
        f0 = self.evaluar(x0)
        f1 = self.evaluar(x1)
        
        resultados = []
        for i in range(self.max_iter):
            # Evitar división por cero
            if abs(f1 - f0) < 1e-15:
                raise ValueError("División por cero en método de la secante")
            
            # Calcular siguiente punto
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            f2 = self.evaluar(x2)
            
            resultados.append({
                'iteracion': i + 1,
                'x0': x0,
                'x1': x1,
                'x2': x2,
                'f(x0)': f0,
                'f(x1)': f1,
                'error': abs(x2 - x1)
            })
            
            # Verificar convergencia
            if abs(x2 - x1) < self.tolerancia:
                return x2, resultados
            
            # Actualizar valores
            x0, f0 = x1, f1
            x1, f1 = x2, f2
        
        raise ValueError(f"No convergió en {self.max_iter} iteraciones")
    
    def newton_raphson(self):
        """Método de Newton-Raphson"""
        if self.funcion is None:
            raise ValueError("No se ha establecido la función")
        
        x = self.a
        resultados = []
        
        for i in range(self.max_iter):
            fx = self.evaluar(x)
            dfx = self.derivada_numerica(x)
            
            # Evitar división por cero
            if abs(dfx) < 1e-15:
                raise ValueError("Derivada cero en Newton-Raphson")
            
            # Calcular siguiente punto
            x_new = x - fx / dfx
            
            resultados.append({
                'iteracion': i + 1,
                'x': x,
                'f(x)': fx,
                "f'(x)": dfx,
                'x_new': x_new,
                'error': abs(x_new - x)
            })
            
            # Verificar convergencia
            if abs(x_new - x) < self.tolerancia:
                return x_new, resultados
            
            x = x_new
        
        raise ValueError(f"No convergió en {self.max_iter} iteraciones")
    
    def punto_fijo(self, x0, a, b):
        """Método de punto fijo"""
        if self.funcion is None:
            raise ValueError("No se ha establecido la función")
        
        x = x0
        resultados = []
        
        for i in range(self.max_iter):
            x_new = self.evaluar(x)
            
            resultados.append({
                'iteracion': i + 1,
                'x': x,
                'g(x)': x_new,
                'error': abs(x_new - x)
            })
            
            # Verificar convergencia
            if abs(x_new - x) < self.tolerancia:
                return x_new, resultados
            
            # Verificar que no salga del intervalo
            if x_new < a or x_new > b:
                raise ValueError(f"Iteración {i+1} sale del intervalo [{a}, {b}]")
            
            x = x_new
        
        raise ValueError(f"No convergió en {self.max_iter} iteraciones")
    
    def muller(self, x0, x1, x2):
        """Método de Müller"""
        if self.funcion is None:
            raise ValueError("No se ha establecido la función")
        
        # Evaluar en puntos iniciales
        f0 = self.evaluar(x0)
        f1 = self.evaluar(x1)
        f2 = self.evaluar(x2)
        
        resultados = []
        
        for i in range(self.max_iter):
            # Calcular diferencias
            h1 = x1 - x0
            h2 = x2 - x1
            
            # Evitar división por cero
            if abs(h1) < 1e-15 or abs(h2) < 1e-15:
                raise ValueError("Puntos repetidos en Müller")
            
            delta1 = (f1 - f0) / h1
            delta2 = (f2 - f1) / h2
            
            d = (delta2 - delta1) / (h2 + h1)
            b = delta2 + h2 * d
            discriminante = b**2 - 4 * d * f2
            
            # Manejar raíces complejas
            if discriminante < 0:
                discriminante = abs(discriminante)
            
            D = math.sqrt(discriminante)
            
            # Elegir denominador mayor
            denom1 = b + D
            denom2 = b - D
            denom = denom1 if abs(denom1) > abs(denom2) else denom2
            
            if abs(denom) < 1e-15:
                raise ValueError("Denominador cero en Müller")
            
            # Calcular siguiente punto
            x3 = x2 - 2 * f2 / denom
            f3 = self.evaluar(x3)
            
            resultados.append({
                'iteracion': i + 1,
                'x0': x0,
                'x1': x1,
                'x2': x2,
                'x3': x3,
                'error': abs(x3 - x2)
            })
            
            # Verificar convergencia
            if abs(x3 - x2) < self.tolerancia:
                return x3, resultados
            
            # Actualizar para siguiente iteración
            x0, f0 = x1, f1
            x1, f1 = x2, f2
            x2, f2 = x3, f3
        
        raise ValueError(f"No convergió en {self.max_iter} iteraciones")
    
