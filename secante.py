import tkinter as tk
from tkinter import ttk, messagebox
import sol_ecuaciones_var as sol
from tkinter.scrolledtext import ScrolledText
from ui_components import build_param_grid
from ui_base import HoverButtonsMixin

class SecanteWindow(HoverButtonsMixin):
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Método de la Secante")
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
        self.btn_color = "#9b59b6"
        self.btn_hover = "#8e44ad"
        
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
            text="MÉTODO DE LA SECANTE",
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
            {"key": "x0", "label": "x₀ (Primer punto):", "default": "1"},
            {"key": "x1", "label": "x₁ (Segundo punto):", "default": "2"},
            {"key": "error", "label": "Error máximo:", "default": "0.0001"},
            {"key": "iter", "label": "Iteraciones:", "default": "100"},
        ]

        entries = build_param_grid(params_frame, fields, max_fields_per_row=2, label_w=16, entry_w=15)

        self.x0_entry = entries["x0"]
        self.x1_entry = entries["x1"]
        self.error_entry = entries["error"]
        self.iter_entry = entries["iter"]

        for e in [self.x0_entry, self.x1_entry, self.error_entry, self.iter_entry]:
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
        columns = ('iter', 'x0', 'x1', 'x2', 'f(x0)', 'f(x1)', 'error')
        
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
        self.tree.heading('f(x0)', text='f(x₀)')
        self.tree.heading('f(x1)', text='f(x₁)')
        self.tree.heading('error', text='Error')
        
        self.tree.column('iter', width=80, anchor=tk.CENTER)
        self.tree.column('x0', width=100, anchor=tk.CENTER)
        self.tree.column('x1', width=100, anchor=tk.CENTER)
        self.tree.column('x2', width=100, anchor=tk.CENTER)
        self.tree.column('f(x0)', width=120, anchor=tk.CENTER)
        self.tree.column('f(x1)', width=120, anchor=tk.CENTER)
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

        self.proc_text = ScrolledText(proc_frame, height=10, font=("Consolas", 10), wrap="none")
        self.proc_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.proc_text.insert("1.0", "Aquí aparecerán los pasos del método.\n")
        self.proc_text.config(state="disabled")

    
    def setup_events(self):
        """Configurar eventos"""
        # Efecto hover para botones
        for btn in [self.calc_btn, self.clear_btn, self.exit_btn]:
            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(e, b))
    
    def setup_events(self):
        self.bind_hover_buttons([self.calc_btn], normal_bg=self.btn_color, hover_bg=self.btn_hover)

        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg="#7f8c8d"))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg="#95a5a6"))

        self.exit_btn.bind("<Enter>", lambda e: self.exit_btn.config(bg="#c0392b"))
        self.exit_btn.bind("<Leave>", lambda e: self.exit_btn.config(bg="#e74c3c"))

    def render_procedimiento_secante(self, resultados):
        lines = []
        lines.append("iter | x0 | x1 | x2 | f(x0) | f(x1) | error")
        lines.append("-" * 90)
        for r in resultados:
            lines.append(
                f"{r['iteracion']:>4} | "
                f"{r['x0']:.8f} | {r['x1']:.8f} | {r['x2']:.8f} | "
                f"{r['f(x0)']:.3e} | {r['f(x1)']:.3e} | "
                f"{r['error']:.3e}"
            )
        return "\n".join(lines)

    
    def calcular(self):
        """Ejecutar método de la secante"""
        try:
            # Obtener valores de entrada
            funcion = self.func_entry.get().strip()
            x0 = float(self.x0_entry.get())
            x1 = float(self.x1_entry.get())
            error = float(self.error_entry.get())
            iteraciones = int(self.iter_entry.get())
            
            # Validar entrada
            if not funcion:
                messagebox.showerror("Error", "Ingrese una función")
                return
            
            if x0 == x1:
                messagebox.showerror("Error", "x₀ y x₁ no pueden ser iguales")
                return
            
            # Configurar solver
            self.solver.set_funcion(funcion)
            self.solver.a = x0
            self.solver.b = x1
            self.solver.tolerancia = error
            self.solver.max_iter = iteraciones
            
            # Ejecutar método
            raiz, resultados = self.solver.secante()
            
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
                    f"{res['f(x0)']:.6e}",
                    f"{res['f(x1)']:.6e}",
                    f"{res['error']:.6e}"
                ))
            
            texto = self.render_procedimiento_secante(resultados)
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
    
    def limpiar(self):
        """Limpiar todos los campos"""
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, "x**3 - 2*x - 5")
        
        self.x0_entry.delete(0, tk.END)
        self.x0_entry.insert(0, "1")
        
        self.x1_entry.delete(0, tk.END)
        self.x1_entry.insert(0, "2")
        
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
    app = SecanteWindow(root)
    root.mainloop()
    
