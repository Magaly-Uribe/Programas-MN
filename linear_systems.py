"""
Métodos Numéricos para Sistemas Lineales
ESCOM - IPN

Incluye:
- Eliminación Gaussiana (Pivoteo Parcial, Escalado, Total)
- Factorización LU (Doolittle) con matrices elementales
- Factorización PLU (con pivoteo)
- Factorización Cholesky (A = L·Lᵀ)
- Factorización LDLᵀ (matrices simétricas)
- Mínimos Cuadrados (lineal, exponencial, potencial)
"""

import numpy as np
from typing import Tuple, List, Optional


class LinearSystemsSolver:
    """Clase para resolver sistemas lineales."""
    
    def __init__(self, precision: int = 6):
        self.precision = precision
        self.steps = []
    
    def _format_matrix(self, A: np.ndarray, b: Optional[np.ndarray] = None, 
                       name: str = "Matriz") -> str:
        """Formatea una matriz para mostrar."""
        n = A.shape[0]
        result = f"{name}:\n"
        for i in range(n):
            row = "  ["
            for j in range(A.shape[1]):
                row += f"{A[i,j]:10.{self.precision}f}"
            if b is not None:
                row += f" | {b[i]:10.{self.precision}f}"
            row += " ]"
            result += row + "\n"
        return result
    
    def _format_vector(self, x: np.ndarray, name: str = "x") -> str:
        """Formatea un vector para mostrar."""
        result = f"{name} = ["
        result += ", ".join([f"{xi:.{self.precision}f}" for xi in x])
        result += "]"
        return result
    
    # ==================== ELIMINACIÓN GAUSSIANA ====================
    
    def partial_pivoting(self, A: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, List[str]]:
        """
        Eliminación Gaussiana con Pivoteo Parcial.
        Busca el máximo |a_ik| en la columna k.
        """
        self.steps = []
        n = len(b)
        A = A.astype(float).copy()
        b = b.astype(float).copy()
        
        self.steps.append("=" * 60)
        self.steps.append("ELIMINACIÓN GAUSSIANA - PIVOTEO PARCIAL")
        self.steps.append("=" * 60)
        self.steps.append(self._format_matrix(A, b, "Matriz aumentada inicial"))
        
        # Fase de eliminación
        for k in range(n - 1):
            self.steps.append(f"\n{'─' * 40}")
            self.steps.append(f"PASO k = {k + 1}: Columna {k + 1}")
            self.steps.append("─" * 40)
            
            # Buscar pivote máximo en columna k
            max_idx = k
            max_val = abs(A[k, k])
            self.steps.append(f"\nBuscando pivote máximo en columna {k + 1}:")
            for i in range(k + 1, n):
                self.steps.append(f"  |a[{i+1},{k+1}]| = |{A[i,k]:.{self.precision}f}| = {abs(A[i,k]):.{self.precision}f}")
                if abs(A[i, k]) > max_val:
                    max_val = abs(A[i, k])
                    max_idx = i
            
            self.steps.append(f"\nMáximo: |{max_val:.{self.precision}f}| en fila {max_idx + 1}")
            
            # Intercambiar filas si es necesario
            if max_idx != k:
                self.steps.append(f"Intercambiar F{k + 1} ↔ F{max_idx + 1}")
                A[[k, max_idx]] = A[[max_idx, k]]
                b[[k, max_idx]] = b[[max_idx, k]]
                self.steps.append(self._format_matrix(A, b, "Después del intercambio"))
            else:
                self.steps.append("No se requiere intercambio")
            
            # Verificar pivote
            if abs(A[k, k]) < 1e-12:
                self.steps.append("ERROR: Pivote cercano a cero")
                raise ValueError("Sistema singular o mal condicionado")
            
            # Eliminación
            self.steps.append("\nCalculando factores y eliminando:")
            for i in range(k + 1, n):
                factor = A[i, k] / A[k, k]
                self.steps.append(f"  s_{i+1} = a[{i+1},{k+1}]/a[{k+1},{k+1}] = {A[i,k]:.{self.precision}f}/{A[k,k]:.{self.precision}f} = {factor:.{self.precision}f}")
                self.steps.append(f"  F{i + 1} ← F{i + 1} - ({factor:.{self.precision}f})·F{k + 1}")
                A[i, k:] -= factor * A[k, k:]
                b[i] -= factor * b[k]
            
            self.steps.append(self._format_matrix(A, b, f"Matriz después de k={k + 1}"))
        
        # Sustitución hacia atrás
        self.steps.append("\n" + "=" * 60)
        self.steps.append("SUSTITUCIÓN HACIA ATRÁS")
        self.steps.append("=" * 60)
        
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            suma = sum(A[i, j] * x[j] for j in range(i + 1, n))
            x[i] = (b[i] - suma) / A[i, i]
            self.steps.append(f"\nx_{i + 1} = (b_{i + 1} - Σa·x) / a[{i + 1},{i + 1}]")
            self.steps.append(f"x_{i + 1} = ({b[i]:.{self.precision}f} - {suma:.{self.precision}f}) / {A[i, i]:.{self.precision}f} = {x[i]:.{self.precision}f}")
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("SOLUCIÓN FINAL")
        self.steps.append("=" * 60)
        self.steps.append(self._format_vector(x))
        
        return x, self.steps
    
    def scaled_pivoting(self, A: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, List[str]]:
        """
        Eliminación Gaussiana con Pivoteo Escalado.
        Usa ratios r_i = |a_ik| / s_i donde s_i es el factor de escala.
        """
        self.steps = []
        n = len(b)
        A = A.astype(float).copy()
        b = b.astype(float).copy()
        
        self.steps.append("=" * 60)
        self.steps.append("ELIMINACIÓN GAUSSIANA - PIVOTEO ESCALADO")
        self.steps.append("=" * 60)
        self.steps.append(self._format_matrix(A, b, "Matriz aumentada inicial"))
        
        # Calcular factores de escala iniciales
        scale = np.array([max(abs(A[i, :])) for i in range(n)])
        self.steps.append("\nFactores de escala (máximo por fila):")
        for i in range(n):
            self.steps.append(f"  s_{i + 1} = max{{|a_{i + 1}j|}} = {scale[i]:.{self.precision}f}")
        
        # Fase de eliminación
        for k in range(n - 1):
            self.steps.append(f"\n{'─' * 40}")
            self.steps.append(f"PASO k = {k + 1}: Columna {k + 1}")
            self.steps.append("─" * 40)
            
            # Calcular ratios
            self.steps.append("\nCalculando ratios r_i = |a_ik| / s_i:")
            max_idx = k
            max_ratio = abs(A[k, k]) / scale[k] if scale[k] > 0 else 0
            self.steps.append(f"  r_{k + 1} = |{A[k, k]:.{self.precision}f}| / {scale[k]:.{self.precision}f} = {max_ratio:.{self.precision}f}")
            
            for i in range(k + 1, n):
                ratio = abs(A[i, k]) / scale[i] if scale[i] > 0 else 0
                self.steps.append(f"  r_{i + 1} = |{A[i, k]:.{self.precision}f}| / {scale[i]:.{self.precision}f} = {ratio:.{self.precision}f}")
                if ratio > max_ratio:
                    max_ratio = ratio
                    max_idx = i
            
            self.steps.append(f"\nMáximo ratio: {max_ratio:.{self.precision}f} en fila {max_idx + 1}")
            
            # Intercambiar filas y factores de escala
            if max_idx != k:
                self.steps.append(f"Intercambiar F{k + 1} ↔ F{max_idx + 1} (y sus factores de escala)")
                A[[k, max_idx]] = A[[max_idx, k]]
                b[[k, max_idx]] = b[[max_idx, k]]
                scale[[k, max_idx]] = scale[[max_idx, k]]
                self.steps.append(self._format_matrix(A, b, "Después del intercambio"))
            else:
                self.steps.append("No se requiere intercambio")
            
            # Verificar pivote
            if abs(A[k, k]) < 1e-12:
                raise ValueError("Sistema singular")
            
            # Eliminación
            self.steps.append("\nCalculando factores y eliminando:")
            for i in range(k + 1, n):
                factor = A[i, k] / A[k, k]
                self.steps.append(f"  s_{i+1} = {factor:.{self.precision}f}, F{i + 1} ← F{i + 1} - ({factor:.{self.precision}f})·F{k + 1}")
                A[i, k:] -= factor * A[k, k:]
                b[i] -= factor * b[k]
            
            self.steps.append(self._format_matrix(A, b, f"Matriz después de k={k + 1}"))
        
        # Sustitución hacia atrás
        self.steps.append("\n" + "=" * 60)
        self.steps.append("SUSTITUCIÓN HACIA ATRÁS")
        self.steps.append("=" * 60)
        
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            suma = sum(A[i, j] * x[j] for j in range(i + 1, n))
            x[i] = (b[i] - suma) / A[i, i]
            self.steps.append(f"x_{i + 1} = {x[i]:.{self.precision}f}")
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("SOLUCIÓN FINAL")
        self.steps.append("=" * 60)
        self.steps.append(self._format_vector(x))
        
        return x, self.steps
    
    def total_pivoting(self, A: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, List[str]]:
        """
        Eliminación Gaussiana con Pivoteo Total.
        Busca el máximo en toda la submatriz, intercambia filas Y columnas.
        ¡IMPORTANTE! Al final se reordena la solución.
        """
        self.steps = []
        n = len(b)
        A = A.astype(float).copy()
        b = b.astype(float).copy()
        
        # Vector de orden de columnas (para reordenar al final)
        col_order = list(range(n))
        
        self.steps.append("=" * 60)
        self.steps.append("ELIMINACIÓN GAUSSIANA - PIVOTEO TOTAL")
        self.steps.append("=" * 60)
        self.steps.append("⚠️ IMPORTANTE: Al final se debe REORDENAR la solución")
        self.steps.append(self._format_matrix(A, b, "Matriz aumentada inicial"))
        self.steps.append(f"Vector de orden inicial: {[i + 1 for i in col_order]}")
        
        # Fase de eliminación
        for k in range(n - 1):
            self.steps.append(f"\n{'─' * 40}")
            self.steps.append(f"PASO k = {k + 1}")
            self.steps.append("─" * 40)
            
            # Buscar máximo en toda la submatriz A[k:n, k:n]
            max_val = 0
            max_row, max_col = k, k
            self.steps.append(f"\nBuscando máximo en submatriz [{k + 1}:{n}, {k + 1}:{n}]:")
            for i in range(k, n):
                for j in range(k, n):
                    if abs(A[i, j]) > max_val:
                        max_val = abs(A[i, j])
                        max_row, max_col = i, j
            
            self.steps.append(f"Máximo: |{max_val:.{self.precision}f}| en posición ({max_row + 1}, {max_col + 1})")
            
            # Intercambiar filas
            if max_row != k:
                self.steps.append(f"Intercambiar F{k + 1} ↔ F{max_row + 1}")
                A[[k, max_row]] = A[[max_row, k]]
                b[[k, max_row]] = b[[max_row, k]]
            
            # Intercambiar columnas
            if max_col != k:
                self.steps.append(f"Intercambiar C{k + 1} ↔ C{max_col + 1}")
                A[:, [k, max_col]] = A[:, [max_col, k]]
                col_order[k], col_order[max_col] = col_order[max_col], col_order[k]
            
            self.steps.append(f"Vector de orden actual: {[i + 1 for i in col_order]}")
            self.steps.append(self._format_matrix(A, b, "Después de intercambios"))
            
            # Verificar pivote
            if abs(A[k, k]) < 1e-12:
                raise ValueError("Sistema singular")
            
            # Eliminación
            self.steps.append("\nEliminando:")
            for i in range(k + 1, n):
                factor = A[i, k] / A[k, k]
                self.steps.append(f"  s_{i+1} = {factor:.{self.precision}f}")
                A[i, k:] -= factor * A[k, k:]
                b[i] -= factor * b[k]
            
            self.steps.append(self._format_matrix(A, b, "Matriz después de eliminar"))
        
        # Sustitución hacia atrás (solución en orden de columnas permutadas)
        self.steps.append("\n" + "=" * 60)
        self.steps.append("SUSTITUCIÓN HACIA ATRÁS")
        self.steps.append("=" * 60)
        
        x_permuted = np.zeros(n)
        for i in range(n - 1, -1, -1):
            suma = sum(A[i, j] * x_permuted[j] for j in range(i + 1, n))
            x_permuted[i] = (b[i] - suma) / A[i, i]
            self.steps.append(f"v_{i + 1} = {x_permuted[i]:.{self.precision}f}")
        
        # Reordenar la solución
        self.steps.append("\n" + "=" * 60)
        self.steps.append("REORDENAMIENTO DE LA SOLUCIÓN")
        self.steps.append("=" * 60)
        self.steps.append(f"Vector de orden final: {[i + 1 for i in col_order]}")
        self.steps.append("\nSolución permutada (v):")
        self.steps.append(self._format_vector(x_permuted, "v"))
        
        # Reordenar: x[col_order[i]] = x_permuted[i]
        x = np.zeros(n)
        self.steps.append("\nReordenando según el vector de orden:")
        for i in range(n):
            x[col_order[i]] = x_permuted[i]
            self.steps.append(f"  x_{col_order[i] + 1} = v_{i + 1} = {x_permuted[i]:.{self.precision}f}")
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("SOLUCIÓN FINAL (REORDENADA)")
        self.steps.append("=" * 60)
        self.steps.append(self._format_vector(x))
        
        return x, self.steps
    
    # ==================== FACTORIZACIÓN LU ====================
    
    def lu_factorization(self, A: np.ndarray) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Factorización LU usando matrices elementales (método de Doolittle).
        A = L × U donde L tiene 1s en la diagonal.
        Los factores se guardan con signo POSITIVO en L.
        """
        self.steps = []
        n = A.shape[0]
        A = A.astype(float).copy()
        L = np.eye(n)
        U = A.copy()
        
        self.steps.append("=" * 60)
        self.steps.append("FACTORIZACIÓN LU (DOOLITTLE)")
        self.steps.append("Método de Matrices Elementales")
        self.steps.append("=" * 60)
        self.steps.append(self._format_matrix(A, name="Matriz A original"))
        
        self.steps.append("\nConcepto:")
        self.steps.append("  M · A = U  →  A = M⁻¹ · U = L · U")
        self.steps.append("  La matriz elemental M tiene -factor en posición (i,k)")
        self.steps.append("  Su inversa M⁻¹ tiene +factor en posición (i,k)")
        self.steps.append("  L = M⁻¹ (acumula los factores con signo +)")
        
        for k in range(n - 1):
            self.steps.append(f"\n{'─' * 40}")
            self.steps.append(f"ITERACIÓN {k + 1}: Columna {k + 1}")
            self.steps.append("─" * 40)
            
            if abs(U[k, k]) < 1e-12:
                raise ValueError("Pivote cero - se requiere PLU")
            
            self.steps.append("\nCalculando factores:")
            for i in range(k + 1, n):
                factor = U[i, k] / U[k, k]
                L[i, k] = factor  # Guardamos con signo +
                
                self.steps.append(f"  s_{i+1} = a[{i+1},{k+1}]/a[{k+1},{k+1}] = {U[i,k]:.{self.precision}f}/{U[k,k]:.{self.precision}f} = {factor:.{self.precision}f}")
                
                # Matriz elemental: -factor en posición (i,k)
                self.steps.append(f"  Matriz elemental M: -s_{i+1} = -{factor:.{self.precision}f} en posición ({i+1},{k+1})")
                self.steps.append(f"  Inversa M⁻¹: +s_{i+1} = +{factor:.{self.precision}f} en L[{i+1},{k+1}]")
                
                # Aplicar operación elemental
                self.steps.append(f"  R{i + 1} ← R{i + 1} - ({factor:.{self.precision}f})·R{k + 1}")
                U[i, k:] -= factor * U[k, k:]
            
            self.steps.append(self._format_matrix(U, name="U parcial"))
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("RESULTADO DE LA FACTORIZACIÓN")
        self.steps.append("=" * 60)
        self.steps.append(self._format_matrix(L, name="L (triangular inferior, 1s en diagonal)"))
        self.steps.append(self._format_matrix(U, name="U (triangular superior)"))
        
        # Verificación
        self.steps.append("\n" + "─" * 40)
        self.steps.append("VERIFICACIÓN: L × U = A")
        self.steps.append("─" * 40)
        LU = L @ U
        self.steps.append(self._format_matrix(LU, name="L × U"))
        
        return L, U, self.steps
    
    def lu_solve(self, L: np.ndarray, U: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, List[str]]:
        """
        Resuelve Ax = b usando factorización LU.
        1) Ly = b (sustitución adelante)
        2) Ux = y (sustitución atrás)
        """
        self.steps = []
        n = len(b)
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("RESOLVER SISTEMA CON LU")
        self.steps.append("=" * 60)
        self.steps.append(self._format_vector(b, "b"))
        
        # Sustitución adelante: Ly = b
        self.steps.append("\n" + "─" * 40)
        self.steps.append("PASO 1: Resolver Ly = b (sustitución adelante)")
        self.steps.append("─" * 40)
        
        y = np.zeros(n)
        for i in range(n):
            suma = sum(L[i, j] * y[j] for j in range(i))
            y[i] = b[i] - suma
            self.steps.append(f"y_{i + 1} = b_{i + 1} - Σ(L·y) = {b[i]:.{self.precision}f} - {suma:.{self.precision}f} = {y[i]:.{self.precision}f}")
        
        self.steps.append(self._format_vector(y, "y"))
        
        # Sustitución atrás: Ux = y
        self.steps.append("\n" + "─" * 40)
        self.steps.append("PASO 2: Resolver Ux = y (sustitución atrás)")
        self.steps.append("─" * 40)
        
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            suma = sum(U[i, j] * x[j] for j in range(i + 1, n))
            x[i] = (y[i] - suma) / U[i, i]
            self.steps.append(f"x_{i + 1} = (y_{i + 1} - Σ(U·x)) / U[{i + 1},{i + 1}] = ({y[i]:.{self.precision}f} - {suma:.{self.precision}f}) / {U[i, i]:.{self.precision}f} = {x[i]:.{self.precision}f}")
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("SOLUCIÓN")
        self.steps.append("=" * 60)
        self.steps.append(self._format_vector(x))
        
        return x, self.steps
    
    # ==================== FACTORIZACIÓN PLU ====================
    
    def plu_factorization(self, A: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[str]]:
        """
        Factorización PLU con pivoteo parcial.
        PA = LU donde P es matriz de permutación.
        Propiedad: P⁻¹ = Pᵀ
        """
        self.steps = []
        n = A.shape[0]
        A = A.astype(float).copy()
        L = np.zeros((n, n))
        U = A.copy()
        P = np.eye(n)
        
        self.steps.append("=" * 60)
        self.steps.append("FACTORIZACIÓN PLU (con pivoteo)")
        self.steps.append("=" * 60)
        self.steps.append("PA = LU  donde P⁻¹ = Pᵀ")
        self.steps.append(self._format_matrix(A, name="Matriz A original"))
        
        for k in range(n - 1):
            self.steps.append(f"\n{'─' * 40}")
            self.steps.append(f"ITERACIÓN {k + 1}")
            self.steps.append("─" * 40)
            
            # Buscar pivote máximo
            max_idx = k
            max_val = abs(U[k, k])
            for i in range(k + 1, n):
                if abs(U[i, k]) > max_val:
                    max_val = abs(U[i, k])
                    max_idx = i
            
            # Intercambiar si es necesario
            if max_idx != k:
                self.steps.append(f"Pivote máximo: |{max_val:.{self.precision}f}| en fila {max_idx + 1}")
                self.steps.append(f"Intercambiar F{k + 1} ↔ F{max_idx + 1}")
                U[[k, max_idx]] = U[[max_idx, k]]
                P[[k, max_idx]] = P[[max_idx, k]]
                # También intercambiar las columnas ya calculadas de L
                if k > 0:
                    L[[k, max_idx], :k] = L[[max_idx, k], :k]
            
            if abs(U[k, k]) < 1e-12:
                raise ValueError("Sistema singular")
            
            # Eliminación
            for i in range(k + 1, n):
                factor = U[i, k] / U[k, k]
                L[i, k] = factor
                U[i, k:] -= factor * U[k, k:]
                self.steps.append(f"  s_{i+1} = {factor:.{self.precision}f}")
        
        # Poner 1s en la diagonal de L
        np.fill_diagonal(L, 1)
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("RESULTADO")
        self.steps.append("=" * 60)
        self.steps.append(self._format_matrix(P, name="P (matriz de permutación)"))
        self.steps.append(self._format_matrix(L, name="L"))
        self.steps.append(self._format_matrix(U, name="U"))
        
        # Verificación
        self.steps.append("\n" + "─" * 40)
        self.steps.append("VERIFICACIÓN: PA = LU")
        PA = P @ A
        LU = L @ U
        self.steps.append(self._format_matrix(PA, name="PA"))
        self.steps.append(self._format_matrix(LU, name="LU"))
        
        return P, L, U, self.steps
    
    def plu_solve(self, P: np.ndarray, L: np.ndarray, U: np.ndarray, 
                  b: np.ndarray) -> Tuple[np.ndarray, List[str]]:
        """
        Resuelve Ax = b usando factorización PLU.
        1) Pb (permutar b)
        2) Ly = Pb
        3) Ux = y
        """
        self.steps = []
        n = len(b)
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("RESOLVER CON PLU")
        self.steps.append("=" * 60)
        
        # Permutar b
        Pb = P @ b
        self.steps.append(self._format_vector(b, "b original"))
        self.steps.append(self._format_vector(Pb, "Pb (permutado)"))
        
        # Resolver Ly = Pb
        self.steps.append("\nResolviendo Ly = Pb:")
        y = np.zeros(n)
        for i in range(n):
            suma = sum(L[i, j] * y[j] for j in range(i))
            y[i] = Pb[i] - suma
            self.steps.append(f"  y_{i + 1} = {y[i]:.{self.precision}f}")
        
        # Resolver Ux = y
        self.steps.append("\nResolviendo Ux = y:")
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            suma = sum(U[i, j] * x[j] for j in range(i + 1, n))
            x[i] = (y[i] - suma) / U[i, i]
            self.steps.append(f"  x_{i + 1} = {x[i]:.{self.precision}f}")
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("SOLUCIÓN")
        self.steps.append("=" * 60)
        self.steps.append(self._format_vector(x))
        
        return x, self.steps
    
    # ==================== FACTORIZACIÓN CHOLESKY ====================
    
    def cholesky_factorization(self, A: np.ndarray) -> Tuple[np.ndarray, List[str]]:
        """
        Factorización de Cholesky: A = L·Lᵀ
        Solo para matrices simétricas definidas positivas.
        
        Fórmulas:
        l_ii = √(a_ii - Σ(k<i) l_ik²)
        l_ji = (a_ji - Σ(k<i) l_jk·l_ik) / l_ii  para j > i
        """
        self.steps = []
        n = A.shape[0]
        A = A.astype(float)
        L = np.zeros((n, n))
        
        self.steps.append("=" * 60)
        self.steps.append("FACTORIZACIÓN DE CHOLESKY")
        self.steps.append("A = L · Lᵀ (para matrices simétricas definidas positivas)")
        self.steps.append("=" * 60)
        self.steps.append(self._format_matrix(A, name="Matriz A"))
        
        # Verificar simetría
        if not np.allclose(A, A.T):
            self.steps.append("\n⚠️ ADVERTENCIA: La matriz no es simétrica")
        
        self.steps.append("\nFórmulas:")
        self.steps.append("  l_ii = √(a_ii - Σ l_ik²)")
        self.steps.append("  l_ji = (a_ji - Σ l_jk·l_ik) / l_ii")
        
        for i in range(n):
            self.steps.append(f"\n{'─' * 40}")
            self.steps.append(f"Columna {i + 1}")
            self.steps.append("─" * 40)
            
            # Elemento diagonal
            suma = sum(L[i, k]**2 for k in range(i))
            val = A[i, i] - suma
            
            if val <= 0:
                self.steps.append(f"ERROR: a_{i+1}{i+1} - Σl²_ik = {val:.{self.precision}f} ≤ 0")
                self.steps.append("La matriz no es definida positiva")
                raise ValueError("Matriz no es definida positiva")
            
            L[i, i] = np.sqrt(val)
            self.steps.append(f"l_{i+1}{i+1} = √({A[i,i]:.{self.precision}f} - {suma:.{self.precision}f}) = √{val:.{self.precision}f} = {L[i,i]:.{self.precision}f}")
            
            # Elementos debajo de la diagonal
            for j in range(i + 1, n):
                suma = sum(L[j, k] * L[i, k] for k in range(i))
                L[j, i] = (A[j, i] - suma) / L[i, i]
                self.steps.append(f"l_{j+1}{i+1} = ({A[j,i]:.{self.precision}f} - {suma:.{self.precision}f}) / {L[i,i]:.{self.precision}f} = {L[j,i]:.{self.precision}f}")
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("RESULTADO")
        self.steps.append("=" * 60)
        self.steps.append(self._format_matrix(L, name="L"))
        self.steps.append(self._format_matrix(L.T, name="Lᵀ"))
        
        # Verificación
        self.steps.append("\n" + "─" * 40)
        self.steps.append("VERIFICACIÓN: L · Lᵀ = A")
        LLT = L @ L.T
        self.steps.append(self._format_matrix(LLT, name="L · Lᵀ"))
        
        return L, self.steps
    
    # ==================== FACTORIZACIÓN LDLᵀ ====================
    
    def ldlt_factorization(self, A: np.ndarray) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Factorización LDLᵀ: A = L·D·Lᵀ
        Para matrices simétricas.
        
        Fórmulas:
        d_j = a_jj - Σ(k<j) l_jk² · d_k
        l_ij = (a_ij - Σ(k<j) l_ik · l_jk · d_k) / d_j  para i > j
        """
        self.steps = []
        n = A.shape[0]
        A = A.astype(float)
        L = np.eye(n)
        D = np.zeros(n)
        
        self.steps.append("=" * 60)
        self.steps.append("FACTORIZACIÓN LDLᵀ")
        self.steps.append("A = L · D · Lᵀ (para matrices simétricas)")
        self.steps.append("=" * 60)
        self.steps.append(self._format_matrix(A, name="Matriz A"))
        
        self.steps.append("\nFórmulas:")
        self.steps.append("  d_j = a_jj - Σ l_jk² · d_k")
        self.steps.append("  l_ij = (a_ij - Σ l_ik · l_jk · d_k) / d_j")
        
        for j in range(n):
            self.steps.append(f"\n{'─' * 40}")
            self.steps.append(f"Columna j = {j + 1}")
            self.steps.append("─" * 40)
            
            # Calcular d_j
            suma_d = sum(L[j, k]**2 * D[k] for k in range(j))
            D[j] = A[j, j] - suma_d
            self.steps.append(f"d_{j+1} = a_{j+1}{j+1} - Σ(l²·d) = {A[j,j]:.{self.precision}f} - {suma_d:.{self.precision}f} = {D[j]:.{self.precision}f}")
            
            if abs(D[j]) < 1e-12:
                raise ValueError("d_j = 0, factorización no posible")
            
            # Calcular l_ij para i > j
            for i in range(j + 1, n):
                suma_l = sum(L[i, k] * L[j, k] * D[k] for k in range(j))
                L[i, j] = (A[i, j] - suma_l) / D[j]
                self.steps.append(f"l_{i+1}{j+1} = ({A[i,j]:.{self.precision}f} - {suma_l:.{self.precision}f}) / {D[j]:.{self.precision}f} = {L[i,j]:.{self.precision}f}")
        
        D_matrix = np.diag(D)
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("RESULTADO")
        self.steps.append("=" * 60)
        self.steps.append(self._format_matrix(L, name="L (triangular inferior, 1s en diagonal)"))
        self.steps.append(f"D (diagonal) = [{', '.join([f'{d:.{self.precision}f}' for d in D])}]")
        self.steps.append(self._format_matrix(L.T, name="Lᵀ"))
        
        # Verificación
        self.steps.append("\n" + "─" * 40)
        self.steps.append("VERIFICACIÓN: L · D · Lᵀ = A")
        LDLT = L @ D_matrix @ L.T
        self.steps.append(self._format_matrix(LDLT, name="L · D · Lᵀ"))
        
        return L, D, self.steps


