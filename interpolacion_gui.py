"""
GUI para Métodos de Interpolación
ESCOM - IPN
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from interpolacion_methods import (DiferenciasDivididas, NewtonGregory, 
                                    MetodoNeville, PolinomioTaylor)


class DiferenciasDivididasWindow:
    """Ventana para Diferencias Divididas de Newton."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Diferencias Divididas de Newton")
        self.parent.geometry("950x700")
        
        self.bg_color = "#f5f5f5"
        self.parent.configure(bg=self.bg_color)
        self.solver = DiferenciasDivididas()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="DIFERENCIAS DIVIDIDAS DE NEWTON",
                 font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Modo de entrada
        mode_frame = tk.LabelFrame(main_frame, text=" Modo de Entrada ", bg=self.bg_color)
        mode_frame.pack(fill=tk.X, pady=5)
        
        self.modo_var = tk.StringVar(value="manual")
        tk.Radiobutton(mode_frame, text="Datos manuales", variable=self.modo_var,
                       value="manual", bg=self.bg_color, command=self.cambiar_modo).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="Desde función", variable=self.modo_var,
                       value="funcion", bg=self.bg_color, command=self.cambiar_modo).pack(side=tk.LEFT, padx=10)
        
        # Frame función (inicialmente oculto)
        self.func_frame = tk.Frame(main_frame, bg=self.bg_color)
        tk.Label(self.func_frame, text="f(x) =", bg=self.bg_color).pack(side=tk.LEFT)
        self.func_entry = tk.Entry(self.func_frame, width=40)
        self.func_entry.pack(side=tk.LEFT, padx=10)
        self.func_entry.insert(0, "ln(x)")
        
        # Entrada de datos
        input_frame = tk.LabelFrame(main_frame, text=" Datos ", bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=5)
        
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row1, text="X (separados por coma):", bg=self.bg_color).pack(side=tk.LEFT)
        self.x_entry = tk.Entry(row1, width=50)
        self.x_entry.pack(side=tk.LEFT, padx=10)
        self.x_entry.insert(0, "1, 2, 3, 4, 5")
        
        self.y_row = tk.Frame(input_frame, bg=self.bg_color)
        self.y_row.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(self.y_row, text="Y (separados por coma):", bg=self.bg_color).pack(side=tk.LEFT)
        self.y_entry = tk.Entry(self.y_row, width=50)
        self.y_entry.pack(side=tk.LEFT, padx=10)
        self.y_entry.insert(0, "0, 0.693, 1.099, 1.386, 1.609")
        
        # Evaluación
        eval_frame = tk.Frame(input_frame, bg=self.bg_color)
        eval_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(eval_frame, text="Evaluar en x =", bg=self.bg_color).pack(side=tk.LEFT)
        self.eval_entry = tk.Entry(eval_frame, width=10)
        self.eval_entry.pack(side=tk.LEFT, padx=5)
        self.eval_entry.insert(0, "2.5")
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Calcular", command=self.calcular,
                  bg="#3498db", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Evaluar", command=self.evaluar,
                  bg="#27ae60", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar,
                  bg="#95a5a6", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.parent.destroy,
                  bg="#e74c3c", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        
        # Resultado
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 12, "bold"),
                                      bg=self.bg_color, fg="#27ae60")
        self.result_label.pack(pady=5)
        
        # Procedimiento
        self.proc_text = scrolledtext.ScrolledText(main_frame, height=22, font=("Courier", 9))
        self.proc_text.pack(fill=tk.BOTH, expand=True)
    
    def cambiar_modo(self):
        if self.modo_var.get() == "funcion":
            self.func_frame.pack(fill=tk.X, pady=5, after=self.parent.winfo_children()[0].winfo_children()[1])
            self.y_row.pack_forget()
        else:
            self.func_frame.pack_forget()
            self.y_row.pack(fill=tk.X, padx=10, pady=5)
    
    def calcular(self):
        try:
            x_str = self.x_entry.get().strip()
            x_datos = [float(x.strip()) for x in x_str.split(',')]
            
            if self.modo_var.get() == "funcion":
                import sympy as sp
                x_sym = sp.symbols('x')
                funcion = self.func_entry.get().replace('ln', 'log')
                expr = sp.sympify(funcion)
                f_func = sp.lambdify(x_sym, expr, modules=['math'])
                y_datos = [f_func(x) for x in x_datos]
                self.solver.f_func = f_func
            else:
                y_str = self.y_entry.get().strip()
                y_datos = [float(y.strip()) for y in y_str.split(',')]
                self.solver.f_func = None
            
            if len(x_datos) != len(y_datos):
                messagebox.showerror("Error", "X e Y deben tener la misma cantidad de elementos")
                return
            
            matriz, polinomio, pasos = self.solver.calcular(x_datos, y_datos, self.solver.f_func)
            
            self.result_label.config(text=f"Polinomio calculado exitosamente")
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def evaluar(self):
        try:
            x_val = float(self.eval_entry.get())
            resultado, real, pasos = self.solver.evaluar(x_val)
            
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
            if real is not None:
                self.result_label.config(text=f"P({x_val}) = {resultado:.8f}, Real = {real:.8f}")
            else:
                self.result_label.config(text=f"P({x_val}) = {resultado:.8f}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def limpiar(self):
        self.result_label.config(text="")
        self.proc_text.delete(1.0, tk.END)


class NewtonGregoryWindow:
    """Ventana para Newton-Gregory (equiespaciado)."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Newton-Gregory (Equiespaciado)")
        self.parent.geometry("900x650")
        
        self.bg_color = "#f5f5f5"
        self.parent.configure(bg=self.bg_color)
        self.solver = NewtonGregory()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="NEWTON-GREGORY (DIFERENCIAS FINITAS)",
                 font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Entrada
        input_frame = tk.LabelFrame(main_frame, text=" Datos Equiespaciados ", bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=10)
        
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row1, text="X (separados por coma):", bg=self.bg_color).pack(side=tk.LEFT)
        self.x_entry = tk.Entry(row1, width=50)
        self.x_entry.pack(side=tk.LEFT, padx=10)
        self.x_entry.insert(0, "0, 0.5, 1, 1.5, 2")
        
        row2 = tk.Frame(input_frame, bg=self.bg_color)
        row2.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row2, text="Y (separados por coma):", bg=self.bg_color).pack(side=tk.LEFT)
        self.y_entry = tk.Entry(row2, width=50)
        self.y_entry.pack(side=tk.LEFT, padx=10)
        self.y_entry.insert(0, "1, 1.649, 2.718, 4.482, 7.389")
        
        row3 = tk.Frame(input_frame, bg=self.bg_color)
        row3.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row3, text="Evaluar en x =", bg=self.bg_color).pack(side=tk.LEFT)
        self.eval_entry = tk.Entry(row3, width=10)
        self.eval_entry.pack(side=tk.LEFT, padx=5)
        self.eval_entry.insert(0, "0.75")
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Calcular", command=self.calcular,
                  bg="#9b59b6", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.parent.destroy,
                  bg="#e74c3c", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        
        # Resultado
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 12, "bold"),
                                      bg=self.bg_color, fg="#27ae60")
        self.result_label.pack(pady=5)
        
        # Procedimiento
        self.proc_text = scrolledtext.ScrolledText(main_frame, height=20, font=("Courier", 9))
        self.proc_text.pack(fill=tk.BOTH, expand=True)
    
    def calcular(self):
        try:
            x_datos = [float(x.strip()) for x in self.x_entry.get().split(',')]
            y_datos = [float(y.strip()) for y in self.y_entry.get().split(',')]
            x_val = float(self.eval_entry.get())
            
            matriz, polinomio, pasos = self.solver.calcular(x_datos, y_datos)
            resultado, real, eval_pasos = self.solver.evaluar(x_val)
            
            self.result_label.config(text=f"P({x_val}) = {resultado:.8f}")
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos + eval_pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


class NevilleWindow:
    """Ventana para método de Neville."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Método de Neville")
        self.parent.geometry("900x600")
        
        self.bg_color = "#f5f5f5"
        self.parent.configure(bg=self.bg_color)
        self.solver = MetodoNeville()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="MÉTODO DE NEVILLE",
                 font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Entrada
        input_frame = tk.LabelFrame(main_frame, text=" Datos ", bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=10)
        
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row1, text="X:", bg=self.bg_color).pack(side=tk.LEFT)
        self.x_entry = tk.Entry(row1, width=50)
        self.x_entry.pack(side=tk.LEFT, padx=10)
        self.x_entry.insert(0, "1, 2, 3, 4")
        
        row2 = tk.Frame(input_frame, bg=self.bg_color)
        row2.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row2, text="Y:", bg=self.bg_color).pack(side=tk.LEFT)
        self.y_entry = tk.Entry(row2, width=50)
        self.y_entry.pack(side=tk.LEFT, padx=10)
        self.y_entry.insert(0, "0, 0.693, 1.099, 1.386")
        
        row3 = tk.Frame(input_frame, bg=self.bg_color)
        row3.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row3, text="x a interpolar:", bg=self.bg_color).pack(side=tk.LEFT)
        self.eval_entry = tk.Entry(row3, width=10)
        self.eval_entry.pack(side=tk.LEFT, padx=5)
        self.eval_entry.insert(0, "2.5")
        
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
        self.proc_text = scrolledtext.ScrolledText(main_frame, height=18, font=("Courier", 9))
        self.proc_text.pack(fill=tk.BOTH, expand=True)
    
    def calcular(self):
        try:
            x_datos = [float(x.strip()) for x in self.x_entry.get().split(',')]
            y_datos = [float(y.strip()) for y in self.y_entry.get().split(',')]
            x_val = float(self.eval_entry.get())
            
            resultado, Q, pasos = self.solver.calcular(x_datos, y_datos, x_val)
            
            self.result_label.config(text=f"P({x_val}) ≈ {resultado:.10f}")
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


