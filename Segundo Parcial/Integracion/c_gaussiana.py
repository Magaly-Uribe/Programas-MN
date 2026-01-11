import tkinter as tk
from tkinter import ttk, messagebox
import math

class CuadraturaGaussianaWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Cuadratura Gaussiana (Polinomios de Legendre)")
        self.parent.geometry("650x550")
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Configurar eventos
        self.setup_events()
        
        # Coeficientes de Gauss-Legendre predefinidos
        self.coeficientes = {
            2: {
                'nodos': [-0.5773502692, 0.5773502692],
                'pesos': [1.0, 1.0]
            },
            3: {
                'nodos': [-0.7745966692, 0.0, 0.7745966692],
                'pesos': [0.5555555556, 0.8888888889, 0.5555555556]
            },
            4: {
                'nodos': [-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116],
                'pesos': [0.3478548451, 0.6521451549, 0.6521451549, 0.3478548451]
            }
        }
    
    def setup_styles(self):
        """Configurar estilos"""
        self.bg_color = "#f5f5f5"
        self.entry_bg = "white"
        self.btn_color = "#9b59b6"
        self.btn_hover = "#8e44ad"
        
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
            text="CUADRATURA GAUSSIANA (POLINOMIOS DE LEGENDRE)",
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
        self.func_entry.insert(0, "exp(-x**2)")
        
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
            width=12,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.a_entry.grid(row=0, column=1, padx=(0, 15), pady=10, sticky=tk.W)
        self.a_entry.insert(0, "-1")
        
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
            width=12,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.b_entry.grid(row=0, column=3, padx=(0, 15), pady=10, sticky=tk.W)
        self.b_entry.insert(0, "1")
        
        # Número de intervalos
        tk.Label(
            params_frame,
            text="N° intervalos (n):",
            font=("Arial", 11),
            bg=self.bg_color
        ).grid(row=1, column=0, padx=(0, 5), pady=10, sticky=tk.W)
        
        self.n_entry = tk.Entry(
            params_frame,
            font=("Arial", 11),
            width=12,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.n_entry.grid(row=1, column=1, padx=(0, 15), pady=10, sticky=tk.W)
        self.n_entry.insert(0, "4")
        
        # Grado del polinomio (ComboBox)
        tk.Label(
            params_frame,
            text="Grado Legendre:",
            font=("Arial", 11),
            bg=self.bg_color
        ).grid(row=1, column=2, padx=(0, 5), pady=10, sticky=tk.W)
        
        self.grado_var = tk.StringVar()
        self.grado_combo = ttk.Combobox(
            params_frame,
            textvariable=self.grado_var,
            values=["2", "3", "4"],
            font=("Arial", 11),
            width=10,
            state="readonly"
        )
        self.grado_combo.grid(row=1, column=3, padx=(0, 15), pady=10, sticky=tk.W)
        self.grado_combo.set("3")
        
        # Info frame
        info_frame = tk.Frame(main_frame, bg=self.bg_color)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_text = "Grados disponibles:\n" \
                   "• Grado 2: 2 puntos de Gauss, exacto para polinomios hasta grado 3\n" \
                   "• Grado 3: 3 puntos de Gauss, exacto para polinomios hasta grado 5\n" \
                   "• Grado 4: 4 puntos de Gauss, exacto para polinomios hasta grado 7"
        
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
            height=10,
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
        
        # Botón Mostrar Puntos
        self.points_btn = tk.Button(
            button_frame,
            text="Ver Puntos",
            command=self.mostrar_puntos,
            font=("Arial", 11),
            bg="#1abc9c",
            fg="white",
            activebackground="#16a085",
            activeforeground="white",
            width=12,
            height=1,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.points_btn.pack(side=tk.LEFT, padx=(0, 10))
        
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
        for btn in [self.calc_btn, self.clear_btn, self.points_btn, self.exit_btn]:
            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(e, b))
    
    def on_enter(self, event, button):
        """Efecto hover al entrar"""
        if button == self.calc_btn:
            button.config(bg=self.btn_hover)
        elif button == self.clear_btn:
            button.config(bg="#7f8c8d")
        elif button == self.points_btn:
            button.config(bg="#16a085")
        elif button == self.exit_btn:
            button.config(bg="#c0392b")
    
    def on_leave(self, event, button):
        """Efecto hover al salir"""
        if button == self.calc_btn:
            button.config(bg=self.btn_color)
        elif button == self.clear_btn:
            button.config(bg="#95a5a6")
        elif button == self.points_btn:
            button.config(bg="#1abc9c")
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
    
    def transformar_punto(self, x, a, b):
        """Transformar punto de [-1,1] a [a,b]"""
        return ((b - a) * x + (a + b)) / 2
    
    def cuadratura_gaussiana(self, a, b, n_intervalos, grado, funcion_str):
        """Aplicar cuadratura gaussiana compuesta"""
        # Obtener coeficientes para el grado seleccionado
        coef = self.coeficientes[grado]
        nodos = coef['nodos']
        pesos = coef['pesos']
        
        # Ancho de cada subintervalo
        h = (b - a) / n_intervalos
        
        resultado_total = 0.0
        
        for i in range(n_intervalos):
            # Extremos del subintervalo
            ai = a + i * h
            bi = ai + h
            
            # Calcular integral en subintervalo
            integral_intervalo = 0.0
            for j in range(grado):
                # Transformar nodo de [-1,1] a [ai, bi]
                x_transformado = self.transformar_punto(nodos[j], ai, bi)
                # Evaluar función y multiplicar por peso
                integral_intervalo += pesos[j] * self.evaluar_funcion(x_transformado, funcion_str)
            
            # Escalar por factor de transformación
            integral_intervalo *= (bi - ai) / 2
            resultado_total += integral_intervalo
        
        return resultado_total
    
    def calcular(self):
        """Ejecutar cuadratura gaussiana"""
        try:
            # Obtener valores de entrada
            funcion = self.func_entry.get().strip()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            n = int(self.n_entry.get())
            grado = int(self.grado_combo.get())
            
            # Validar entrada
            if not funcion:
                messagebox.showerror("Error", "Ingrese una función")
                return
            
            if a >= b:
                messagebox.showerror("Error", "a debe ser menor que b")
                return
            
            if n <= 0:
                messagebox.showerror("Error", "El número de intervalos debe ser positivo")
                return
            
            if grado not in [2, 3, 4]:
                messagebox.showerror("Error", "El grado debe ser 2, 3 o 4")
                return
            
            # Verificar que la función es evaluable
            try:
                test_val = self.evaluar_funcion(a, funcion)
            except Exception as e:
                messagebox.showerror("Error", f"Función inválida: {str(e)}")
                return
            
            # Calcular integral
            resultado = self.cuadratura_gaussiana(a, b, n, grado, funcion)
            
            # Obtener coeficientes para mostrar
            coef = self.coeficientes[grado]
            
            # Mostrar resultados
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"════════════════════════════════════════\n")
            self.result_text.insert(tk.END, f"RESULTADOS GAUSS-LEGENDRE\n")
            self.result_text.insert(tk.END, f"════════════════════════════════════════\n\n")
            self.result_text.insert(tk.END, f"Función: f(x) = {funcion}\n")
            self.result_text.insert(tk.END, f"Intervalo: [{a:.4f}, {b:.4f}]\n")
            self.result_text.insert(tk.END, f"N° subintervalos: {n}\n")
            self.result_text.insert(tk.END, f"Grado polinomio: {grado}\n")
            self.result_text.insert(tk.END, f"N° puntos Gauss: {grado}\n\n")
            self.result_text.insert(tk.END, f"════════════════════════════════════════\n")
            self.result_text.insert(tk.END, f"Valor de la integral: {resultado:.12f}\n")
            self.result_text.insert(tk.END, f"════════════════════════════════════════\n")
            
            # Colorizar resultado
            self.result_text.tag_add("result", "8.0", "end")
            self.result_text.tag_config("result", foreground="#27ae60", font=("Courier New", 11, "bold"))
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def mostrar_puntos(self):
        """Mostrar puntos y pesos de Gauss"""
        try:
            grado = int(self.grado_combo.get())
            coef = self.coeficientes[grado]
            
            puntos_window = tk.Toplevel(self.parent)
            puntos_window.title(f"Puntos y Pesos - Grado {grado}")
            puntos_window.geometry("400x300")
            puntos_window.configure(bg="#f5f5f5")
            
            # Título
            tk.Label(
                puntos_window,
                text=f"PUNTOS Y PESOS DE GAUSS-LEGENDRE (Grado {grado})",
                font=("Arial", 12, "bold"),
                fg="#2c3e50",
                bg="#f5f5f5"
            ).pack(pady=10)
            
            # Frame para tabla
            table_frame = tk.Frame(puntos_window, bg="#f5f5f5")
            table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Encabezados
            headers = ["Punto", "Nodo ξ", "Peso w"]
            for col, header in enumerate(headers):
                tk.Label(
                    table_frame,
                    text=header,
                    font=("Arial", 10, "bold"),
                    fg="#34495e",
                    bg="#f5f5f5",
                    width=15
                ).grid(row=0, column=col, padx=2, pady=5)
            
            # Datos
            for i in range(grado):
                tk.Label(
                    table_frame,
                    text=f"{i+1}",
                    font=("Arial", 10),
                    fg="#2c3e50",
                    bg="#f5f5f5",
                    width=15
                ).grid(row=i+1, column=0, padx=2, pady=3)
                
                tk.Label(
                    table_frame,
                    text=f"{coef['nodos'][i]:.10f}",
                    font=("Courier New", 9),
                    fg="#2980b9",
                    bg="#f5f5f5",
                    width=15
                ).grid(row=i+1, column=1, padx=2, pady=3)
                
                tk.Label(
                    table_frame,
                    text=f"{coef['pesos'][i]:.10f}",
                    font=("Courier New", 9),
                    fg="#27ae60",
                    bg="#f5f5f5",
                    width=15
                ).grid(row=i+1, column=2, padx=2, pady=3)
            
            # Botón cerrar
            tk.Button(
                puntos_window,
                text="Cerrar",
                command=puntos_window.destroy,
                font=("Arial", 10),
                bg="#95a5a6",
                fg="white",
                width=10
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar puntos: {str(e)}")
    
    def limpiar(self):
        """Limpiar todos los campos"""
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, "exp(-x**2)")
        
        self.a_entry.delete(0, tk.END)
        self.a_entry.insert(0, "-1")
        
        self.b_entry.delete(0, tk.END)
        self.b_entry.insert(0, "1")
        
        self.n_entry.delete(0, tk.END)
        self.n_entry.insert(0, "4")
        
        self.grado_combo.set("3")
        
        self.result_text.delete(1.0, tk.END)

# Para probar individualmente
if __name__ == "__main__":
    root = tk.Tk()
    app = CuadraturaGaussianaWindow(root)
    root.mainloop()