import tkinter as tk
from controller import CajaRegistradoraController

# Punto de entrada principal de la aplicación
# Este archivo inicializa la interfaz gráfica y el controlador
if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana principal de la aplicación
    app = CajaRegistradoraController(root)  # Inicializar el controlador con la ventana raíz
    root.mainloop()  # Iniciar el bucle principal de la interfaz gráfica