class TaylorWindow:
    """Ventana para Polinomio de Taylor."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Polinomio de Taylor")
        self.parent.geometry("800x550")
        
        self.bg_color = "#f5f5f5"
        self.parent.configure(bg=self.bg_color)
        self.solver = PolinomioTaylor()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="POLINOMIO DE TAYLOR",
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
        
        tk.Label(row2, text="Centro x₀:", bg=self.bg_color).pack(side=tk.LEFT)
        self.x0_entry = tk.Entry(row2, width=10)
        self.x0_entry.pack(side=tk.LEFT, padx=5)
        self.x0_entry.insert(0, "0")
        
        tk.Label(row2, text="Grado n:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.n_entry = tk.Entry(row2, width=8)
        self.n_entry.pack(side=tk.LEFT, padx=5)
        self.n_entry.insert(0, "5")
        
        tk.Label(row2, text="Evaluar en x:", bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 0))
        self.eval_entry = tk.Entry(row2, width=10)
        self.eval_entry.pack(side=tk.LEFT, padx=5)
        self.eval_entry.insert(0, "0.5")
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Calcular", command=self.calcular,
                  bg="#1abc9c", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.parent.destroy,
                  bg="#e74c3c", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        
        # Resultado
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 12, "bold"),
                                      bg=self.bg_color, fg="#27ae60")
        self.result_label.pack(pady=5)
        
        # Procedimiento
        self.proc_text = scrolledtext.ScrolledText(main_frame, height=18, font=("Courier", 9))
        self.proc_text.pack(fill=tk.BOTH, expand=True)
    
    def calcular(self):
        try:
            funcion = self.func_entry.get().strip()
            x0 = float(self.x0_entry.get())
            n = int(self.n_entry.get())
            x_eval = float(self.eval_entry.get())
            
            polinomio, resultado, pasos = self.solver.calcular(funcion, x0, n, x_eval)
            
            if resultado is not None:
                self.result_label.config(text=f"T_{n}({x_eval}) = {resultado:.8f}")
            
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DiferenciasDivididasWindow(root)
    root.mainloop()
