import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from ui_components import build_param_grid
from ui_base import HoverButtonsMixin
import sol_ecuaciones_var as sol

class NewtonWindow(HoverButtonsMixin):
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Método de Newton-Raphson")
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
        self.btn_color = "#e67e22"
        self.btn_hover = "#d35400"
        
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
            text="MÉTODO DE NEWTON-RAPHSON",
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
        
        # Parámetros (grid consistente)
        params_frame = tk.Frame(input_frame, bg=self.bg_color)
        params_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        fields = [
            {"key": "x0", "label": "Valor inicial x₀:", "default": "1"},
            {"key": "error", "label": "Error máximo:", "default": "1e-6"},
            {"key": "iter", "label": "Iteraciones:", "default": "100"},
        ]

        entries = build_param_grid(params_frame, fields, max_fields_per_row=2)

        self.x0_entry = entries["x0"]
        self.error_entry = entries["error"]
        self.iter_entry = entries["iter"]

        for e in [self.x0_entry, self.error_entry, self.iter_entry]:
            e.config(font=("Arial", 11), bg=self.entry_bg)
        
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
        columns = ('iter', 'x', 'f(x)', "f'(x)", 'x_new', 'error')
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Configurar columnas
        self.tree.heading('iter', text='Iteración')
        self.tree.heading('x', text='x')
        self.tree.heading('f(x)', text='f(x)')
        self.tree.heading("f'(x)", text="f'(x)")
        self.tree.heading('x_new', text='x_nuevo')
        self.tree.heading('error', text='Error')
        
        self.tree.column('iter', width=80, anchor=tk.CENTER)
        self.tree.column('x', width=120, anchor=tk.CENTER)
        self.tree.column('f(x)', width=120, anchor=tk.CENTER)
        self.tree.column("f'(x)", width=120, anchor=tk.CENTER)
        self.tree.column('x_new', width=120, anchor=tk.CENTER)
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
        
        # Frame para procedimiento (opcional)
        proc_frame = tk.LabelFrame(
            main_frame,
            text=" Procedimiento ",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg="#34495e",
            relief=tk.GROOVE,
            bd=2
        )
        proc_frame.pack(fill=tk.BOTH, expand=False, pady=(10, 0))

        self.proc_text = ScrolledText(
            proc_frame,
            height=10,
            font=("Consolas", 10),
            wrap="none"
        )
        self.proc_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.proc_text.insert("1.0", "Aquí aparecerán los pasos del método.\n")
        self.proc_text.config(state="disabled")

    def setup_events(self):
        """Configurar eventos"""
        self.bind_hover_buttons(
            [self.calc_btn],
            normal_bg=self.btn_color,
            hover_bg=self.btn_hover
        )

        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg="#7f8c8d"))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg="#95a5a6"))

        self.exit_btn.bind("<Enter>", lambda e: self.exit_btn.config(bg="#c0392b"))
        self.exit_btn.bind("<Leave>", lambda e: self.exit_btn.config(bg="#e74c3c"))

    def calcular(self):
        """Ejecutar método de Newton-Raphson"""
        try:
            # Obtener valores de entrada
            funcion = self.func_entry.get().strip()
            x0 = float(self.x0_entry.get())
            error = float(self.error_entry.get())
            iteraciones = int(self.iter_entry.get())
            
            # Validar entrada
            if not funcion:
                messagebox.showerror("Error", "Ingrese una función")
                return
            
            # Configurar solver
            self.solver.set_funcion(funcion)
            self.solver.a = x0
            self.solver.tolerancia = error
            self.solver.max_iter = iteraciones
            
            # Ejecutar método
            raiz, resultados = self.solver.newton_raphson()
            
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
                derivada = res["df"]
                
                self.tree.insert('', tk.END, values=(
                    res['iteracion'],
                    f"{res['x']:.6f}",
                    f"{res['f(x)']:.6e}",
                    f"{derivada:.6e}",
                    f"{res['x_new']:.6f}",
                    f"{res['error']:.6e}"
                ))
                
            texto = self.render_procedimiento_newton(resultados)
            self.proc_text.config(state="normal")
            self.proc_text.delete("1.0", "end")
            self.proc_text.insert("1.0", texto)
            self.proc_text.config(state="disabled")

            
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
    
    def render_procedimiento_newton(self, resultados):
        lines = []
        lines.append("iter | x | f(x) | f'(x) | x_new | error")
        lines.append("-" * 90)
        for r in resultados:
            # OJO: ajusta las keys si tu solver usa nombres distintos
            lines.append(
                f"{r['iteracion']:>4} | "
                f"{r['x']:.10f} | {r['f(x)']:.3e} | {r['df']:.3e} | "
                f"{r['x_new']:.10f} | {r['error']:.3e}"
            )
        return "\n".join(lines)

    
    def limpiar(self):
        """Limpiar todos los campos"""
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, "x**3 - 2*x - 5")
        
        self.x0_entry.delete(0, tk.END)
        self.x0_entry.insert(0, "2")
        
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
    app = NewtonWindow(root)
    root.mainloop()
    
