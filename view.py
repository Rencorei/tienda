import tkinter as tk
from tkinter import ttk

class CajaRegistradoraView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.root.title("Caja Registradora - Versión 1.02")
        self.root.geometry("850x600")
        self.root.resizable(False, False)

        # Paleta de colores
        self.color_fondo = "#2C3E50"
        self.color_texto = "#ECF0F1"
        self.color_boton = "#3498DB"
        self.color_boton_hover = "#2980B9"
        self.color_acento = "#E74C3C"
        self.color_acento_hover = "#C0392B"

        self.configurar_estilo()

        # Creación de frames
        self.frame_login = tk.Frame(self.root, bg=self.color_fondo)
        self.frame_menu = tk.Frame(self.root, bg=self.color_fondo)
        self.frame_ventas = tk.Frame(self.root, bg=self.color_fondo)
        self.frame_inventario = tk.Frame(self.root, bg=self.color_fondo)

        # Variable para el ComboBox
        self.producto_seleccionado = tk.StringVar()

        # Configurar cada uno de los frames
        self.configurar_frame_login()
        self.configurar_frame_menu()
        self.configurar_frame_ventas()
        self.configurar_frame_inventario()

        self.mostrar_frame(self.frame_login)

    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TButton', font=('Arial', 11, 'bold'),
                        background=self.color_boton, foreground='white')
        style.configure('TEntry', font=('Arial', 10), padding=5)
        style.configure('TCombobox', font=('Arial', 10), padding=5)
        style.configure('TLabel', font=('Arial', 10),
                        background=self.color_fondo, foreground=self.color_texto)
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'),
                        background=self.color_fondo, foreground=self.color_texto)

    def mostrar_frame(self, frame):
        for f in (self.frame_login, self.frame_menu, self.frame_ventas, self.frame_inventario):
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    # ---------- Frame Login ----------
    def configurar_frame_login(self):
        frame_container = tk.Frame(self.frame_login, bg=self.color_fondo, padx=40, pady=40)
        frame_container.place(relx=0.5, rely=0.5, anchor='center')

        logo_label = tk.Label(frame_container, text="CAJA REGISTRADORA",
                            font=("Arial", 24, "bold"),
                            bg=self.color_fondo, fg=self.color_texto)
        logo_label.pack(pady=(0, 30))

        titulo = tk.Label(frame_container, text="Inicio de Sesión",
                        font=("Arial", 18, "bold"),
                        bg=self.color_fondo, fg=self.color_texto)
        titulo.pack(pady=(0, 20))

        frame_inputs = tk.Frame(frame_container, bg=self.color_fondo, padx=20, pady=20,
                                highlightbackground=self.color_texto, highlightthickness=1)
        frame_inputs.pack(fill="both", expand=True)

        lbl_usuario = tk.Label(frame_inputs, text="Usuario:",
                            font=("Arial", 12),
                            bg=self.color_fondo, fg=self.color_texto)
        lbl_usuario.pack(anchor='w', pady=(0, 5))
        self.entry_usuario = ttk.Entry(frame_inputs, width=30, font=("Arial", 12))
        self.entry_usuario.pack(pady=(0, 15), ipady=3)

        lbl_password = tk.Label(frame_inputs, text="Contraseña:",
                                font=("Arial", 12),
                                bg=self.color_fondo, fg=self.color_texto)
        lbl_password.pack(anchor='w', pady=(0, 5))
        self.entry_password = ttk.Entry(frame_inputs, width=30, font=("Arial", 12), show="*")
        self.entry_password.pack(pady=(0, 15), ipady=3)

        btn_ingresar = tk.Button(frame_inputs, text="Ingresar",
                                width=15, height=1,
                                bg=self.color_boton, fg="white",
                                activebackground=self.color_boton_hover,
                                font=("Arial", 12, "bold"),
                                command=self.controller.validar_login)
        btn_ingresar.pack(pady=10)

        version_label = tk.Label(frame_container, text="Versión 1.02",
                                font=("Arial", 8),
                                bg=self.color_fondo, fg=self.color_texto)
        version_label.pack(pady=(20, 0))

    # ---------- Frame Menú Principal ----------
    def configurar_frame_menu(self):
        frame_container = tk.Frame(self.frame_menu, bg=self.color_fondo)
        frame_container.place(relx=0.5, rely=0.5, anchor='center')

        titulo = tk.Label(frame_container, text="CAJA REGISTRADORA",
                            font=("Arial", 22, "bold"),
                            bg=self.color_fondo, fg=self.color_texto)
        titulo.pack(pady=(0, 40))

        btn_ventas = tk.Button(frame_container, text="Módulo de Ventas",
                                width=25, height=2,
                                bg=self.color_boton, fg="white",
                                activebackground=self.color_boton_hover,
                                font=("Arial", 14, "bold"),
                                command=lambda: self.mostrar_frame(self.frame_ventas))
        btn_ventas.pack(pady=10)

        btn_inventario = tk.Button(frame_container, text="Módulo de Inventario",
                                    width=25, height=2,
                                    bg=self.color_boton, fg="white",
                                    activebackground=self.color_boton_hover,
                                    font=("Arial", 14, "bold"),
                                    command=lambda: self.mostrar_frame(self.frame_inventario))
        btn_inventario.pack(pady=10)

        btn_about = tk.Button(frame_container, text="Acerca de",
                                width=25, height=2,
                                bg=self.color_boton, fg="white",
                                activebackground=self.color_boton_hover,
                                font=("Arial", 14, "bold"),
                                command=self.controller.mostrar_about)
        btn_about.pack(pady=10)

        btn_cerrar_sesion = tk.Button(frame_container, text="Cerrar Sesión",
                                    width=25, height=2,
                                    bg=self.color_acento, fg="white",
                                    activebackground=self.color_acento_hover,
                                    font=("Arial", 14, "bold"),
                                    command=self.controller.cerrar_sesion)
        btn_cerrar_sesion.pack(pady=30)

    # ---------- Frame Ventas ----------
    def configurar_frame_ventas(self):
        main_container = tk.Frame(self.frame_ventas, bg=self.color_fondo, padx=20, pady=20)
        main_container.pack(fill="both", expand=True)

        titulo = tk.Label(main_container, text="MÓDULO DE VENTAS",
                            font=("Arial", 18, "bold"),
                            bg=self.color_fondo, fg=self.color_texto)
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Contenedor izquierdo (formulario)
        frame_izquierdo = tk.Frame(main_container, bg=self.color_fondo, padx=15, pady=15,
                                    highlightbackground=self.color_texto, highlightthickness=1)
        frame_izquierdo.grid(row=1, column=0, padx=(0, 10), sticky="nsew")

        tk.Label(frame_izquierdo, text="Agregar Producto",
                font=("Arial", 14, "bold"),
                bg=self.color_fondo, fg=self.color_texto).pack(pady=(0, 15))

        tk.Label(frame_izquierdo, text="Seleccione Producto:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(anchor='w', pady=(0, 5))

        self.combo_productos = ttk.Combobox(frame_izquierdo,
                                            values=[p["nombre"] for p in self.controller.model.productos_disponibles],
                                            font=("Arial", 12),
                                            state="readonly",
                                            textvariable=self.producto_seleccionado,
                                            width=28)
        self.combo_productos.pack(fill="x", pady=(0, 10))
        self.combo_productos.bind("<<ComboboxSelected>>", self.controller.actualizar_precio)

        tk.Label(frame_izquierdo, text="Precio:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(anchor='w', pady=(0, 5))
        self.entry_precio = ttk.Entry(frame_izquierdo, width=30, font=("Arial", 12), state="readonly")
        self.entry_precio.pack(fill="x", pady=(0, 10))

        tk.Label(frame_izquierdo, text="Cantidad:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(anchor='w', pady=(0, 5))
        self.entry_cantidad = ttk.Entry(frame_izquierdo, width=30, font=("Arial", 12))
        self.entry_cantidad.pack(fill="x", pady=(0, 15))
        self.entry_cantidad.insert(0, "1")

        btn_agregar = tk.Button(frame_izquierdo, text="Agregar Producto",
                                width=15, height=1,
                                bg=self.color_boton, fg="white",
                                activebackground=self.color_boton_hover,
                                font=("Arial", 12, "bold"),
                                command=self.controller.agregar_producto)
        btn_agregar.pack(pady=10)

        # Contenedor derecho (detalle de venta)
        frame_derecho = tk.Frame(main_container, bg=self.color_fondo, padx=15, pady=15,
                                highlightbackground=self.color_texto, highlightthickness=1)
        frame_derecho.grid(row=1, column=1, padx=(10, 0), sticky="nsew")

        tk.Label(frame_derecho, text="Detalle de Venta",
                font=("Arial", 14, "bold"),
                bg=self.color_fondo, fg=self.color_texto).pack(pady=(0, 15))

        self.lista_ventas = tk.Listbox(frame_derecho, width=50, height=10,
                                    font=("Arial", 12),
                                    bg=self.color_texto, fg=self.color_fondo,
                                    selectbackground=self.color_boton)
        self.lista_ventas.pack(fill="both", expand=True, pady=(0, 10))

        btn_eliminar = tk.Button(frame_derecho, text="Eliminar Producto",
                                width=15, height=1,
                                bg=self.color_acento, fg="white",
                                activebackground=self.color_acento_hover,
                                font=("Arial", 12, "bold"),
                                command=self.controller.eliminar_producto)
        btn_eliminar.pack(pady=5)

        self.label_total = tk.Label(frame_derecho, text="Total: S/.0.00",
                                    font=("Arial", 16, "bold"),
                                    bg=self.color_fondo, fg=self.color_texto)
        self.label_total.pack(pady=10)

        btn_finalizar = tk.Button(frame_derecho, text="Finalizar Venta",
                                width=15, height=1,
                                bg=self.color_acento, fg="white",
                                activebackground=self.color_acento_hover,
                                font=("Arial", 12, "bold"),
                                command=self.controller.finalizar_venta)
        btn_finalizar.pack(pady=10)

        btn_volver_menu = tk.Button(main_container, text="Volver al Menú",
                                    width=15, height=1,
                                    bg=self.color_boton, fg="white",
                                    activebackground=self.color_boton_hover,
                                    font=("Arial", 12, "bold"),
                                    command=lambda: self.mostrar_frame(self.frame_menu))
        btn_volver_menu.grid(row=2, column=0, columnspan=3, pady=20)

        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(1, weight=1)

    # ---------- Frame Inventario ----------
    def configurar_frame_inventario(self):
        main_container = tk.Frame(self.frame_inventario, bg=self.color_fondo, padx=20, pady=20)
        main_container.pack(fill="both", expand=True)

        titulo = tk.Label(main_container, text="MÓDULO DE INVENTARIO",
                            font=("Arial", 18, "bold"),
                            bg=self.color_fondo, fg=self.color_texto)
        titulo.pack(pady=(0, 20))

        frame_contenido = tk.Frame(main_container, bg=self.color_fondo, padx=20, pady=20,
                                highlightbackground=self.color_texto, highlightthickness=1)
        frame_contenido.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame_contenido, text="🔧",
                font=("Arial", 36),
                bg=self.color_fondo, fg=self.color_texto).pack(pady=20)
        tk.Label(frame_contenido, text="Sección en Construcción",
                font=("Arial", 18, "bold"),
                bg=self.color_fondo, fg=self.color_texto).pack()
        tk.Label(frame_contenido, text="Estamos trabajando para implementar esta funcionalidad.",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(pady=10)
        tk.Label(frame_contenido, text="Por favor, vuelve pronto para ver las actualizaciones.",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(pady=5)

        btn_volver_menu = tk.Button(main_container, text="Volver al Menú",
                                    width=15, height=1,
                                    bg=self.color_boton, fg="white",
                                    activebackground=self.color_boton_hover,
                                    font=("Arial", 12, "bold"),
                                    command=lambda: self.mostrar_frame(self.frame_menu))
        btn_volver_menu.pack(pady=20)
