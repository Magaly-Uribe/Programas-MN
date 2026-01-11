import tkinter as tk
from tkinter import ttk, messagebox
import sol_ecuaciones_var as sol

class MullerWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Método de Müller")
        self.parent.geometry("900x700")
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear solver
        self.solver = sol.SolEcuaciones()
        
        # Crear interfaz
        self.create_widgets()
        
        # Configurar eventos
        self.setup_events()
    
    def setup_styles(self):
        """Configurar estilos"""
        self.bg_color = "#f5f5f5"
        self.entry_bg = "white"
        self.btn_color = "#e74c3c"
        self.btn_hover = "#c0392b"
        
        self.parent.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Crear todos los widgets"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="MÉTODO DE MÜLLER",
            font=("Arial", 18, "bold"),
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
            font=("Arial", 11),
            width=40,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.func_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.func_entry.insert(0, "x**3 - 2*x - 5")
        
        # Parámetros en línea
        params_frame = tk.Frame(input_frame, bg=self.bg_color)
        params_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # x0
        tk.Label(
            params_frame,
            text="x₀:",
            font=("Arial", 11),
            bg=self.bg_color
        ).grid(row=0, column=0, padx=(0, 5), pady=5, sticky=tk.W)
        
        self.x0_entry = tk.Entry(
            params_frame,
            font=("Arial", 11),
            width=12,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.x0_entry.grid(row=0, column=1, padx=(0, 15), pady=5, sticky=tk.W)
        self.x0_entry.insert(0, "1")
        
        # x1
        tk.Label(
            params_frame,
            text="x₁:",
            font=("Arial", 11),
            bg=self.bg_color
        ).grid(row=0, column=2, padx=(0, 5), pady=5, sticky=tk.W)
        
        self.x1_entry = tk.Entry(
            params_frame,
            font=("Arial", 11),
            width=12,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.x1_entry.grid(row=0, column=3, padx=(0, 15), pady=5, sticky=tk.W)
        self.x1_entry.insert(0, "2")
        
        # x2
        tk.Label(
            params_frame,
            text="x₂:",
            font=("Arial", 11),
            bg=self.bg_color
        ).grid(row=0, column=4, padx=(0, 5), pady=5, sticky=tk.W)
        
        self.x2_entry = tk.Entry(
            params_frame,
            font=("Arial", 11),
            width=12,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.x2_entry.grid(row=0, column=5, padx=(0, 15), pady=5, sticky=tk.W)
        self.x2_entry.insert(0, "3")
        
        # Error
        tk.Label(
            params_frame,
            text="Error máximo:",
            font=("Arial", 11),
            bg=self.bg_color
        ).grid(row=0, column=6, padx=(0, 5), pady=5, sticky=tk.W)
        
        self.error_entry = tk.Entry(
            params_frame,
            font=("Arial", 11),
            width=12,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.error_entry.grid(row=0, column=7, padx=(0, 15), pady=5, sticky=tk.W)
        self.error_entry.insert(0, "0.0001")
        
        # Iteraciones
        tk.Label(
            params_frame,
            text="Iteraciones:",
            font=("Arial", 11),
            bg=self.bg_color
        ).grid(row=0, column=8, padx=(0, 5), pady=5, sticky=tk.W)
        
        self.iter_entry = tk.Entry(
            params_frame,
            font=("Arial", 11),
            width=12,
            bg=self.entry_bg,
            relief=tk.SOLID,
            bd=1
        )
        self.iter_entry.grid(row=0, column=9, padx=(0, 0), pady=5, sticky=tk.W)
        self.iter_entry.insert(0, "100")
        
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
        
        tk.Label(
            result_frame,
            text="Raíz aproximada:",
            font=("Arial", 11, "bold"),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=(10, 5), pady=10)
        
        self.result_label = tk.Label(
            result_frame,
            text="",
            font=("Arial", 11),
            bg=self.bg_color,
            fg="#e74c3c"
        )
        self.result_label.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        # Frame de botones
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botón Calcular
        self.calc_btn = tk.Button(
            button_frame,
            text="Calcular",
            command=self.calcular,
            font=("Arial", 11, "bold"),
            bg=self.btn_color,
            fg="white",
            activebackground=self.btn_hover,
            activeforeground="white",
            width=12,
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
            bg="#34495e",
            fg="white",
            activebackground="#2c3e50",
            activeforeground="white",
            width=12,
            height=1,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.exit_btn.pack(side=tk.RIGHT)
        
        # Frame para la tabla de resultados
        table_frame = tk.LabelFrame(
            main_frame,
            text=" Tabla de Iteraciones ",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg="#34495e",
            relief=tk.GROOVE,
            bd=2
        )
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview (tabla)
        columns = ('iter', 'x0', 'x1', 'x2', 'x3', 'error')
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Configurar columnas
        self.tree.heading('iter', text='Iteración')
        self.tree.heading('x0', text='x₀')
        self.tree.heading('x1', text='x₁')
        self.tree.heading('x2', text='x₂')
        self.tree.heading('x3', text='x₃')
        self.tree.heading('error', text='Error')
        
        self.tree.column('iter', width=80, anchor=tk.CENTER)
        self.tree.column('x0', width=100, anchor=tk.CENTER)
        self.tree.column('x1', width=100, anchor=tk.CENTER)
        self.tree.column('x2', width=100, anchor=tk.CENTER)
        self.tree.column('x3', width=100, anchor=tk.CENTER)
        self.tree.column('error', width=120, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
    
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
            button.config(bg="#2c3e50")
    
    def on_leave(self, event, button):
        """Efecto hover al salir"""
        if button == self.calc_btn:
            button.config(bg=self.btn_color)
        elif button == self.clear_btn:
           button.config(bg="#95a5a6")
        elif button == self.exit_btn:
            button.config(bg="#34495e")
    
    def calcular(self):
        """Ejecutar método de Müller"""
        try:
            # Obtener valores de entrada
            funcion = self.func_entry.get().strip()
            x0 = float(self.x0_entry.get())
            x1 = float(self.x1_entry.get())
            x2 = float(self.x2_entry.get())
            error = float(self.error_entry.get())
            iteraciones = int(self.iter_entry.get())
            
            # Validar entrada
            if not funcion:
                messagebox.showerror("Error", "Ingrese una función")
                return
            
            # Verificar que los puntos sean distintos
            if x0 == x1 or x0 == x2 or x1 == x2:
                messagebox.showerror("Error", "Los puntos x₀, x₁ y x₂ deben ser distintos")
                return
            
            # Configurar solver
            self.solver.set_funcion(funcion)
            self.solver.tolerancia = error
            self.solver.max_iter = iteraciones
            
            # Ejecutar método
            raiz, resultados = self.solver.muller(x0, x1, x2)
            
            # Mostrar resultado
            self.result_label.config(
                text=f"{raiz:.10f}",
                fg="#27ae60"
            )
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Llenar tabla
            for res in resultados:
                self.tree.insert('', tk.END, values=(
                    res['iteracion'],
                    f"{res['x0']:.6f}",
                    f"{res['x1']:.6f}",
                    f"{res['x2']:.6f}",
                    f"{res['x3']:.6f}",
                    f"{res['error']:.6e}"
                ))
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Éxito",
                f"Raíz encontrada: {raiz:.10f}\n"
                f"Error final: {resultados[-1]['error']:.2e}\n"
                f"Iteraciones: {len(resultados)}"
            )
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def limpiar(self):
        """Limpiar todos los campos"""
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, "x**3 - 2*x - 5")
        
        self.x0_entry.delete(0, tk.END)
        self.x0_entry.insert(0, "1")
        
        self.x1_entry.delete(0, tk.END)
        self.x1_entry.insert(0, "2")
        
        self.x2_entry.delete(0, tk.END)
        self.x2_entry.insert(0, "3")
        
        self.error_entry.delete(0, tk.END)
        self.error_entry.insert(0, "0.0001")
        
        self.iter_entry.delete(0, tk.END)
        self.iter_entry.insert(0, "100")
        
        self.result_label.config(text="", fg="#e74c3c")
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

# Para probar individualmente
if __name__ == "__main__":
    root = tk.Tk()
    app = MullerWindow(root)
    root.mainloop()
    