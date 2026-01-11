"""
GUI para Métodos de Derivación Numérica
ESCOM - IPN
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from derivacion_methods import DerivacionNumerica, ExtrapolacionRichardson


class DerivacionWindow:
    """Ventana para derivación numérica (2, 3 y 5 puntos)."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Derivación Numérica")
        self.parent.geometry("1100x700")
        
        self.bg_color = "#f5f5f5"
        self.btn_color = "#3498db"
        self.parent.configure(bg=self.bg_color)
        
        self.solver = DerivacionNumerica()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="DERIVACIÓN NUMÉRICA (2, 3 y 5 PUNTOS)",
                 font=("Arial", 16, "bold"), fg="#2c3e50", bg=self.bg_color).pack(pady=10)
        
        # Entrada
        input_frame = tk.LabelFrame(main_frame, text=" Parámetros ", bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=10)
        
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row1, text="f(x) =", bg=self.bg_color).pack(side=tk.LEFT)
        self.func_entry = tk.Entry(row1, width=50)
        self.func_entry.pack(side=tk.LEFT, padx=10)
        self.func_entry.insert(0, "sin(x)")
        
        row2 = tk.Frame(input_frame, bg=self.bg_color)
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        for txt, default, width in [("x0:", "0", 10), ("h:", "0.1", 10), ("n:", "10", 8)]:
            tk.Label(row2, text=txt, bg=self.bg_color).pack(side=tk.LEFT, padx=(10, 0))
            entry = tk.Entry(row2, width=width)
            entry.pack(side=tk.LEFT, padx=5)
            entry.insert(0, default)
            setattr(self, f"{txt[:-1]}_entry" if txt != "n:" else "n_entry", entry)
        
        # Renombrar correctamente
        self.x0_entry = self.x0_entry
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Calcular", command=self.calcular,
                  bg=self.btn_color, fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar,
                  bg="#95a5a6", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.parent.destroy,
                  bg="#e74c3c", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        
        # Tabla
        table_frame = tk.LabelFrame(main_frame, text=" Tabla de Derivadas ", bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        cols = ('i', 'xi', 'f(xi)', 'd2', 'd3', 'd5', 'real', 'error')
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=10)
        
        headers = ['i', 'xᵢ', 'f(xᵢ)', "f'(2pts)", "f'(3pts)", "f'(5pts)", 'Real', 'Error%']
        for col, h in zip(cols, headers):
            self.tree.heading(col, text=h)
            self.tree.column(col, width=100 if col != 'i' else 50, anchor=tk.CENTER)
        
        scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Procedimiento
        tk.Label(main_frame, text="Procedimiento:", bg=self.bg_color).pack(anchor=tk.W)
        self.proc_text = scrolledtext.ScrolledText(main_frame, height=8, font=("Courier", 9))
        self.proc_text.pack(fill=tk.BOTH, expand=True)
    
    def calcular(self):
        try:
            self.solver.set_funcion(self.func_entry.get().strip())
            resultados, pasos = self.solver.derivacion_tabla(
                float(self.x0_entry.get()),
                float(self.h_entry.get()),
                int(self.n_entry.get())
            )
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for r in resultados:
                vals = [r['i'], f"{r['xi']:.4f}", f"{r['f(xi)']:.6f}"]
                for key in ['d2', 'd3', 'd5']:
                    vals.append(f"{r[key]:.6f}" if r[key] else "---")
                vals.append(f"{r['real']:.6f}")
                vals.append(f"{r['error']:.4f}%" if r['error'] else "---")
                self.tree.insert('', tk.END, values=vals)
            
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def limpiar(self):
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, "sin(x)")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.proc_text.delete(1.0, tk.END)


class RichardsonWindow:
    """Ventana para Extrapolación de Richardson."""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Extrapolación de Richardson")
        self.parent.geometry("900x600")
        
        self.bg_color = "#f5f5f5"
        self.parent.configure(bg=self.bg_color)
        self.solver = ExtrapolacionRichardson()
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="EXTRAPOLACIÓN DE RICHARDSON",
                 font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Entrada
        input_frame = tk.LabelFrame(main_frame, text=" Parámetros ", bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=10)
        
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(row1, text="f(x) =", bg=self.bg_color).pack(side=tk.LEFT)
        self.func_entry = tk.Entry(row1, width=40)
        self.func_entry.pack(side=tk.LEFT, padx=10)
        self.func_entry.insert(0, "x * exp(x)")
        
        row2 = tk.Frame(input_frame, bg=self.bg_color)
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row2, text="x:", bg=self.bg_color).pack(side=tk.LEFT)
        self.x_entry = tk.Entry(row2, width=10)
        self.x_entry.pack(side=tk.LEFT, padx=5)
        self.x_entry.insert(0, "1")
        
        tk.Label(row2, text="h:", bg=self.bg_color).pack(side=tk.LEFT, padx=(20, 0))
        self.h_entry = tk.Entry(row2, width=10)
        self.h_entry.pack(side=tk.LEFT, padx=5)
        self.h_entry.insert(0, "0.4")
        
        tk.Label(row2, text="Niveles:", bg=self.bg_color).pack(side=tk.LEFT, padx=(20, 0))
        self.n_entry = tk.Entry(row2, width=8)
        self.n_entry.pack(side=tk.LEFT, padx=5)
        self.n_entry.insert(0, "4")
        
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
            self.solver.set_funcion(self.func_entry.get().strip())
            R, resultado, pasos = self.solver.calcular(
                float(self.x_entry.get()),
                float(self.h_entry.get()),
                int(self.n_entry.get())
            )
            
            self.result_label.config(text=f"f'(x) ≈ {resultado:.12f}")
            self.proc_text.delete(1.0, tk.END)
            self.proc_text.insert(tk.END, "\n".join(pasos))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DerivacionWindow(root)
    root.mainloop()
