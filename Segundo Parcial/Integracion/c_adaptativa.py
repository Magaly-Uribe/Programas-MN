import tkinter as tk
from tkinter import ttk, messagebox
import math

class CuadraturaAdaptativaWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Cuadratura Adaptativa (Simpson Adaptativo)")
        self.parent.geometry("600x500")
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Configurar eventos
        self.setup_events()
    
    def setup_styles(self):
        """Configurar estilos"""
        self.bg_color = "#f5f5f5"
        self.entry_bg = "white"
        self.btn_color = "#3498db"
        self.btn_hover = "#2980b9"
        
        self.parent.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Crear todos los widgets"""
        # Frame principal
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="CUADRATURA ADAPTATIVA (SIMPSON ADAPTATIVO)",
            font=("Arial", 16, "bold"),
            fg="#2c3e50",
            bg=self.bg_color
        )
        title_label.pack()
        
        # Frame de entrada de datos
        input_frame = tk.LabelFrame(
            main_frame,
            text=" Parámetros de Entrada ",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg="#34495e",
            relief=tk.GROOVE,
            bd=2
        )
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Función
        func_frame = tk.Frame(input_frame, bg=self.bg_color)
        func_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            func_frame,
            text="Función f(x):",
            font=("Arial", 11),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.func_entry = tk.Entry(
            func_frame,
            font=("Courier New", 11),
            width=40,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.func_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.func_entry.insert(0, "sin(x)/x")
        
        # Parámetros en grid
        params_frame = tk.Frame(input_frame, bg=self.bg_color)
        params_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Límite inferior
        tk.Label(
            params_frame,
            text="Límite inferior a:",
            font=("Arial", 11),
            bg=self.bg_color
        ).grid(row=0, column=0, padx=(0, 5), pady=10, sticky=tk.W)
        
        self.a_entry = tk.Entry(
            params_frame,
            font=("Arial", 11),
            width=15,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.a_entry.grid(row=0, column=1, padx=(0, 20), pady=10, sticky=tk.W)
        self.a_entry.insert(0, "0.1")
        
        # Límite superior
        tk.Label(
            params_frame,
            text="Límite superior b:",
            font=("Arial", 11),
            bg=self.bg_color
        ).grid(row=0, column=2, padx=(0, 5), pady=10, sticky=tk.W)
        
        self.b_entry = tk.Entry(
            params_frame,
            font=("Arial", 11),
            width=15,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.b_entry.grid(row=0, column=3, padx=(0, 20), pady=10, sticky=tk.W)
        self.b_entry.insert(0, "1")
        
        # Error
        tk.Label(
            params_frame,
            text="Error máximo:",
            font=("Arial", 11),
            bg=self.bg_color
        ).grid(row=1, column=0, padx=(0, 5), pady=10, sticky=tk.W)
        
        self.error_entry = tk.Entry(
            params_frame,
            font=("Arial", 11),
            width=15,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.error_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky=tk.W)
        self.error_entry.insert(0, "0.0001")
        
        # Info frame
        info_frame = tk.Frame(main_frame, bg=self.bg_color)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_text = "Nota: Método adaptativo de Simpson. Se divide automáticamente\n" \
                   "los intervalos hasta alcanzar la precisión deseada."
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 10),
            fg="#7f8c8d",
            bg=self.bg_color,
            justify=tk.LEFT
        )
        info_label.pack()
        
        # Frame de resultado
        result_frame = tk.LabelFrame(
            main_frame,
            text=" Resultado ",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg="#34495e",
            relief=tk.GROOVE,
            bd=2
        )
        result_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Área para mostrar resultados
        self.result_text = tk.Text(
            result_frame,
            height=8,
            font=("Courier New", 10),
            bg="#f8f9fa",
            fg="#2c3e50",
            relief=tk.SOLID,
            bd=1,
            wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar para resultado
        result_scrollbar = ttk.Scrollbar(self.result_text)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        result_scrollbar.configure(command=self.result_text.yview)
        
        # Frame de botones
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botón Calcular
        self.calc_btn = tk.Button(
            button_frame,
            text="Calcular Integral",
            command=self.calcular,
            font=("Arial", 11, "bold"),
            bg=self.btn_color,
            fg="white",
            activebackground=self.btn_hover,
            activeforeground="white",
            width=15,
            height=1,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.calc_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Limpiar
        self.clear_btn = tk.Button(
            button_frame,
            text="Limpiar",
            command=self.limpiar,
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            width=12,
            height=1,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Salir
        self.exit_btn = tk.Button(
            button_frame,
            text="Salir",
            command=self.parent.destroy,
            font=("Arial", 11),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            width=12,
            height=1,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.exit_btn.pack(side=tk.RIGHT)
    
    def setup_events(self):
        """Configurar eventos"""
        # Efecto hover para botones
        for btn in [self.calc_btn, self.clear_btn, self.exit_btn]:
            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(e, b))
    
    def on_enter(self, event, button):
        """Efecto hover al entrar"""
        if button == self.calc_btn:
            button.config(bg=self.btn_hover)
        elif button == self.clear_btn:
            button.config(bg="#7f8c8d")
        elif button == self.exit_btn:
            button.config(bg="#c0392b")
    
    def on_leave(self, event, button):
        """Efecto hover al salir"""
        if button == self.calc_btn:
            button.config(bg=self.btn_color)
        elif button == self.clear_btn:
            button.config(bg="#95a5a6")
        elif button == self.exit_btn:
            button.config(bg="#e74c3c")
    
    def evaluar_funcion(self, x, funcion_str):
        """Evaluar función matemática en punto x"""
        try:
            # Reemplazar funciones matemáticas
            funcion_str = funcion_str.replace('sin', 'math.sin')
            funcion_str = funcion_str.replace('cos', 'math.cos')
            funcion_str = funcion_str.replace('tan', 'math.tan')
            funcion_str = funcion_str.replace('exp', 'math.exp')
            funcion_str = funcion_str.replace('log', 'math.log')
            funcion_str = funcion_str.replace('sqrt', 'math.sqrt')
            
            # Evaluar
            return eval(funcion_str, {"math": math, "x": x})
        except:
            raise ValueError(f"Error al evaluar función en x={x}")
    
    def simpson_simple(self, a, b, funcion_str):
        """Regla de Simpson 1/3 simple"""
        h = (b - a) / 2
        fa = self.evaluar_funcion(a, funcion_str)
        fm = self.evaluar_funcion(a + h, funcion_str)
        fb = self.evaluar_funcion(b, funcion_str)
        
        return (h / 3) * (fa + 4 * fm + fb)
    
    def cuadratura_adaptativa_rec(self, a, b, error_max, funcion_str, nivel=0, nivel_max=20):
        """Método recursivo adaptativo"""
        if nivel > nivel_max:
            return self.simpson_simple(a, b, funcion_str), nivel
        
        # Simpson simple en intervalo completo
        I1 = self.simpson_simple(a, b, funcion_str)
        
        # Simpson en dos subintervalos
        m = (a + b) / 2
        I2_left = self.simpson_simple(a, m, funcion_str)
        I2_right = self.simpson_simple(m, b, funcion_str)
        I2 = I2_left + I2_right
        
        # Estimación del error
        error_est = abs(I2 - I1) / 15
        
        if error_est <= error_max:
            # Corrección de Richardson
            return I2 + (I2 - I1) / 15, nivel
        else:
            # Dividir y conquistar
            left_result, left_nivel = self.cuadratura_adaptativa_rec(
                a, m, error_max/2, funcion_str, nivel+1, nivel_max
            )
            right_result, right_nivel = self.cuadratura_adaptativa_rec(
                m, b, error_max/2, funcion_str, nivel+1, nivel_max
            )
            return left_result + right_result, max(left_nivel, right_nivel)
    
    def calcular(self):
        """Ejecutar cuadratura adaptativa"""
        try:
            # Obtener valores de entrada
            funcion = self.func_entry.get().strip()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            error = float(self.error_entry.get())
            
            # Validar entrada
            if not funcion:
                messagebox.showerror("Error", "Ingrese una función")
                return
            
            if a >= b:
                messagebox.showerror("Error", "a debe ser menor que b")
                return
            
            if error <= 0:
                messagebox.showerror("Error", "El error debe ser mayor que 0")
                return
            
            # Verificar que la función es evaluable
            try:
                test_val = self.evaluar_funcion(a, funcion)
            except Exception as e:
                messagebox.showerror("Error", f"Función inválida: {str(e)}")
                return
            
            # Calcular integral adaptativa
            resultado, niveles = self.cuadratura_adaptativa_rec(a, b, error, funcion)
            
            # Mostrar resultados
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"════════════════════════════════════════\n")
            self.result_text.insert(tk.END, f"RESULTADOS DE LA INTEGRACIÓN\n")
            self.result_text.insert(tk.END, f"════════════════════════════════════════\n\n")
            self.result_text.insert(tk.END, f"Función: f(x) = {funcion}\n")
            self.result_text.insert(tk.END, f"Intervalo: [{a:.4f}, {b:.4f}]\n")
            self.result_text.insert(tk.END, f"Error máximo: {error:.2e}\n\n")
            self.result_text.insert(tk.END, f"════════════════════════════════════════\n")
            self.result_text.insert(tk.END, f"Valor de la integral: {resultado:.10f}\n")
            self.result_text.insert(tk.END, f"Niveles de recursión: {niveles}\n")
            self.result_text.insert(tk.END, f"════════════════════════════════════════\n")
            
            # Colorizar resultado
            self.result_text.tag_add("result", "5.0", "end")
            self.result_text.tag_config("result", foreground="#27ae60", font=("Courier New", 11, "bold"))
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def limpiar(self):
        """Limpiar todos los campos"""
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, "sin(x)/x")
        
        self.a_entry.delete(0, tk.END)
        self.a_entry.insert(0, "0.1")
        
        self.b_entry.delete(0, tk.END)
        self.b_entry.insert(0, "1")
        
        self.error_entry.delete(0, tk.END)
        self.error_entry.insert(0, "0.0001")
        
        self.result_text.delete(1.0, tk.END)

# Para probar individualmente
if __name__ == "__main__":
    root = tk.Tk()
    app = CuadraturaAdaptativaWindow(root)
    root.mainloop()