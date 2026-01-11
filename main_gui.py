"""
Métodos Numéricos - Interfaz Gráfica Principal
ESCOM - IPN
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
from ode_systems import ODESystemSolver

# Importar módulos de raíces
import biseccion, falsa_posicion, secante, newton, punto_fijo, muller

# Importar GUIs adicionales
import derivacion_gui, integracion_gui, interpolacion_gui


class AplicacionMetodosNumericos:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos - ESCOM IPN")
        self.root.geometry("1350x850")
        
        self.linear = LinearSystemsSolver()
        self.least_sq = LeastSquares()
        self.ode_basic = ODEBasicMethods()
        self.ode_adv = ODEAdvancedMethods()
        self.ode_sys = ODESystemSolver()
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.crear_pestana_gauss()
        self.crear_pestana_factorizacion()
        self.crear_pestana_edo()
        self.crear_pestana_sistemas()
        self.crear_pestana_minimos_cuadrados()
        self.crear_pestana_raices()
        self.crear_pestana_derivacion()
        self.crear_pestana_integracion()
        self.crear_pestana_interpolacion()
    
    def crear_pestana_gauss(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Eliminación Gaussiana")
        
        panel_izq = ttk.Frame(frame)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(panel_izq, text="Eliminación Gaussiana", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.metodo_gauss = tk.StringVar(value="partial")
        for txt, val in [("Pivoteo Parcial", "partial"), ("Pivoteo Escalado", "scaled"), ("Pivoteo Total", "total")]:
            tk.Radiobutton(panel_izq, text=txt, variable=self.metodo_gauss, value=val).pack(anchor=tk.W)
        
        frame_n = tk.Frame(panel_izq)
        frame_n.pack(pady=10)
        tk.Label(frame_n, text="n:").pack(side=tk.LEFT)
        self.gauss_n = tk.StringVar(value="3")
        tk.Spinbox(frame_n, from_=2, to=8, width=5, textvariable=self.gauss_n).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_n, text="Crear", command=self.crear_matriz_gauss).pack(side=tk.LEFT)
        
        self.frame_matriz_gauss = tk.LabelFrame(panel_izq, text="[A|b]")
        self.frame_matriz_gauss.pack(pady=10)
        self.entradas_gauss = []
        self.entradas_b_gauss = []
        self.crear_matriz_gauss()
        
        frame_btn = tk.Frame(panel_izq)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Ejemplo", command=self.ejemplo_gauss).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_btn, text="Resolver", bg='#4CAF50', fg='white', command=self.resolver_gauss).pack(side=tk.LEFT, padx=3)
        
        panel_der = ttk.Frame(frame)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.resultado_gauss = scrolledtext.ScrolledText(panel_der, width=70, height=45, font=('Courier', 9))
        self.resultado_gauss.pack(fill=tk.BOTH, expand=True)
    
    def crear_matriz_gauss(self):
        for w in self.frame_matriz_gauss.winfo_children(): w.destroy()
        n = int(self.gauss_n.get()) if self.gauss_n.get().isdigit() else 3
        self.entradas_gauss, self.entradas_b_gauss = [], []
        for i in range(n):
            fila, f = [], tk.Frame(self.frame_matriz_gauss)
            f.pack()
            for j in range(n):
                e = tk.Entry(f, width=7, justify='center')
                e.pack(side=tk.LEFT, padx=1)
                e.insert(0, "0")
                fila.append(e)
            tk.Label(f, text="|").pack(side=tk.LEFT)
            eb = tk.Entry(f, width=7, justify='center')
            eb.pack(side=tk.LEFT, padx=1)
            eb.insert(0, "0")
            self.entradas_b_gauss.append(eb)
            self.entradas_gauss.append(fila)
    
    def ejemplo_gauss(self):
        self.gauss_n.set("3")
        self.crear_matriz_gauss()
        A, b = [[2, -1, 1], [3, 3, 9], [3, 3, 5]], [2, -1, 4]
        for i in range(3):
            for j in range(3):
                self.entradas_gauss[i][j].delete(0, tk.END)
                self.entradas_gauss[i][j].insert(0, str(A[i][j]))
            self.entradas_b_gauss[i].delete(0, tk.END)
            self.entradas_b_gauss[i].insert(0, str(b[i]))
    
    def resolver_gauss(self):
        try:
            n = len(self.entradas_gauss)
            A = np.array([[float(self.entradas_gauss[i][j].get()) for j in range(n)] for i in range(n)])
            b = np.array([float(self.entradas_b_gauss[i].get()) for i in range(n)])
            metodo = self.metodo_gauss.get()
            x, pasos = getattr(self.linear, f"{metodo}_pivoting")(A, b)
            self.resultado_gauss.delete(1.0, tk.END)
            self.resultado_gauss.insert(tk.END, "\n".join(pasos))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def crear_pestana_factorizacion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Factorización")
        
        panel_izq = ttk.Frame(frame)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(panel_izq, text="Factorización", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.tipo_fact = tk.StringVar(value="lu")
        for txt, val in [("LU", "lu"), ("PLU", "plu"), ("Cholesky", "cholesky"), ("LDLᵀ", "ldlt")]:
            tk.Radiobutton(panel_izq, text=txt, variable=self.tipo_fact, value=val).pack(anchor=tk.W)
        
        self.resolver_sistema_var = tk.BooleanVar(value=True)
        tk.Checkbutton(panel_izq, text="Resolver Ax=b", variable=self.resolver_sistema_var).pack(anchor=tk.W)
        
        frame_n = tk.Frame(panel_izq)
        frame_n.pack(pady=10)
        tk.Label(frame_n, text="n:").pack(side=tk.LEFT)
        self.fact_n = tk.StringVar(value="3")
        tk.Spinbox(frame_n, from_=2, to=8, width=5, textvariable=self.fact_n).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_n, text="Crear", command=self.crear_matriz_fact).pack(side=tk.LEFT)
        
        self.frame_matriz_fact = tk.LabelFrame(panel_izq, text="[A|b]")
        self.frame_matriz_fact.pack(pady=10)
        self.entradas_fact, self.entradas_b_fact = [], []
        self.crear_matriz_fact()
        
        # --- CAMBIO AQUI: Frame para botones Ejemplo y Resolver ---
        frame_btn = tk.Frame(panel_izq)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Ejemplo", command=self.ejemplo_fact).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Resolver", bg='#2196F3', fg='white', command=self.resolver_fact).pack(side=tk.LEFT, padx=5)
        # ----------------------------------------------------------
        
        panel_der = ttk.Frame(frame)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.resultado_fact = scrolledtext.ScrolledText(panel_der, width=70, height=45, font=('Courier', 9))
        self.resultado_fact.pack(fill=tk.BOTH, expand=True)
    
    def crear_matriz_fact(self):
        for w in self.frame_matriz_fact.winfo_children(): w.destroy()
        n = int(self.fact_n.get()) if self.fact_n.get().isdigit() else 3
        self.entradas_fact, self.entradas_b_fact = [], []
        for i in range(n):
            fila, f = [], tk.Frame(self.frame_matriz_fact)
            f.pack()
            for j in range(n):
                e = tk.Entry(f, width=7, justify='center')
                e.pack(side=tk.LEFT, padx=1)
                e.insert(0, "0")
                fila.append(e)
            tk.Label(f, text="|").pack(side=tk.LEFT)
            eb = tk.Entry(f, width=7, justify='center')
            eb.pack(side=tk.LEFT, padx=1)
            eb.insert(0, "0")
            self.entradas_b_fact.append(eb)
            self.entradas_fact.append(fila)
    
    def ejemplo_fact(self):
        """Genera un ejemplo de matriz simétrica definida positiva (4, -1, 0...)."""
        self.fact_n.set("3")
        self.crear_matriz_fact()
        
        # Matriz A (Simétrica Definida Positiva para que funcione con Cholesky)
        A = [
            [4, -1, 0],
            [-1, 4, -1],
            [0, -1, 4]
        ]
        # Vector b
        b = [2, 6, 2]
        
        for i in range(3):
            for j in range(3):
                self.entradas_fact[i][j].delete(0, tk.END)
                self.entradas_fact[i][j].insert(0, str(A[i][j]))
            self.entradas_b_fact[i].delete(0, tk.END)
            self.entradas_b_fact[i].insert(0, str(b[i]))
    
    def resolver_fact(self):
        try:
            # Obtener datos de la interfaz
            n = len(self.entradas_fact)
            A = np.array([[float(self.entradas_fact[i][j].get()) for j in range(n)] for i in range(n)])
            b = np.array([float(self.entradas_b_fact[i].get()) for i in range(n)])
            tipo = self.tipo_fact.get()
            resolver = self.resolver_sistema_var.get()
            
            pasos_totales = []
            
            # Ejecutar lógica según el método seleccionado
            if tipo == "lu":
                # 1. Factorización
                L, U, pasos = self.linear.lu_factorization(A)
                pasos_totales.extend(pasos)
                # 2. Solución (si se requiere)
                if resolver:
                    x, pasos_solve = self.linear.lu_solve(L, U, b)
                    pasos_totales.extend(pasos_solve)
                    
            elif tipo == "plu":
                # 1. Factorización
                P, L, U, pasos = self.linear.plu_factorization(A)
                pasos_totales.extend(pasos)
                # 2. Solución
                if resolver:
                    x, pasos_solve = self.linear.plu_solve(P, L, U, b)
                    pasos_totales.extend(pasos_solve)
            
            elif tipo == "cholesky":
                # 1. Factorización
                L, pasos = self.linear.cholesky_factorization(A)
                pasos_totales.extend(pasos)
                # La clase base no tiene implementado resolver para Cholesky
                if resolver:
                    pasos_totales.append("\nNota: La resolución Ax=b para Cholesky no está implementada en la librería base.")
            
            elif tipo == "ldlt":
                # 1. Factorización
                L, D, pasos = self.linear.ldlt_factorization(A)
                pasos_totales.extend(pasos)
                # La clase base no tiene implementado resolver para LDLt
                if resolver:
                    pasos_totales.append("\nNota: La resolución Ax=b para LDLT no está implementada en la librería base.")

            # Mostrar resultados en el área de texto
            self.resultado_fact.delete(1.0, tk.END)
            self.resultado_fact.insert(tk.END, "\n".join(pasos_totales))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def crear_pestana_edo(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="EDOs")
        
        panel_izq = ttk.Frame(frame)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(panel_izq, text="dy/dt = f(t, y):").pack(anchor=tk.W)
        self.edo_eq = tk.Entry(panel_izq, width=25)
        self.edo_eq.pack(fill=tk.X, pady=3)
        self.edo_eq.insert(0, "y - t**2 + 1")
        
        params = tk.Frame(panel_izq)
        params.pack(pady=5)
        for i, (txt, val) in enumerate([("t₀:", "0"), ("y₀:", "0.5"), ("t_fin:", "2"), ("h:", "0.2")]):
            tk.Label(params, text=txt).grid(row=i//2, column=(i%2)*2)
            e = tk.Entry(params, width=8)
            e.grid(row=i//2, column=(i%2)*2+1, padx=3)
            e.insert(0, val)
            setattr(self, f"edo_{txt.replace('₀','0').replace(':','').replace('_','')}", e)
        
        self.edo_metodo = tk.StringVar(value="rk4")
        for txt, val in [("Euler", "euler"), ("RK2", "rk2"), ("RK4", "rk4"), ("RKF45", "rkf45")]:
            tk.Radiobutton(panel_izq, text=txt, variable=self.edo_metodo, value=val).pack(anchor=tk.W)
        
        tk.Button(panel_izq, text="Resolver", bg='#FF9800', fg='white', command=self.resolver_edo).pack(pady=15)
        
        panel_der = ttk.Frame(frame)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig_edo = Figure(figsize=(6, 3.5), dpi=100)
        self.ax_edo = self.fig_edo.add_subplot(111)
        self.canvas_edo = FigureCanvasTkAgg(self.fig_edo, panel_der)
        self.canvas_edo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.resultado_edo = scrolledtext.ScrolledText(panel_der, height=18, font=('Courier', 9))
        self.resultado_edo.pack(fill=tk.BOTH, expand=True)
    
    def resolver_edo(self):
        try:
            eq = self.edo_eq.get()
            t0, y0 = float(self.edo_t0.get()), float(self.edo_y0.get())
            t_end, h = float(self.edo_tfin.get()), float(self.edo_h.get())
            f = self.ode_basic.parse_equation(eq)
            metodo = self.edo_metodo.get()
            
            if metodo in ["euler", "rk2", "rk4"]:
                t, y, pasos = getattr(self.ode_basic, metodo)(f, t0, y0, t_end, h)
            else:
                t, y, pasos = self.ode_adv.rkf45(f, t0, y0, t_end, h)
            
            self.resultado_edo.delete(1.0, tk.END)
            self.resultado_edo.insert(tk.END, "\n".join(pasos))
            
            self.ax_edo.clear()
            self.ax_edo.plot(t, y, 'b-o', markersize=4)
            self.ax_edo.grid(True, alpha=0.3)
            self.canvas_edo.draw()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def crear_pestana_sistemas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Sistemas EDO")
        
        panel_izq = ttk.Frame(frame)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(panel_izq, text="Ecuaciones (una/línea):").pack(anchor=tk.W)
        self.sys_eqs = tk.Text(panel_izq, width=25, height=3)
        self.sys_eqs.pack(fill=tk.X, pady=3)
        self.sys_eqs.insert(tk.END, "y2\n-y1")
        
        tk.Label(panel_izq, text="Variables:").pack(anchor=tk.W)
        self.sys_vars = tk.Entry(panel_izq, width=20)
        self.sys_vars.pack(fill=tk.X)
        self.sys_vars.insert(0, "y1, y2")
        
        tk.Label(panel_izq, text="y₀:").pack(anchor=tk.W)
        self.sys_y0 = tk.Entry(panel_izq, width=20)
        self.sys_y0.pack(fill=tk.X)
        self.sys_y0.insert(0, "0, 1")
        
        for txt, val in [("t₀:", "0"), ("t_fin:", "10"), ("h:", "0.1")]:
            tk.Label(panel_izq, text=txt).pack(anchor=tk.W)
            e = tk.Entry(panel_izq, width=10)
            e.pack()
            e.insert(0, val)
            setattr(self, f"sys_{txt.replace('₀','0').replace(':','').replace('_','')}", e)
        
        tk.Button(panel_izq, text="Resolver (RK4)", bg='#9C27B0', fg='white', command=self.resolver_sistema).pack(pady=15)
        
        panel_der = ttk.Frame(frame)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig_sys = Figure(figsize=(6, 3.5), dpi=100)
        self.ax_sys = self.fig_sys.add_subplot(111)
        self.canvas_sys = FigureCanvasTkAgg(self.fig_sys, panel_der)
        self.canvas_sys.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.resultado_sys = scrolledtext.ScrolledText(panel_der, height=15, font=('Courier', 9))
        self.resultado_sys.pack(fill=tk.BOTH, expand=True)
    
    def resolver_sistema(self):
        try:
            eqs = [e.strip() for e in self.sys_eqs.get(1.0, tk.END).strip().split('\n') if e.strip()]
            vars_list = [v.strip() for v in self.sys_vars.get().split(',')]
            y0 = [float(v.strip()) for v in self.sys_y0.get().split(',')]
            t0, t_end, h = float(self.sys_t0.get()), float(self.sys_tfin.get()), float(self.sys_h.get())
            
            f_list = self.ode_sys.parse_system(eqs, 't', vars_list)
            t, y, pasos = self.ode_sys.system_rk4(f_list, t0, y0, t_end, h)
            
            self.resultado_sys.delete(1.0, tk.END)
            self.resultado_sys.insert(tk.END, "\n".join(pasos))
            
            self.ax_sys.clear()
            for i in range(len(y0)):
                self.ax_sys.plot(t, y[:, i], '-o', markersize=2, label=f'y{i+1}')
            self.ax_sys.legend()
            self.ax_sys.grid(True, alpha=0.3)
            self.canvas_sys.draw()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def crear_pestana_minimos_cuadrados(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Mínimos Cuadrados")
        
        panel_izq = ttk.Frame(frame)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.tipo_mc = tk.StringVar(value="linear")
        for txt, val in [("Lineal", "linear"), ("Exponencial", "exp"), ("Potencial", "power")]:
            tk.Radiobutton(panel_izq, text=txt, variable=self.tipo_mc, value=val).pack(anchor=tk.W)
        
        tk.Label(panel_izq, text="X:").pack(anchor=tk.W)
        self.mc_x = tk.Entry(panel_izq, width=30)
        self.mc_x.pack(fill=tk.X)
        self.mc_x.insert(0, "1, 2, 3, 4, 5")
        
        tk.Label(panel_izq, text="Y:").pack(anchor=tk.W)
        self.mc_y = tk.Entry(panel_izq, width=30)
        self.mc_y.pack(fill=tk.X)
        self.mc_y.insert(0, "2.1, 3.9, 6.2, 7.8, 10.1")
        
        tk.Button(panel_izq, text="Calcular", bg='#4CAF50', fg='white', command=self.resolver_mc).pack(pady=15)
        
        panel_der = ttk.Frame(frame)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig_mc = Figure(figsize=(6, 4), dpi=100)
        self.ax_mc = self.fig_mc.add_subplot(111)
        self.canvas_mc = FigureCanvasTkAgg(self.fig_mc, panel_der)
        self.canvas_mc.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.resultado_mc = scrolledtext.ScrolledText(panel_der, height=12, font=('Courier', 9))
        self.resultado_mc.pack(fill=tk.BOTH, expand=True)
    
    def resolver_mc(self):
        try:
            x = np.array([float(v.strip()) for v in self.mc_x.get().split(',')])
            y = np.array([float(v.strip()) for v in self.mc_y.get().split(',')])
            tipo = self.tipo_mc.get()
            
            if tipo == "linear":
                a0, a1, r, pasos = self.least_sq.linear_fit(x, y)
                y_fit = a0 + a1 * x
            elif tipo == "exp":
                a, b, r, pasos = self.least_sq.exponential_fit(x, y)
                y_fit = a * np.exp(b * x)
            else:
                a, b, r, pasos = self.least_sq.power_fit(x, y)
                y_fit = a * x**b
            
            self.resultado_mc.delete(1.0, tk.END)
            self.resultado_mc.insert(tk.END, "\n".join(pasos))
            
            self.ax_mc.clear()
            self.ax_mc.scatter(x, y, c='blue', s=50, label='Datos')
            x_plot = np.linspace(min(x), max(x), 100)
            if tipo == "linear": y_plot = a0 + a1 * x_plot
            elif tipo == "exp": y_plot = a * np.exp(b * x_plot)
            else: y_plot = a * x_plot**b
            self.ax_mc.plot(x_plot, y_plot, 'r-', linewidth=2, label='Ajuste')
            self.ax_mc.legend()
            self.ax_mc.grid(True, alpha=0.3)
            self.canvas_mc.draw()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def crear_pestana_raices(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Raíces")
        
        panel = tk.Frame(frame)
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(panel, text="Solución de f(x)=0", font=('Arial', 16, 'bold')).pack(pady=20)
        
        btn_frame = tk.Frame(panel)
        btn_frame.pack()
        
        botones = [
            ("Bisección", lambda: biseccion.BiseccionWindow(tk.Toplevel(self.root))),
            ("Falsa Posición", lambda: falsa_posicion.FalsaPosicionWindow(tk.Toplevel(self.root))),
            ("Secante", lambda: secante.SecanteWindow(tk.Toplevel(self.root))),
            ("Newton-Raphson", lambda: newton.NewtonWindow(tk.Toplevel(self.root))),
            ("Punto Fijo", lambda: punto_fijo.PuntoFijoWindow(tk.Toplevel(self.root))),
            ("Müller", lambda: muller.MullerWindow(tk.Toplevel(self.root)))
        ]
        
        for i, (txt, cmd) in enumerate(botones):
            tk.Button(btn_frame, text=txt, command=cmd, width=18, height=2,
                     bg="#4a7abc", fg="white").grid(row=i//2, column=i%2, padx=10, pady=10)
    
    def crear_pestana_derivacion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Derivación")
        
        panel = tk.Frame(frame)
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(panel, text="Derivación Numérica", font=('Arial', 16, 'bold')).pack(pady=20)
        
        btn_frame = tk.Frame(panel)
        btn_frame.pack()
        
        botones = [
            ("Derivación (2,3,5 pts)", lambda: derivacion_gui.DerivacionWindow(tk.Toplevel(self.root))),
            ("Richardson", lambda: derivacion_gui.RichardsonWindow(tk.Toplevel(self.root)))
        ]
        
        for txt, cmd in botones:
            tk.Button(btn_frame, text=txt, command=cmd, width=20, height=2,
                     bg="#3498db", fg="white").pack(pady=10)
    
    def crear_pestana_integracion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Integración")
        
        panel = tk.Frame(frame)
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(panel, text="Integración Numérica", font=('Arial', 16, 'bold')).pack(pady=20)
        
        btn_frame = tk.Frame(panel)
        btn_frame.pack()
        
        botones = [
            ("Trapecio/Simpson", lambda: integracion_gui.IntegracionBasicaWindow(tk.Toplevel(self.root))),
            ("Romberg", lambda: integracion_gui.RombergWindow(tk.Toplevel(self.root))),
            ("Gaussiana", lambda: integracion_gui.GaussianaWindow(tk.Toplevel(self.root))),
            ("Adaptativa", lambda: integracion_gui.AdaptativaWindow(tk.Toplevel(self.root))),
            ("Integral Doble", lambda: integracion_gui.IntegracionDobleWindow(tk.Toplevel(self.root)))
        ]
        
        for i, (txt, cmd) in enumerate(botones):
            tk.Button(btn_frame, text=txt, command=cmd, width=18, height=2,
                     bg="#27ae60", fg="white").grid(row=i//2, column=i%2, padx=10, pady=10)
    
    def crear_pestana_interpolacion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Interpolación")
        
        panel = tk.Frame(frame)
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(panel, text="Interpolación", font=('Arial', 16, 'bold')).pack(pady=20)
        
        btn_frame = tk.Frame(panel)
        btn_frame.pack()
        
        botones = [
            ("Diferencias Divididas", lambda: interpolacion_gui.DiferenciasDivididasWindow(tk.Toplevel(self.root))),
            ("Newton-Gregory", lambda: interpolacion_gui.NewtonGregoryWindow(tk.Toplevel(self.root))),
            ("Neville", lambda: interpolacion_gui.NevilleWindow(tk.Toplevel(self.root))),
            ("Taylor", lambda: interpolacion_gui.TaylorWindow(tk.Toplevel(self.root)))
        ]
        
        for i, (txt, cmd) in enumerate(botones):
            tk.Button(btn_frame, text=txt, command=cmd, width=18, height=2,
                     bg="#9b59b6", fg="white").grid(row=i//2, column=i%2, padx=10, pady=10)


def main():
    root = tk.Tk()
    app = AplicacionMetodosNumericos(root)
    root.mainloop()


if __name__ == "__main__":
    main()
