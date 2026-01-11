"""
GUI para Métodos de Integración Numérica
ESCOM - IPN
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from integracion_methods import (IntegracionNumerica, IntegracionRomberg, 
                                  CuadraturaGaussiana, CuadraturaAdaptativa,
                                  IntegracionDoble)


class IntegracionBasicaWindow:
    """Ventana para métodos básicos de integración (Trapecio, Simpson)."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Integración Numérica")
        self.parent.geometry("900x650")
        
        self.bg_color = "#f5f5f5"
        self.parent.configure(bg=self.bg_color)
        self.solver = IntegracionNumerica()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="INTEGRACIÓN NUMÉRICA",
                 font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Entrada
        input_frame = tk.LabelFrame(main_frame, text=" Parámetros ", bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Función
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row1, text="f(x) =", bg=self.bg_color).pack(side=tk.LEFT)
        self.func_entry = tk.Entry(row1, width=40)
        self.func_entry.pack(side=tk.LEFT, padx=10)
        self.func_entry.insert(0, "sin(x)")
        
        # Límites y n
        row2 = tk.Frame(input_frame, bg=self.bg_color)
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row2, text="a:", bg=self.bg_color).pack(side=tk.LEFT)
        self.a_entry = tk.Entry(row2, width=10)
        self.a_entry.pack(side=tk.LEFT, padx=5)
        self.a_entry.insert(0, "0")
        
        tk.Label(row2, text="b:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.b_entry = tk.Entry(row2, width=10)
        self.b_entry.pack(side=tk.LEFT, padx=5)
        self.b_entry.insert(0, "3.14159")
        
        tk.Label(row2, text="n:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.n_entry = tk.Entry(row2, width=8)
        self.n_entry.pack(side=tk.LEFT, padx=5)
        self.n_entry.insert(0, "10")
        
        # Método
        row3 = tk.Frame(input_frame, bg=self.bg_color)
        row3.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row3, text="Método:", bg=self.bg_color).pack(side=tk.LEFT)
        
        self.metodo_var = tk.StringVar(value="trapecio_simple")
        metodos = [
            ("Trapecio Simple", "trapecio_simple"),
            ("Trapecio Compuesto", "trapecio_compuesto"),
            ("Simpson 1/3 Simple", "simpson_1_3_simple"),
            ("Simpson 1/3 Compuesto", "simpson_1_3_compuesto"),
            ("Simpson 3/8 Simple", "simpson_3_8_simple"),
            ("Simpson 3/8 Compuesto", "simpson_3_8_compuesto"),
        ]
        
        for txt, val in metodos:
            tk.Radiobutton(row3, text=txt, variable=self.metodo_var, 
                          value=val, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Calcular", command=self.calcular,
                  bg="#27ae60", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar,
                  bg="#95a5a6", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.parent.destroy,
                  bg="#e74c3c", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        
        # Resultado
        result_frame = tk.LabelFrame(main_frame, text=" Resultado ", bg=self.bg_color)
        result_frame.pack(fill=tk.X, pady=5)
        
        self.result_label = tk.Label(result_frame, text="", font=("Arial", 14, "bold"),
                                      bg=self.bg_color, fg="#27ae60")
        self.result_label.pack(pady=10)
        
        # Procedimiento
        tk.Label(main_frame, text="Procedimiento:", bg=self.bg_color).pack(anchor=tk.W)
        self.proc_text = scrolledtext.ScrolledText(main_frame, height=15, font=("Courier", 9))
        self.proc_text.pack(fill=tk.BOTH, expand=True)
    
    def calcular(self):
        try:
            funcion = self.func_entry.get().strip()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            n = int(self.n_entry.get())
            metodo = self.metodo_var.get()
            
            self.solver.set_funcion(funcion)
            
            if metodo == "trapecio_simple":
                resultado, pasos = self.solver.trapecio_simple(a, b)
            elif metodo == "trapecio_compuesto":
                resultado, pasos = self.solver.trapecio_compuesto(a, b, n)
            elif metodo == "simpson_1_3_simple":
                resultado, pasos = self.solver.simpson_1_3_simple(a, b)
            elif metodo == "simpson_1_3_compuesto":
                resultado, pasos = self.solver.simpson_1_3_compuesto(a, b, n)
            elif metodo == "simpson_3_8_simple":
                resultado, pasos = self.solver.simpson_3_8_simple(a, b)
            else:
                resultado, pasos = self.solver.simpson_3_8_compuesto(a, b, n)
            
            self.result_label.config(text=f"∫f(x)dx ≈ {resultado:.10f}")
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def limpiar(self):
        self.result_label.config(text="")
        self.proc_text.delete(1.0, tk.END)


class RombergWindow:
    """Ventana para Integración de Romberg."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Integración de Romberg")
        self.parent.geometry("900x600")
        
        self.bg_color = "#f5f5f5"
        self.parent.configure(bg=self.bg_color)
        self.solver = IntegracionRomberg()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="INTEGRACIÓN DE ROMBERG",
                 font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Entrada
        input_frame = tk.LabelFrame(main_frame, text=" Parámetros ", bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=10)
        
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row1, text="f(x) =", bg=self.bg_color).pack(side=tk.LEFT)
        self.func_entry = tk.Entry(row1, width=40)
        self.func_entry.pack(side=tk.LEFT, padx=10)
        self.func_entry.insert(0, "sin(x)")
        
        row2 = tk.Frame(input_frame, bg=self.bg_color)
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        for txt, default in [("a:", "0"), ("b:", "3.14159"), ("Niveles:", "5")]:
            tk.Label(row2, text=txt, bg=self.bg_color).pack(side=tk.LEFT, padx=(10, 0))
            entry = tk.Entry(row2, width=10)
            entry.pack(side=tk.LEFT, padx=5)
            entry.insert(0, default)
            name = txt.replace(":", "").lower()
            setattr(self, f"{name}_entry", entry)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Calcular", command=self.calcular,
                  bg="#e67e22", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.parent.destroy,
                  bg="#e74c3c", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        
        # Resultado
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 14, "bold"),
                                      bg=self.bg_color, fg="#27ae60")
        self.result_label.pack(pady=5)
        
        # Procedimiento
        self.proc_text = scrolledtext.ScrolledText(main_frame, height=20, font=("Courier", 9))
        self.proc_text.pack(fill=tk.BOTH, expand=True)
    
    def calcular(self):
        try:
            self.solver.set_funcion(self.func_entry.get().strip())
            R, resultado, pasos = self.solver.calcular(
                float(self.a_entry.get()),
                float(self.b_entry.get()),
                int(self.niveles_entry.get())
            )
            
            self.result_label.config(text=f"∫f(x)dx ≈ {resultado:.10f}")
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


class GaussianaWindow:
    """Ventana para Cuadratura Gaussiana."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Cuadratura Gaussiana")
        self.parent.geometry("900x600")
        
        self.bg_color = "#f5f5f5"
        self.parent.configure(bg=self.bg_color)
        self.solver = CuadraturaGaussiana()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="CUADRATURA GAUSSIANA",
                 font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Entrada
        input_frame = tk.LabelFrame(main_frame, text=" Parámetros ", bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=10)
        
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row1, text="f(x) =", bg=self.bg_color).pack(side=tk.LEFT)
        self.func_entry = tk.Entry(row1, width=40)
        self.func_entry.pack(side=tk.LEFT, padx=10)
        self.func_entry.insert(0, "exp(-x**2)")
        
        row2 = tk.Frame(input_frame, bg=self.bg_color)
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row2, text="a:", bg=self.bg_color).pack(side=tk.LEFT)
        self.a_entry = tk.Entry(row2, width=10)
        self.a_entry.pack(side=tk.LEFT, padx=5)
        self.a_entry.insert(0, "-1")
        
        tk.Label(row2, text="b:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.b_entry = tk.Entry(row2, width=10)
        self.b_entry.pack(side=tk.LEFT, padx=5)
        self.b_entry.insert(0, "1")
        
        tk.Label(row2, text="Subintervalos:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.n_entry = tk.Entry(row2, width=8)
        self.n_entry.pack(side=tk.LEFT, padx=5)
        self.n_entry.insert(0, "4")
        
        tk.Label(row2, text="Grado:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.grado_combo = ttk.Combobox(row2, values=["2", "3", "4", "5"], width=5)
        self.grado_combo.pack(side=tk.LEFT, padx=5)
        self.grado_combo.set("3")
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Calcular", command=self.calcular,
                  bg="#9b59b6", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.parent.destroy,
                  bg="#e74c3c", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        
        # Resultado
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 14, "bold"),
                                      bg=self.bg_color, fg="#27ae60")
        self.result_label.pack(pady=5)
        
        # Procedimiento
        self.proc_text = scrolledtext.ScrolledText(main_frame, height=18, font=("Courier", 9))
        self.proc_text.pack(fill=tk.BOTH, expand=True)
    
    def calcular(self):
        try:
            self.solver.set_funcion(self.func_entry.get().strip())
            resultado, pasos = self.solver.calcular(
                float(self.a_entry.get()),
                float(self.b_entry.get()),
                int(self.n_entry.get()),
                int(self.grado_combo.get())
            )
            
            self.result_label.config(text=f"∫f(x)dx ≈ {resultado:.10f}")
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


class AdaptativaWindow:
    """Ventana para Cuadratura Adaptativa."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Cuadratura Adaptativa")
        self.parent.geometry("800x550")
        
        self.bg_color = "#f5f5f5"
        self.parent.configure(bg=self.bg_color)
        self.solver = CuadraturaAdaptativa()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="CUADRATURA ADAPTATIVA",
                 font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Entrada
        input_frame = tk.LabelFrame(main_frame, text=" Parámetros ", bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=10)
        
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row1, text="f(x) =", bg=self.bg_color).pack(side=tk.LEFT)
        self.func_entry = tk.Entry(row1, width=40)
        self.func_entry.pack(side=tk.LEFT, padx=10)
        self.func_entry.insert(0, "sin(x)/x")
        
        row2 = tk.Frame(input_frame, bg=self.bg_color)
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row2, text="a:", bg=self.bg_color).pack(side=tk.LEFT)
        self.a_entry = tk.Entry(row2, width=10)
        self.a_entry.pack(side=tk.LEFT, padx=5)
        self.a_entry.insert(0, "0.1")
        
        tk.Label(row2, text="b:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.b_entry = tk.Entry(row2, width=10)
        self.b_entry.pack(side=tk.LEFT, padx=5)
        self.b_entry.insert(0, "1")
        
        tk.Label(row2, text="Tolerancia:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.tol_entry = tk.Entry(row2, width=12)
        self.tol_entry.pack(side=tk.LEFT, padx=5)
        self.tol_entry.insert(0, "0.0001")
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Calcular", command=self.calcular,
                  bg="#3498db", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.parent.destroy,
                  bg="#e74c3c", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        
        # Resultado
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 14, "bold"),
                                      bg=self.bg_color, fg="#27ae60")
        self.result_label.pack(pady=5)
        
        # Procedimiento
        self.proc_text = scrolledtext.ScrolledText(main_frame, height=15, font=("Courier", 9))
        self.proc_text.pack(fill=tk.BOTH, expand=True)
    
    def calcular(self):
        try:
            self.solver.set_funcion(self.func_entry.get().strip())
            resultado, niveles, pasos = self.solver.calcular(
                float(self.a_entry.get()),
                float(self.b_entry.get()),
                float(self.tol_entry.get())
            )
            
            self.result_label.config(text=f"∫f(x)dx ≈ {resultado:.10f}  (Niveles: {niveles})")
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


class IntegracionDobleWindow:
    """Ventana para Integración Doble."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Integración Doble")
        self.parent.geometry("900x600")
        
        self.bg_color = "#f5f5f5"
        self.parent.configure(bg=self.bg_color)
        self.solver = IntegracionDoble()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="INTEGRACIÓN DOBLE",
                 font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Entrada
        input_frame = tk.LabelFrame(main_frame, text=" Parámetros ", bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=10)
        
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row1, text="f(x,y) =", bg=self.bg_color).pack(side=tk.LEFT)
        self.func_entry = tk.Entry(row1, width=40)
        self.func_entry.pack(side=tk.LEFT, padx=10)
        self.func_entry.insert(0, "x**2 + y*x")
        
        row2 = tk.Frame(input_frame, bg=self.bg_color)
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        for txt, default in [("x₀:", "0"), ("x₁:", "2"), ("y₀:", "0"), ("y₁:", "2")]:
            tk.Label(row2, text=txt, bg=self.bg_color).pack(side=tk.LEFT, padx=(10, 0))
            entry = tk.Entry(row2, width=8)
            entry.pack(side=tk.LEFT, padx=3)
            entry.insert(0, default)
            name = txt.replace(":", "").replace("₀", "0").replace("₁", "1")
            setattr(self, f"{name}_entry", entry)
        
        row3 = tk.Frame(input_frame, bg=self.bg_color)
        row3.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row3, text="n:", bg=self.bg_color).pack(side=tk.LEFT)
        self.n_entry = tk.Entry(row3, width=8)
        self.n_entry.pack(side=tk.LEFT, padx=5)
        self.n_entry.insert(0, "4")
        
        tk.Label(row3, text="m:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.m_entry = tk.Entry(row3, width=8)
        self.m_entry.pack(side=tk.LEFT, padx=5)
        self.m_entry.insert(0, "4")
        
        tk.Label(row3, text="Método:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.metodo_var = tk.StringVar(value="simpson")
        tk.Radiobutton(row3, text="Trapecio", variable=self.metodo_var, 
                      value="trapecio", bg=self.bg_color).pack(side=tk.LEFT)
        tk.Radiobutton(row3, text="Simpson", variable=self.metodo_var, 
                      value="simpson", bg=self.bg_color).pack(side=tk.LEFT)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Calcular", command=self.calcular,
                  bg="#16a085", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.parent.destroy,
                  bg="#e74c3c", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        
        # Resultado
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 14, "bold"),
                                      bg=self.bg_color, fg="#27ae60")
        self.result_label.pack(pady=5)
        
        # Procedimiento
        self.proc_text = scrolledtext.ScrolledText(main_frame, height=15, font=("Courier", 9))
        self.proc_text.pack(fill=tk.BOTH, expand=True)
    
    def calcular(self):
        try:
            self.solver.set_funcion(self.func_entry.get().strip())
            
            x0 = float(self.x0_entry.get())
            x1 = float(self.x1_entry.get())
            y0 = float(self.y0_entry.get())
            y1 = float(self.y1_entry.get())
            n = int(self.n_entry.get())
            m = int(self.m_entry.get())
            
            if self.metodo_var.get() == "trapecio":
                resultado, pasos = self.solver.trapecio_doble(x0, x1, y0, y1, n, m)
            else:
                resultado, pasos = self.solver.simpson_doble(x0, x1, y0, y1, n, m)
            
            self.result_label.config(text=f"∬f(x,y)dA ≈ {resultado:.10f}")
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = IntegracionBasicaWindow(root)
    root.mainloop()
