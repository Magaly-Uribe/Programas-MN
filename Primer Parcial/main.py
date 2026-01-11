import tkinter as tk
from tkinter import ttk, messagebox
import biseccion
import falsa_posicion
import secante
import newton
import punto_fijo
import muller

class MetodosNumericosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos")
        self.root.geometry("800x600")
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
    
    def setup_styles(self):
        """Configurar estilos para la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores
        self.bg_color = "#f0f0f0"
        self.btn_color = "#4a7abc"
        self.btn_hover = "#3a6aac"
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Crear los widgets de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="MÉTODOS NUMÉRICOS",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg=self.bg_color
        )
        title_label.pack(pady=(0, 30))
        
        # Subtítulo
        subtitle_label = tk.Label(
            main_frame,
            text="Solución de Ecuaciones de una Variable",
            font=("Arial", 14),
            fg="#7f8c8d",
            bg=self.bg_color
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Frame para botones
        buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
        buttons_frame.pack()
        
        # Lista de métodos con sus funciones
        metodos = [
            ("Bisección", self.abrir_biseccion),
            ("Falsa Posición", self.abrir_falsa_posicion),
            ("Secante", self.abrir_secante),
            ("Newton-Raphson", self.abrir_newton),
            ("Punto Fijo", self.abrir_punto_fijo),
            ("Müller", self.abrir_muller)
        ]
        
        # Crear botones
        for i, (nombre, comando) in enumerate(metodos):
            btn = tk.Button(
                buttons_frame,
                text=nombre,
                command=comando,
                font=("Arial", 12),
                bg=self.btn_color,
                fg="white",
                activebackground=self.btn_hover,
                activeforeground="white",
                width=20,
                height=2,
                cursor="hand2",
                relief=tk.FLAT,
                bd=0
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            
            # Efecto hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.btn_hover))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.btn_color))
        
        # Configurar grid
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        # Botón salir
        salir_btn = tk.Button(
            main_frame,
            text="Salir",
            command=self.root.quit,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            width=15,
            height=2,
            cursor="hand2",
            relief=tk.FLAT
        )
        salir_btn.pack(pady=(40, 0))
        
        # Información del desarrollador
        info_label = tk.Label(
            main_frame,
            text="Desarrollado con Python y Tkinter",
            font=("Arial", 10),
            fg="#95a5a6",
            bg=self.bg_color
        )
        info_label.pack(side=tk.BOTTOM, pady=10)
    
    def abrir_biseccion(self):
        """Abrir ventana de Bisección"""
        biseccion_window = tk.Toplevel(self.root)
        biseccion.BiseccionWindow(biseccion_window)
    
    def abrir_falsa_posicion(self):
        """Abrir ventana de Falsa Posición"""
        falsa_window = tk.Toplevel(self.root)
        falsa_posicion.FalsaPosicionWindow(falsa_window)
    
    def abrir_secante(self):
        """Abrir ventana de Secante"""
        secante_window = tk.Toplevel(self.root)
        secante.SecanteWindow(secante_window)
    
    def abrir_newton(self):
        """Abrir ventana de Newton-Raphson"""
        newton_window = tk.Toplevel(self.root)
        newton.NewtonWindow(newton_window)
    
    def abrir_punto_fijo(self):
        """Abrir ventana de Punto Fijo"""
        punto_fijo_window = tk.Toplevel(self.root)
        punto_fijo.PuntoFijoWindow(punto_fijo_window)
    
    def abrir_muller(self):
        """Abrir ventana de Müller"""
        muller_window = tk.Toplevel(self.root)
        muller.MullerWindow(muller_window)

def main():
    root = tk.Tk()
    app = MetodosNumericosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