class LeastSquares:
    """Clase para ajuste por mínimos cuadrados."""
    
    def __init__(self, precision: int = 6):
        self.precision = precision
        self.steps = []
    
    def linear_fit(self, x: np.ndarray, y: np.ndarray) -> Tuple[float, float, float, List[str]]:
        """
        Ajuste lineal: y = a₀ + a₁·x
        
        Fórmulas:
        a₁ = (n·Σxy - Σx·Σy) / (n·Σx² - (Σx)²)
        a₀ = (Σy - a₁·Σx) / n
        """
        self.steps = []
        n = len(x)
        
        self.steps.append("=" * 60)
        self.steps.append("MÍNIMOS CUADRADOS - AJUSTE LINEAL")
        self.steps.append("Modelo: y = a₀ + a₁·x")
        self.steps.append("=" * 60)
        
        # Calcular sumas
        sum_x = np.sum(x)
        sum_y = np.sum(y)
        sum_xy = np.sum(x * y)
        sum_x2 = np.sum(x**2)
        sum_y2 = np.sum(y**2)
        
        self.steps.append("\nTabla de datos:")
        self.steps.append(f"{'i':>3} {'xᵢ':>12} {'yᵢ':>12} {'xᵢ²':>12} {'xᵢyᵢ':>12}")
        self.steps.append("-" * 55)
        for i in range(n):
            self.steps.append(f"{i+1:>3} {x[i]:>12.{self.precision}f} {y[i]:>12.{self.precision}f} {x[i]**2:>12.{self.precision}f} {x[i]*y[i]:>12.{self.precision}f}")
        self.steps.append("-" * 55)
        self.steps.append(f"{'Σ':>3} {sum_x:>12.{self.precision}f} {sum_y:>12.{self.precision}f} {sum_x2:>12.{self.precision}f} {sum_xy:>12.{self.precision}f}")
        
        # Calcular coeficientes
        denom = n * sum_x2 - sum_x**2
        a1 = (n * sum_xy - sum_x * sum_y) / denom
        a0 = (sum_y - a1 * sum_x) / n
        
        self.steps.append(f"\nn = {n}")
        self.steps.append(f"\na₁ = (n·Σxy - Σx·Σy) / (n·Σx² - (Σx)²)")
        self.steps.append(f"a₁ = ({n}·{sum_xy:.{self.precision}f} - {sum_x:.{self.precision}f}·{sum_y:.{self.precision}f}) / ({n}·{sum_x2:.{self.precision}f} - {sum_x:.{self.precision}f}²)")
        self.steps.append(f"a₁ = {a1:.{self.precision}f}")
        
        self.steps.append(f"\na₀ = (Σy - a₁·Σx) / n")
        self.steps.append(f"a₀ = ({sum_y:.{self.precision}f} - {a1:.{self.precision}f}·{sum_x:.{self.precision}f}) / {n}")
        self.steps.append(f"a₀ = {a0:.{self.precision}f}")
        
        # Coeficiente de correlación
        r = (n * sum_xy - sum_x * sum_y) / np.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
        
        self.steps.append(f"\nCoeficiente de correlación:")
        self.steps.append(f"r = {r:.{self.precision}f}")
        self.steps.append(f"r² = {r**2:.{self.precision}f}")
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("RESULTADO")
        self.steps.append("=" * 60)
        self.steps.append(f"y = {a0:.{self.precision}f} + {a1:.{self.precision}f}·x")
        
        return a0, a1, r, self.steps
    
    def exponential_fit(self, x: np.ndarray, y: np.ndarray) -> Tuple[float, float, float, List[str]]:
        """
        Ajuste exponencial: y = a·e^(bx)
        Linealización: ln(y) = ln(a) + b·x
        """
        self.steps = []
        
        self.steps.append("=" * 60)
        self.steps.append("MÍNIMOS CUADRADOS - AJUSTE EXPONENCIAL")
        self.steps.append("Modelo: y = a·e^(bx)")
        self.steps.append("=" * 60)
        
        self.steps.append("\nLinealización: ln(y) = ln(a) + b·x")
        self.steps.append("Sea Y = ln(y), A = ln(a)")
        self.steps.append("Modelo linealizado: Y = A + b·x")
        
        # Linealizar
        Y = np.log(y)
        
        # Ajuste lineal sobre (x, Y)
        n = len(x)
        sum_x = np.sum(x)
        sum_Y = np.sum(Y)
        sum_xY = np.sum(x * Y)
        sum_x2 = np.sum(x**2)
        
        denom = n * sum_x2 - sum_x**2
        b = (n * sum_xY - sum_x * sum_Y) / denom
        A = (sum_Y - b * sum_x) / n
        a = np.exp(A)
        
        self.steps.append(f"\nb = {b:.{self.precision}f}")
        self.steps.append(f"A = ln(a) = {A:.{self.precision}f}")
        self.steps.append(f"a = e^A = {a:.{self.precision}f}")
        
        # Correlación
        sum_Y2 = np.sum(Y**2)
        r = (n * sum_xY - sum_x * sum_Y) / np.sqrt((n * sum_x2 - sum_x**2) * (n * sum_Y2 - sum_Y**2))
        
        self.steps.append(f"\nr (sobre datos linealizados) = {r:.{self.precision}f}")
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("RESULTADO")
        self.steps.append("=" * 60)
        self.steps.append(f"y = {a:.{self.precision}f} · e^({b:.{self.precision}f}·x)")
        
        return a, b, r, self.steps
    
    def power_fit(self, x: np.ndarray, y: np.ndarray) -> Tuple[float, float, float, List[str]]:
        """
        Ajuste potencial: y = a·x^b
        Linealización: ln(y) = ln(a) + b·ln(x)
        """
        self.steps = []
        
        self.steps.append("=" * 60)
        self.steps.append("MÍNIMOS CUADRADOS - AJUSTE POTENCIAL")
        self.steps.append("Modelo: y = a·x^b")
        self.steps.append("=" * 60)
        
        self.steps.append("\nLinealización: ln(y) = ln(a) + b·ln(x)")
        self.steps.append("Sea Y = ln(y), X = ln(x), A = ln(a)")
        self.steps.append("Modelo linealizado: Y = A + b·X")
        
        # Linealizar
        X = np.log(x)
        Y = np.log(y)
        
        # Ajuste lineal sobre (X, Y)
        n = len(X)
        sum_X = np.sum(X)
        sum_Y = np.sum(Y)
        sum_XY = np.sum(X * Y)
        sum_X2 = np.sum(X**2)
        
        denom = n * sum_X2 - sum_X**2
        b = (n * sum_XY - sum_X * sum_Y) / denom
        A = (sum_Y - b * sum_X) / n
        a = np.exp(A)
        
        self.steps.append(f"\nb = {b:.{self.precision}f}")
        self.steps.append(f"A = ln(a) = {A:.{self.precision}f}")
        self.steps.append(f"a = e^A = {a:.{self.precision}f}")
        
        # Correlación
        sum_Y2 = np.sum(Y**2)
        r = (n * sum_XY - sum_X * sum_Y) / np.sqrt((n * sum_X2 - sum_X**2) * (n * sum_Y2 - sum_Y**2))
        
        self.steps.append(f"\nr (sobre datos linealizados) = {r:.{self.precision}f}")
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("RESULTADO")
        self.steps.append("=" * 60)
        self.steps.append(f"y = {a:.{self.precision}f} · x^{b:.{self.precision}f}")
        
        return a, b, r, self.steps
    
    def polynomial_fit(self, x: np.ndarray, y: np.ndarray, degree: int) -> Tuple[np.ndarray, List[str]]:
        """
        Ajuste polinomial de grado n.
        Resuelve las ecuaciones normales.
        """
        self.steps = []
        m = len(x)
        
        self.steps.append("=" * 60)
        self.steps.append(f"MÍNIMOS CUADRADOS - AJUSTE POLINOMIAL GRADO {degree}")
        self.steps.append(f"Modelo: y = a₀ + a₁x + a₂x² + ... + a_{degree}x^{degree}")
        self.steps.append("=" * 60)
        
        # Construir matriz del sistema normal
        n = degree + 1
        A = np.zeros((n, n))
        b = np.zeros(n)
        
        for i in range(n):
            for j in range(n):
                A[i, j] = np.sum(x**(i + j))
            b[i] = np.sum(y * x**i)
        
        self.steps.append("\nSistema de ecuaciones normales:")
        self.steps.append(f"Matriz A ({n}×{n}) y vector b:")
        
        # Resolver sistema
        coefs = np.linalg.solve(A, b)
        
        self.steps.append("\n" + "=" * 60)
        self.steps.append("RESULTADO")
        self.steps.append("=" * 60)
        
        poly_str = f"y = {coefs[0]:.{self.precision}f}"
        for i in range(1, n):
            if coefs[i] >= 0:
                poly_str += f" + {coefs[i]:.{self.precision}f}·x"
            else:
                poly_str += f" - {abs(coefs[i]):.{self.precision}f}·x"
            if i > 1:
                poly_str += f"^{i}"
        
        self.steps.append(poly_str)
        
        return coefs, self.steps
