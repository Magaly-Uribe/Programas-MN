"""
Métodos Numéricos - Interfaz Gráfica Principal
ESCOM - IPN

Incluye todas las pestañas:
1. Eliminación Gaussiana (Parcial, Escalado, Total)
2. Factorización (LU, PLU, Cholesky, LDLᵀ)
3. EDOs (Euler, Taylor, RK2, RK3, RK4, RKF45, Adams)
4. Sistemas de EDOs
5. Mínimos Cuadrados
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importar módulos
from linear_systems import LinearSystemsSolver, LeastSquares
from ode_basic import ODEBasicMethods
from ode_advanced import ODEAdvancedMethods
from ode_systems import ODESystemSolver, HigherOrderConverter


class AplicacionMetodosNumericos:
    """Aplicación principal."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos - ESCOM IPN")
        self.root.geometry("1300x800")
        
        # Inicializar solvers
        self.linear = LinearSystemsSolver()
        self.least_sq = LeastSquares()
        self.ode_basic = ODEBasicMethods()
        self.ode_adv = ODEAdvancedMethods()
        self.ode_sys = ODESystemSolver()
        
        # Notebook principal
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear pestañas
        self.crear_pestana_gauss()
        self.crear_pestana_factorizacion()
        self.crear_pestana_edo()
        self.crear_pestana_sistemas()
        self.crear_pestana_minimos_cuadrados()
    
    # ==================== ELIMINACIÓN GAUSSIANA ====================
    def crear_pestana_gauss(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Eliminación Gaussiana")
        
        # Panel izquierdo
        panel_izq = ttk.Frame(frame)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(panel_izq, text="Eliminación Gaussiana", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Método
        tk.Label(panel_izq, text="Método:").pack(anchor=tk.W)
        self.metodo_gauss = tk.StringVar(value="partial")
        for txt, val in [("Pivoteo Parcial", "partial"),
                         ("Pivoteo Escalado", "scaled"),
                         ("Pivoteo Total", "total")]:
            tk.Radiobutton(panel_izq, text=txt, variable=self.metodo_gauss, 
                          value=val).pack(anchor=tk.W)
        
        # Tamaño
        frame_n = tk.Frame(panel_izq)
        frame_n.pack(pady=10, anchor=tk.W)
        tk.Label(frame_n, text="n:").pack(side=tk.LEFT)
        self.gauss_n = tk.StringVar(value="3")
        tk.Spinbox(frame_n, from_=2, to=8, width=5, 
                   textvariable=self.gauss_n).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_n, text="Crear", 
                  command=self.crear_matriz_gauss).pack(side=tk.LEFT)
        
        # Matriz
        self.frame_matriz_gauss = tk.LabelFrame(panel_izq, text="[A|b]")
        self.frame_matriz_gauss.pack(pady=10)
        self.entradas_gauss = []
        self.entradas_b_gauss = []
        self.crear_matriz_gauss()
        
        # Botones
        frame_btn = tk.Frame(panel_izq)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Ejemplo", 
                  command=self.ejemplo_gauss).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_btn, text="Limpiar", 
                  command=self.limpiar_gauss).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_btn, text="Resolver", bg='#4CAF50', fg='white',
                  command=self.resolver_gauss).pack(side=tk.LEFT, padx=3)
        
        # Resultados
        panel_der = ttk.Frame(frame)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(panel_der, text="Procedimiento:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        self.resultado_gauss = scrolledtext.ScrolledText(panel_der, width=70, height=45, font=('Courier', 9))
        self.resultado_gauss.pack(fill=tk.BOTH, expand=True)
    
    def crear_matriz_gauss(self):
        for w in self.frame_matriz_gauss.winfo_children():
            w.destroy()
        
        n = int(self.gauss_n.get()) if self.gauss_n.get().isdigit() else 3
        self.entradas_gauss = []
        self.entradas_b_gauss = []
        
        for i in range(n):
            fila = []
            f = tk.Frame(self.frame_matriz_gauss)
            f.pack()
            for j in range(n):
                e = tk.Entry(f, width=7, justify='center')
                e.pack(side=tk.LEFT, padx=1, pady=1)
                e.insert(0, "0")
                fila.append(e)
            tk.Label(f, text="|").pack(side=tk.LEFT)
            eb = tk.Entry(f, width=7, justify='center')
            eb.pack(side=tk.LEFT, padx=1, pady=1)
            eb.insert(0, "0")
            self.entradas_b_gauss.append(eb)
            self.entradas_gauss.append(fila)
    
    def ejemplo_gauss(self):
        self.gauss_n.set("3")
        self.crear_matriz_gauss()
        A = [[2, -1, 1], [3, 3, 9], [3, 3, 5]]
        b = [2, -1, 4]
        for i in range(3):
            for j in range(3):
                self.entradas_gauss[i][j].delete(0, tk.END)
                self.entradas_gauss[i][j].insert(0, str(A[i][j]))
            self.entradas_b_gauss[i].delete(0, tk.END)
            self.entradas_b_gauss[i].insert(0, str(b[i]))
    
    def limpiar_gauss(self):
        for i in range(len(self.entradas_gauss)):
            for j in range(len(self.entradas_gauss)):
                self.entradas_gauss[i][j].delete(0, tk.END)
                self.entradas_gauss[i][j].insert(0, "0")
            self.entradas_b_gauss[i].delete(0, tk.END)
            self.entradas_b_gauss[i].insert(0, "0")
        self.resultado_gauss.delete(1.0, tk.END)
    
    def resolver_gauss(self):
        try:
            n = len(self.entradas_gauss)
            A = np.array([[float(self.entradas_gauss[i][j].get()) for j in range(n)] for i in range(n)])
            b = np.array([float(self.entradas_b_gauss[i].get()) for i in range(n)])
            
            metodo = self.metodo_gauss.get()
            if metodo == "partial":
                x, pasos = self.linear.partial_pivoting(A, b)
            elif metodo == "scaled":
                x, pasos = self.linear.scaled_pivoting(A, b)
            else:
                x, pasos = self.linear.total_pivoting(A, b)
            
            self.resultado_gauss.delete(1.0, tk.END)
            for p in pasos:
                self.resultado_gauss.insert(tk.END, p + "\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== FACTORIZACIÓN ====================
    def crear_pestana_factorizacion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Factorización")
        
        panel_izq = ttk.Frame(frame)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(panel_izq, text="Factorización de Matrices", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Tipo
        tk.Label(panel_izq, text="Tipo:").pack(anchor=tk.W)
        self.tipo_fact = tk.StringVar(value="lu")
        for txt, val in [("LU (Doolittle)", "lu"), 
                         ("PLU (con pivoteo)", "plu"),
                         ("Cholesky (A=LLᵀ)", "cholesky"),
                         ("LDLᵀ (simétrica)", "ldlt")]:
            tk.Radiobutton(panel_izq, text=txt, variable=self.tipo_fact, 
                          value=val).pack(anchor=tk.W)
        
        self.resolver_sistema_var = tk.BooleanVar(value=True)
        tk.Checkbutton(panel_izq, text="Resolver Ax=b", 
                       variable=self.resolver_sistema_var).pack(anchor=tk.W, pady=5)
        
        # Tamaño
        frame_n = tk.Frame(panel_izq)
        frame_n.pack(pady=10, anchor=tk.W)
        tk.Label(frame_n, text="n:").pack(side=tk.LEFT)
        self.fact_n = tk.StringVar(value="3")
        tk.Spinbox(frame_n, from_=2, to=8, width=5, 
                   textvariable=self.fact_n).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_n, text="Crear", 
                  command=self.crear_matriz_fact).pack(side=tk.LEFT)
        
        self.frame_matriz_fact = tk.LabelFrame(panel_izq, text="A | b")
        self.frame_matriz_fact.pack(pady=10)
        self.entradas_fact = []
        self.entradas_b_fact = []
        self.crear_matriz_fact()
        
        frame_btn = tk.Frame(panel_izq)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Ejemplo", command=self.ejemplo_fact).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_btn, text="Limpiar", command=self.limpiar_fact).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_btn, text="Factorizar", bg='#4CAF50', fg='white',
                  command=self.resolver_fact).pack(side=tk.LEFT, padx=3)
        
        panel_der = ttk.Frame(frame)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(panel_der, text="Procedimiento:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        self.resultado_fact = scrolledtext.ScrolledText(panel_der, width=70, height=45, font=('Courier', 9))
        self.resultado_fact.pack(fill=tk.BOTH, expand=True)
    
    def crear_matriz_fact(self):
        for w in self.frame_matriz_fact.winfo_children():
            w.destroy()
        
        n = int(self.fact_n.get()) if self.fact_n.get().isdigit() else 3
        self.entradas_fact = []
        self.entradas_b_fact = []
        
        for i in range(n):
            fila = []
            f = tk.Frame(self.frame_matriz_fact)
            f.pack()
            for j in range(n):
                e = tk.Entry(f, width=7, justify='center')
                e.pack(side=tk.LEFT, padx=1, pady=1)
                e.insert(0, "0")
                fila.append(e)
            tk.Label(f, text="|").pack(side=tk.LEFT)
            eb = tk.Entry(f, width=7, justify='center')
            eb.pack(side=tk.LEFT, padx=1, pady=1)
            eb.insert(0, "0")
            self.entradas_b_fact.append(eb)
            self.entradas_fact.append(fila)
    
    def ejemplo_fact(self):
        tipo = self.tipo_fact.get()
        self.fact_n.set("3")
        self.crear_matriz_fact()
        
        if tipo in ["cholesky", "ldlt"]:
            # Matriz simétrica definida positiva
            A = [[4, 2, 2], [2, 5, 1], [2, 1, 6]]
        else:
            A = [[2, 1, -1], [4, 5, -3], [-2, 5, -2]]
        b = [3, 9, -5]
        
        for i in range(3):
            for j in range(3):
                self.entradas_fact[i][j].delete(0, tk.END)
                self.entradas_fact[i][j].insert(0, str(A[i][j]))
            self.entradas_b_fact[i].delete(0, tk.END)
            self.entradas_b_fact[i].insert(0, str(b[i]))
    
    def limpiar_fact(self):
        for i in range(len(self.entradas_fact)):
            for j in range(len(self.entradas_fact)):
                self.entradas_fact[i][j].delete(0, tk.END)
                self.entradas_fact[i][j].insert(0, "0")
            self.entradas_b_fact[i].delete(0, tk.END)
            self.entradas_b_fact[i].insert(0, "0")
        self.resultado_fact.delete(1.0, tk.END)
    
    def resolver_fact(self):
        try:
            n = len(self.entradas_fact)
            A = np.array([[float(self.entradas_fact[i][j].get()) for j in range(n)] for i in range(n)])
            b = np.array([float(self.entradas_b_fact[i].get()) for i in range(n)])
            
            self.resultado_fact.delete(1.0, tk.END)
            tipo = self.tipo_fact.get()
            
            if tipo == "lu":
                L, U, pasos = self.linear.lu_factorization(A)
                for p in pasos:
                    self.resultado_fact.insert(tk.END, p + "\n")
                if self.resolver_sistema_var.get():
                    x, pasos2 = self.linear.lu_solve(L, U, b)
                    for p in pasos2:
                        self.resultado_fact.insert(tk.END, p + "\n")
            
            elif tipo == "plu":
                P, L, U, pasos = self.linear.plu_factorization(A)
                for p in pasos:
                    self.resultado_fact.insert(tk.END, p + "\n")
                if self.resolver_sistema_var.get():
                    x, pasos2 = self.linear.plu_solve(P, L, U, b)
                    for p in pasos2:
                        self.resultado_fact.insert(tk.END, p + "\n")
            
            elif tipo == "cholesky":
                L, pasos = self.linear.cholesky_factorization(A)
                for p in pasos:
                    self.resultado_fact.insert(tk.END, p + "\n")
            
            elif tipo == "ldlt":
                L, D, pasos = self.linear.ldlt_factorization(A)
                for p in pasos:
                    self.resultado_fact.insert(tk.END, p + "\n")
                    
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== EDOs ====================
    def crear_pestana_edo(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Ecuaciones Diferenciales")
        
        panel_izq = ttk.Frame(frame)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(panel_izq, text="EDOs de Primer Orden", 
                 font=('Arial', 14, 'bold')).pack(pady=5)
        
        tk.Label(panel_izq, text="dy/dt = f(t, y) =").pack(anchor=tk.W)
        self.ecuacion_edo = tk.Entry(panel_izq, width=30, font=('Courier', 10))
        self.ecuacion_edo.pack(fill=tk.X, pady=5)
        self.ecuacion_edo.insert(0, "y - t**2 + 1")
        tk.Label(panel_izq, text="Usa: t, y, sin, cos, exp, **", font=('Arial', 8)).pack(anchor=tk.W)
        
        # Método
        tk.Label(panel_izq, text="\nMétodo:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.metodo_edo = tk.StringVar(value="rk4")
        
        metodos = [("Euler", "euler"), ("Taylor 2", "taylor2"), ("Taylor 3", "taylor3"),
                   ("RK-2 (Punto Medio)", "rk2"), ("RK-3", "rk3"), ("RK-4 (Clásico)", "rk4"),
                   ("RK-Fehlberg 4-5", "rkf45"), ("Adams-Bashforth 4", "ab4"),
                   ("Adams-Moulton (P-C)", "am")]
        
        for txt, val in metodos:
            tk.Radiobutton(panel_izq, text=txt, variable=self.metodo_edo, value=val).pack(anchor=tk.W)
        
        # Parámetros
        tk.Label(panel_izq, text="\nParámetros:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        frame_p = tk.Frame(panel_izq)
        frame_p.pack(fill=tk.X, pady=5)
        
        tk.Label(frame_p, text="t₀:").grid(row=0, column=0)
        self.edo_t0 = tk.Entry(frame_p, width=8)
        self.edo_t0.grid(row=0, column=1, padx=5)
        self.edo_t0.insert(0, "0")
        
        tk.Label(frame_p, text="y₀:").grid(row=0, column=2)
        self.edo_y0 = tk.Entry(frame_p, width=8)
        self.edo_y0.grid(row=0, column=3, padx=5)
        self.edo_y0.insert(0, "0.5")
        
        tk.Label(frame_p, text="t_f:").grid(row=1, column=0)
        self.edo_tf = tk.Entry(frame_p, width=8)
        self.edo_tf.grid(row=1, column=1, padx=5)
        self.edo_tf.insert(0, "2")
        
        tk.Label(frame_p, text="h:").grid(row=1, column=2)
        self.edo_h = tk.Entry(frame_p, width=8)
        self.edo_h.grid(row=1, column=3, padx=5)
        self.edo_h.insert(0, "0.2")
        
        tk.Label(frame_p, text="tol:").grid(row=2, column=0)
        self.edo_tol = tk.Entry(frame_p, width=8)
        self.edo_tol.grid(row=2, column=1, padx=5)
        self.edo_tol.insert(0, "1e-6")
        
        # Botones
        frame_btn = tk.Frame(panel_izq)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Ejemplo", command=self.ejemplo_edo).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_btn, text="Limpiar", command=self.limpiar_edo).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_btn, text="Resolver", bg='#4CAF50', fg='white',
                  command=self.resolver_edo).pack(side=tk.LEFT, padx=3)
        
        # Panel derecho
        panel_der = ttk.Frame(frame)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Gráfica
        self.fig_edo = Figure(figsize=(6, 3.5), dpi=100)
        self.ax_edo = self.fig_edo.add_subplot(111)
        self.canvas_edo = FigureCanvasTkAgg(self.fig_edo, panel_der)
        self.canvas_edo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        tk.Label(panel_der, text="Procedimiento:").pack(anchor=tk.W)
        self.resultado_edo = scrolledtext.ScrolledText(panel_der, width=60, height=18, font=('Courier', 9))
        self.resultado_edo.pack(fill=tk.BOTH, expand=True)
    
    def ejemplo_edo(self):
        self.ecuacion_edo.delete(0, tk.END)
        self.ecuacion_edo.insert(0, "y - t**2 + 1")
        self.edo_t0.delete(0, tk.END); self.edo_t0.insert(0, "0")
        self.edo_y0.delete(0, tk.END); self.edo_y0.insert(0, "0.5")
        self.edo_tf.delete(0, tk.END); self.edo_tf.insert(0, "2")
        self.edo_h.delete(0, tk.END); self.edo_h.insert(0, "0.2")
    
    def limpiar_edo(self):
        self.resultado_edo.delete(1.0, tk.END)
        self.ax_edo.clear()
        self.canvas_edo.draw()
    
    def resolver_edo(self):
        try:
            eq = self.ecuacion_edo.get()
            t0 = float(self.edo_t0.get())
            y0 = float(self.edo_y0.get())
            tf = float(self.edo_tf.get())
            h = float(self.edo_h.get())
            tol = float(self.edo_tol.get())
            metodo = self.metodo_edo.get()
            
            f = self.ode_basic.parse_equation(eq)
            
            if metodo == "euler":
                t, y, pasos = self.ode_basic.euler(f, t0, y0, tf, h)
            elif metodo == "taylor2":
                t, y, pasos = self.ode_basic.taylor(eq, t0, y0, tf, h, 2)
            elif metodo == "taylor3":
                t, y, pasos = self.ode_basic.taylor(eq, t0, y0, tf, h, 3)
            elif metodo == "rk2":
                t, y, pasos = self.ode_basic.rk2(f, t0, y0, tf, h)
            elif metodo == "rk3":
                t, y, pasos = self.ode_basic.rk3(f, t0, y0, tf, h)
            elif metodo == "rk4":
                t, y, pasos = self.ode_basic.rk4(f, t0, y0, tf, h)
            elif metodo == "rkf45":
                t, y, pasos = self.ode_adv.rkf45(f, t0, y0, tf, h, tol)
            elif metodo == "ab4":
                t, y, pasos = self.ode_adv.adams_bashforth(f, t0, y0, tf, h)
            elif metodo == "am":
                t, y, pasos = self.ode_adv.adams_moulton(f, t0, y0, tf, h)
            
            self.resultado_edo.delete(1.0, tk.END)
            for p in pasos:
                self.resultado_edo.insert(tk.END, p + "\n")
            
            self.ax_edo.clear()
            self.ax_edo.plot(t, y, 'b-o', markersize=4)
            self.ax_edo.set_xlabel('t')
            self.ax_edo.set_ylabel('y')
            self.ax_edo.set_title(f"dy/dt = {eq}")
            self.ax_edo.grid(True, alpha=0.3)
            self.fig_edo.tight_layout()
            self.canvas_edo.draw()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== SISTEMAS EDOs ====================
    def crear_pestana_sistemas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Sistemas de EDOs")
        
        panel_izq = ttk.Frame(frame)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(panel_izq, text="Sistemas de EDOs", font=('Arial', 14, 'bold')).pack(pady=5)
        
        frame_n = tk.Frame(panel_izq)
        frame_n.pack(anchor=tk.W)
        tk.Label(frame_n, text="Número de ecuaciones:").pack(side=tk.LEFT)
        self.sys_n = tk.StringVar(value="2")
        tk.Spinbox(frame_n, from_=2, to=4, width=5, textvariable=self.sys_n).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_n, text="Crear", command=self.crear_sistema_edo).pack(side=tk.LEFT)
        
        self.frame_sys_eqs = tk.LabelFrame(panel_izq, text="Sistema")
        self.frame_sys_eqs.pack(pady=10, fill=tk.X)
        self.sys_ecuaciones = []
        self.sys_y0 = []
        self.crear_sistema_edo()
        
        tk.Label(panel_izq, text="Método:").pack(anchor=tk.W)
        self.metodo_sys = tk.StringVar(value="rk4")
        tk.Radiobutton(panel_izq, text="Euler", variable=self.metodo_sys, value="euler").pack(anchor=tk.W)
        tk.Radiobutton(panel_izq, text="RK-4", variable=self.metodo_sys, value="rk4").pack(anchor=tk.W)
        
        frame_p = tk.Frame(panel_izq)
        frame_p.pack(pady=10, fill=tk.X)
        tk.Label(frame_p, text="t₀:").grid(row=0, column=0)
        self.sys_t0 = tk.Entry(frame_p, width=8); self.sys_t0.grid(row=0, column=1, padx=5); self.sys_t0.insert(0, "0")
        tk.Label(frame_p, text="t_f:").grid(row=0, column=2)
        self.sys_tf = tk.Entry(frame_p, width=8); self.sys_tf.grid(row=0, column=3, padx=5); self.sys_tf.insert(0, "2")
        tk.Label(frame_p, text="h:").grid(row=1, column=0)
        self.sys_h = tk.Entry(frame_p, width=8); self.sys_h.grid(row=1, column=1, padx=5); self.sys_h.insert(0, "0.1")
        
        frame_btn = tk.Frame(panel_izq)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Ejemplo", command=self.ejemplo_sistema).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_btn, text="Limpiar", command=self.limpiar_sistema).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_btn, text="Resolver", bg='#4CAF50', fg='white', command=self.resolver_sistema).pack(side=tk.LEFT, padx=3)
        
        panel_der = ttk.Frame(frame)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig_sys = Figure(figsize=(6, 3.5), dpi=100)
        self.ax_sys = self.fig_sys.add_subplot(111)
        self.canvas_sys = FigureCanvasTkAgg(self.fig_sys, panel_der)
        self.canvas_sys.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        tk.Label(panel_der, text="Procedimiento:").pack(anchor=tk.W)
        self.resultado_sys = scrolledtext.ScrolledText(panel_der, width=60, height=18, font=('Courier', 9))
        self.resultado_sys.pack(fill=tk.BOTH, expand=True)
    
    def crear_sistema_edo(self):
        for w in self.frame_sys_eqs.winfo_children():
            w.destroy()
        
        n = int(self.sys_n.get()) if self.sys_n.get().isdigit() else 2
        self.sys_ecuaciones = []
        self.sys_y0 = []
        
        tk.Label(self.frame_sys_eqs, text="Variables: t, y1, y2, ...", font=('Arial', 8)).pack(anchor=tk.W)
        
        for i in range(n):
            f = tk.Frame(self.frame_sys_eqs)
            f.pack(fill=tk.X, pady=2)
            tk.Label(f, text=f"dy{i+1}/dt=").pack(side=tk.LEFT)
            eq = tk.Entry(f, width=20)
            eq.pack(side=tk.LEFT, padx=2)
            eq.insert(0, "0")
            self.sys_ecuaciones.append(eq)
            tk.Label(f, text=f"y{i+1}(t₀)=").pack(side=tk.LEFT)
            y0 = tk.Entry(f, width=6)
            y0.pack(side=tk.LEFT, padx=2)
            y0.insert(0, "0")
            self.sys_y0.append(y0)
    
    def ejemplo_sistema(self):
        self.sys_n.set("2")
        self.crear_sistema_edo()
        self.sys_ecuaciones[0].delete(0, tk.END); self.sys_ecuaciones[0].insert(0, "y1 - 0.5*y1*y2")
        self.sys_ecuaciones[1].delete(0, tk.END); self.sys_ecuaciones[1].insert(0, "-y2 + 0.5*y1*y2")
        self.sys_y0[0].delete(0, tk.END); self.sys_y0[0].insert(0, "2")
        self.sys_y0[1].delete(0, tk.END); self.sys_y0[1].insert(0, "1")
        self.sys_t0.delete(0, tk.END); self.sys_t0.insert(0, "0")
        self.sys_tf.delete(0, tk.END); self.sys_tf.insert(0, "10")
        self.sys_h.delete(0, tk.END); self.sys_h.insert(0, "0.1")
    
    def limpiar_sistema(self):
        self.resultado_sys.delete(1.0, tk.END)
        self.ax_sys.clear()
        self.canvas_sys.draw()
    
    def resolver_sistema(self):
        try:
            n = len(self.sys_ecuaciones)
            eqs = [e.get() for e in self.sys_ecuaciones]
            y0 = [float(y.get()) for y in self.sys_y0]
            t0 = float(self.sys_t0.get())
            tf = float(self.sys_tf.get())
            h = float(self.sys_h.get())
            
            var_names = [f"y{i+1}" for i in range(n)]
            f_list = self.ode_sys.parse_system(eqs, 't', var_names)
            
            if self.metodo_sys.get() == "euler":
                t, y, pasos = self.ode_sys.system_euler(f_list, t0, y0, tf, h)
            else:
                t, y, pasos = self.ode_sys.system_rk4(f_list, t0, y0, tf, h)
            
            self.resultado_sys.delete(1.0, tk.END)
            for p in pasos:
                self.resultado_sys.insert(tk.END, p + "\n")
            
            self.ax_sys.clear()
            colores = ['b', 'r', 'g', 'm']
            for i in range(n):
                self.ax_sys.plot(t, y[:, i], f'{colores[i]}-o', markersize=3, label=f'y{i+1}(t)')
            self.ax_sys.set_xlabel('t')
            self.ax_sys.set_ylabel('y')
            self.ax_sys.legend()
            self.ax_sys.grid(True, alpha=0.3)
            self.fig_sys.tight_layout()
            self.canvas_sys.draw()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== MÍNIMOS CUADRADOS ====================
    def crear_pestana_minimos_cuadrados(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Mínimos Cuadrados")
        
        panel_izq = ttk.Frame(frame)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(panel_izq, text="Mínimos Cuadrados", font=('Arial', 14, 'bold')).pack(pady=5)
        
        tk.Label(panel_izq, text="Tipo de ajuste:").pack(anchor=tk.W)
        self.tipo_mc = tk.StringVar(value="linear")
        for txt, val in [("Lineal: y = a₀ + a₁x", "linear"),
                         ("Exponencial: y = a·e^(bx)", "exp"),
                         ("Potencial: y = a·x^b", "power")]:
            tk.Radiobutton(panel_izq, text=txt, variable=self.tipo_mc, value=val).pack(anchor=tk.W)
        
        tk.Label(panel_izq, text="\nDatos (separados por coma):").pack(anchor=tk.W)
        tk.Label(panel_izq, text="x:").pack(anchor=tk.W)
        self.mc_x = tk.Entry(panel_izq, width=35)
        self.mc_x.pack(fill=tk.X)
        self.mc_x.insert(0, "1, 2, 3, 4, 5")
        
        tk.Label(panel_izq, text="y:").pack(anchor=tk.W)
        self.mc_y = tk.Entry(panel_izq, width=35)
        self.mc_y.pack(fill=tk.X)
        self.mc_y.insert(0, "2.1, 3.9, 6.2, 7.8, 10.1")
        
        frame_btn = tk.Frame(panel_izq)
        frame_btn.pack(pady=15)
        tk.Button(frame_btn, text="Ejemplo", command=self.ejemplo_mc).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_btn, text="Calcular", bg='#4CAF50', fg='white', command=self.resolver_mc).pack(side=tk.LEFT, padx=3)
        
        panel_der = ttk.Frame(frame)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig_mc = Figure(figsize=(6, 4), dpi=100)
        self.ax_mc = self.fig_mc.add_subplot(111)
        self.canvas_mc = FigureCanvasTkAgg(self.fig_mc, panel_der)
        self.canvas_mc.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        tk.Label(panel_der, text="Procedimiento:").pack(anchor=tk.W)
        self.resultado_mc = scrolledtext.ScrolledText(panel_der, width=60, height=15, font=('Courier', 9))
        self.resultado_mc.pack(fill=tk.BOTH, expand=True)
    
    def ejemplo_mc(self):
        tipo = self.tipo_mc.get()
        if tipo == "linear":
            self.mc_x.delete(0, tk.END); self.mc_x.insert(0, "1, 2, 3, 4, 5")
            self.mc_y.delete(0, tk.END); self.mc_y.insert(0, "2.1, 3.9, 6.2, 7.8, 10.1")
        elif tipo == "exp":
            self.mc_x.delete(0, tk.END); self.mc_x.insert(0, "0, 1, 2, 3, 4")
            self.mc_y.delete(0, tk.END); self.mc_y.insert(0, "1.0, 2.7, 7.4, 20.1, 54.6")
        else:
            self.mc_x.delete(0, tk.END); self.mc_x.insert(0, "1, 2, 3, 4, 5")
            self.mc_y.delete(0, tk.END); self.mc_y.insert(0, "1, 4, 9, 16, 25")
    
    def resolver_mc(self):
        try:
            x = np.array([float(v.strip()) for v in self.mc_x.get().split(',')])
            y = np.array([float(v.strip()) for v in self.mc_y.get().split(',')])
            tipo = self.tipo_mc.get()
            
            if tipo == "linear":
                a0, a1, r, pasos = self.least_sq.linear_fit(x, y)
                y_fit = a0 + a1 * x
                titulo = f"y = {a0:.4f} + {a1:.4f}x"
            elif tipo == "exp":
                a, b, r, pasos = self.least_sq.exponential_fit(x, y)
                y_fit = a * np.exp(b * x)
                titulo = f"y = {a:.4f}·e^({b:.4f}x)"
            else:
                a, b, r, pasos = self.least_sq.power_fit(x, y)
                y_fit = a * x**b
                titulo = f"y = {a:.4f}·x^{b:.4f}"
            
            self.resultado_mc.delete(1.0, tk.END)
            for p in pasos:
                self.resultado_mc.insert(tk.END, p + "\n")
            
            self.ax_mc.clear()
            self.ax_mc.scatter(x, y, c='blue', label='Datos', s=50)
            x_plot = np.linspace(min(x), max(x), 100)
            if tipo == "linear":
                y_plot = a0 + a1 * x_plot
            elif tipo == "exp":
                y_plot = a * np.exp(b * x_plot)
            else:
                y_plot = a * x_plot**b
            self.ax_mc.plot(x_plot, y_plot, 'r-', label='Ajuste', linewidth=2)
            self.ax_mc.set_xlabel('x')
            self.ax_mc.set_ylabel('y')
            self.ax_mc.set_title(titulo)
            self.ax_mc.legend()
            self.ax_mc.grid(True, alpha=0.3)
            self.fig_mc.tight_layout()
            self.canvas_mc.draw()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = AplicacionMetodosNumericos(root)
    root.mainloop()


if __name__ == "__main__":
    main()
