import tkinter as tk
from tkinter import ttk

# Clase principal que implementa la vista en el patrón MVC
# Gestiona toda la interfaz gráfica de usuario y la presentación visual
class CajaRegistradoraView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.root.title("Caja Registradora - Versión 1.02")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

        # Paleta de colores para toda la aplicación
        self.color_fondo = "#2C3E50"
        self.color_texto = "#ECF0F1"
        self.color_boton = "#3498DB"
        self.color_boton_hover = "#2980B9"
        self.color_acento = "#E74C3C"
        self.color_acento_hover = "#C0392B"

        self.configurar_estilo()

        # Creación de frames principales para cada módulo
        self.frame_login = tk.Frame(self.root, bg=self.color_fondo)
        self.frame_menu = tk.Frame(self.root, bg=self.color_fondo)
        self.frame_ventas = tk.Frame(self.root, bg=self.color_fondo)
        self.frame_inventario = tk.Frame(self.root, bg=self.color_fondo)
        self.frame_historial = tk.Frame(self.root, bg=self.color_fondo)

        # Variables para los ComboBox
        self.producto_seleccionado = tk.StringVar()
        self.producto_seleccionado_inventario = tk.StringVar()

        # Configurar cada uno de los frames
        self.configurar_frame_login()
        self.configurar_frame_menu()
        self.configurar_frame_ventas()
        self.configurar_frame_inventario()
        self.configurar_frame_historial()

        self.mostrar_frame(self.frame_login)

    # Configura el estilo visual de los widgets ttk
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

    # Gestiona la navegación entre frames (pantallas)
    def mostrar_frame(self, frame):
        for f in (self.frame_login, self.frame_menu, self.frame_ventas, self.frame_inventario, self.frame_historial):
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
        frame_container = tk.Frame(self.frame_menu, bg=self.color_fondo, padx=40, pady=40)
        frame_container.pack(fill="both", expand=True)

        titulo = tk.Label(frame_container, text="MENÚ PRINCIPAL",
                            font=("Arial", 24, "bold"),
                            bg=self.color_fondo, fg=self.color_texto)
        titulo.pack(pady=(0, 30))

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

        btn_historial = tk.Button(frame_container, text="Historial de Ventas",
                                    width=25, height=2,
                                    bg=self.color_boton, fg="white",
                                    activebackground=self.color_boton_hover,
                                    font=("Arial", 14, "bold"),
                                    command=lambda: self.mostrar_frame(self.frame_historial))
        btn_historial.pack(pady=10)

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
    # Interfaz para registrar ventas de productos
    def configurar_frame_ventas(self):
        main_container = tk.Frame(self.frame_ventas, bg=self.color_fondo, padx=20, pady=20)
        main_container.pack(fill="both", expand=True)

        titulo = tk.Label(main_container, text="MÓDULO DE VENTAS",
                            font=("Arial", 18, "bold"),
                            bg=self.color_fondo, fg=self.color_texto)
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Contenedor izquierdo (formulario para agregar productos)
        frame_izquierdo = tk.Frame(main_container, bg=self.color_fondo, padx=15, pady=15,
                                    highlightbackground=self.color_texto, highlightthickness=1)
        frame_izquierdo.grid(row=1, column=0, padx=(0, 10), sticky="nsew")

        tk.Label(frame_izquierdo, text="Agregar Producto",
                font=("Arial", 14, "bold"),
                bg=self.color_fondo, fg=self.color_texto).pack(pady=(0, 15))

        tk.Label(frame_izquierdo, text="Seleccione Producto:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(anchor='w', pady=(0, 5))

        # ComboBox para seleccionar productos del inventario
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

        # Contenedor derecho (detalle de venta y total)
        frame_derecho = tk.Frame(main_container, bg=self.color_fondo, padx=15, pady=15,
                                highlightbackground=self.color_texto, highlightthickness=1)
        frame_derecho.grid(row=1, column=1, padx=(10, 0), sticky="nsew")

        tk.Label(frame_derecho, text="Detalle de Venta",
                font=("Arial", 14, "bold"),
                bg=self.color_fondo, fg=self.color_texto).pack(pady=(0, 15))

        # Lista de productos agregados a la venta actual
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

        # Etiqueta para mostrar el total de la venta
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
    # Interfaz para gestionar el inventario de productos
    def configurar_frame_inventario(self):
        main_container = tk.Frame(self.frame_inventario, bg=self.color_fondo, padx=20, pady=20)
        main_container.pack(fill="both", expand=True)

        titulo = tk.Label(main_container, text="MÓDULO DE INVENTARIO",
                            font=("Arial", 18, "bold"),
                            bg=self.color_fondo, fg=self.color_texto)
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Frame izquierdo (formulario para agregar/editar productos)
        frame_izquierdo = tk.Frame(main_container, bg=self.color_fondo, padx=15, pady=15,
                                    highlightbackground=self.color_texto, highlightthickness=1)
        frame_izquierdo.grid(row=1, column=0, padx=(0, 10), sticky="nsew")

        tk.Label(frame_izquierdo, text="Gestión de Productos",
                font=("Arial", 14, "bold"),
                bg=self.color_fondo, fg=self.color_texto).pack(pady=(0, 15))

        # Formulario para agregar/editar productos
        tk.Label(frame_izquierdo, text="Producto:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(anchor='w', pady=(0, 5))
        
        # ComboBox para seleccionar productos predefinidos
        nombres_productos = [producto["nombre"] for producto in self.controller.model.productos_disponibles]
        self.combo_productos_inventario = ttk.Combobox(frame_izquierdo, 
                                                    textvariable=self.producto_seleccionado_inventario,
                                                    values=nombres_productos,
                                                    font=("Arial", 12),
                                                    state="readonly",
                                                    width=28)
        self.combo_productos_inventario.pack(fill="x", pady=(0, 10))
        self.combo_productos_inventario.bind("<<ComboboxSelected>>", self.controller.actualizar_precio_inventario)

        tk.Label(frame_izquierdo, text="Código:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(anchor='w', pady=(0, 5))
        self.entry_codigo_producto = ttk.Entry(frame_izquierdo, width=30, font=("Arial", 12))
        self.entry_codigo_producto.pack(fill="x", pady=(0, 10))

        tk.Label(frame_izquierdo, text="Precio:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(anchor='w', pady=(0, 5))
        self.entry_precio_producto = ttk.Entry(frame_izquierdo, width=30, font=("Arial", 12))
        self.entry_precio_producto.pack(fill="x", pady=(0, 10))

        tk.Label(frame_izquierdo, text="Stock:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(anchor='w', pady=(0, 5))
        self.entry_stock_producto = ttk.Entry(frame_izquierdo, width=30, font=("Arial", 12))
        self.entry_stock_producto.pack(fill="x", pady=(0, 15))

        # Frame para botones de acción
        frame_botones = tk.Frame(frame_izquierdo, bg=self.color_fondo)
        frame_botones.pack(fill="x", pady=10)

        self.btn_agregar_producto = tk.Button(frame_botones, text="Agregar Producto",
                                width=15, height=1,
                                bg=self.color_boton, fg="white",
                                activebackground=self.color_boton_hover,
                                font=("Arial", 12, "bold"),
                                command=self.controller.agregar_producto_inventario)
        self.btn_agregar_producto.pack(side="left", padx=5)

        self.btn_cancelar_edicion = tk.Button(frame_botones, text="Cancelar",
                                width=10, height=1,
                                bg=self.color_acento, fg="white",
                                activebackground=self.color_acento_hover,
                                font=("Arial", 12, "bold"),
                                command=self.controller.cancelar_edicion,
                                state="disabled")
        self.btn_cancelar_edicion.pack(side="right", padx=5)

        # Frame derecho (tabla de productos y búsqueda)
        frame_derecho = tk.Frame(main_container, bg=self.color_fondo, padx=15, pady=15,
                                highlightbackground=self.color_texto, highlightthickness=1)
        frame_derecho.grid(row=1, column=1, padx=(10, 0), sticky="nsew")

        tk.Label(frame_derecho, text="Listado de Productos",
                font=("Arial", 14, "bold"),
                bg=self.color_fondo, fg=self.color_texto).pack(pady=(0, 15))

        # Barra de búsqueda para filtrar productos
        frame_busqueda = tk.Frame(frame_derecho, bg=self.color_fondo)
        frame_busqueda.pack(fill="x", pady=(0, 10))

        tk.Label(frame_busqueda, text="Buscar:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(side="left", padx=(0, 5))

        self.entry_buscar_producto = ttk.Entry(frame_busqueda, width=20, font=("Arial", 12))
        self.entry_buscar_producto.pack(side="left", padx=(0, 5))

        tk.Label(frame_busqueda, text="Por:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(side="left", padx=(5, 5))

        self.combo_criterio_busqueda = ttk.Combobox(frame_busqueda,
                                                values=["Todos", "Código", "Nombre"],
                                                font=("Arial", 12),
                                                state="readonly",
                                                width=10)
        self.combo_criterio_busqueda.pack(side="left", padx=(0, 5))
        self.combo_criterio_busqueda.current(0)

        btn_buscar = tk.Button(frame_busqueda, text="Buscar",
                                width=8, height=1,
                                bg=self.color_boton, fg="white",
                                activebackground=self.color_boton_hover,
                                font=("Arial", 10, "bold"),
                                command=self.controller.buscar_producto)
        btn_buscar.pack(side="right", padx=5)

        # Tabla de productos usando Treeview
        frame_tabla = tk.Frame(frame_derecho, bg=self.color_fondo)
        frame_tabla.pack(fill="both", expand=True, pady=10)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        # Crear tabla con Treeview para mostrar productos
        self.tabla_productos = ttk.Treeview(frame_tabla, columns=("codigo", "nombre", "precio", "stock"),
                                        show="headings", height=10,
                                        yscrollcommand=scrollbar.set)
        self.tabla_productos.pack(fill="both", expand=True)
        scrollbar.config(command=self.tabla_productos.yview)

        # Configurar columnas
        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("precio", text="Precio")
        self.tabla_productos.heading("stock", text="Stock")

        self.tabla_productos.column("codigo", width=80)
        self.tabla_productos.column("nombre", width=200)
        self.tabla_productos.column("precio", width=100)
        self.tabla_productos.column("stock", width=80)

        # Vincular evento de selección
        self.tabla_productos.bind("<<TreeviewSelect>>", self.controller.seleccionar_producto_tabla)

        # Frame para botones de acción de la tabla
        frame_acciones = tk.Frame(frame_derecho, bg=self.color_fondo)
        frame_acciones.pack(fill="x", pady=10)

        btn_editar = tk.Button(frame_acciones, text="Editar",
                            width=10, height=1,
                            bg=self.color_boton, fg="white",
                            activebackground=self.color_boton_hover,
                            font=("Arial", 12, "bold"),
                            command=self.controller.editar_producto)
        btn_editar.pack(side="left", padx=5)

        btn_eliminar = tk.Button(frame_acciones, text="Eliminar",
                                width=10, height=1,
                                bg=self.color_acento, fg="white",
                                activebackground=self.color_acento_hover,
                                font=("Arial", 12, "bold"),
                                command=self.controller.eliminar_producto_inventario)
        btn_eliminar.pack(side="right", padx=5)

        # Botón para volver al menú
        btn_volver_menu = tk.Button(main_container, text="Volver al Menú",
                                    width=15, height=1,
                                    bg=self.color_boton, fg="white",
                                    activebackground=self.color_boton_hover,
                                    font=("Arial", 12, "bold"),
                                    command=lambda: self.mostrar_frame(self.frame_menu))
        btn_volver_menu.grid(row=2, column=0, columnspan=2, pady=20)

        # Configurar grid
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(1, weight=1)

        # Cargar productos en la tabla
        self.cargar_productos_tabla()

    # Carga los productos del modelo en la tabla de inventario
    def cargar_productos_tabla(self):
        # Limpiar tabla
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
            
        # Cargar productos desde el modelo
        for producto in self.controller.model.productos_disponibles:
            # Añadir código y stock a los productos (no existían en el modelo original)
            codigo = producto.get("codigo", "")
            stock = producto.get("stock", 0)
            self.tabla_productos.insert("", "end", values=(codigo, producto["nombre"], f"S/.{producto['precio']:.2f}", stock))
            
    # Actualiza la tabla con los resultados de búsqueda
    def actualizar_tabla_con_resultados(self, resultados):
        # Limpiar tabla
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
            
        # Cargar resultados en la tabla
        if not resultados:
            # Si no hay resultados, mostrar mensaje
            self.tabla_productos.insert("", "end", values=("No hay", "resultados", "encontrados", ""))
        else:
            # Cargar productos encontrados
            for producto in resultados:
                codigo = producto.get("codigo", "")
                stock = producto.get("stock", 0)
                self.tabla_productos.insert("", "end", values=(codigo, producto["nombre"], f"S/.{producto['precio']:.2f}", stock))

    # ---------- Frame Historial ----------
    # Interfaz para visualizar el historial de ventas e ingresos
    def configurar_frame_historial(self):
        main_container = tk.Frame(self.frame_historial, bg=self.color_fondo, padx=20, pady=20)
        main_container.pack(fill="both", expand=True)

        titulo = tk.Label(main_container, text="HISTORIAL DE MOVIMIENTOS",
                            font=("Arial", 18, "bold"),
                            bg=self.color_fondo, fg=self.color_texto)
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Frame para filtros de búsqueda por fecha
        frame_filtros = tk.Frame(main_container, bg=self.color_fondo, padx=15, pady=15,
                                highlightbackground=self.color_texto, highlightthickness=1)
        frame_filtros.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        tk.Label(frame_filtros, text="Filtrar por fecha:",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(side="left", padx=5)

        self.entry_fecha_inicio = ttk.Entry(frame_filtros, width=15, font=("Arial", 12))
        self.entry_fecha_inicio.pack(side="left", padx=5)
        self.entry_fecha_inicio.insert(0, "DD/MM/AAAA")

        tk.Label(frame_filtros, text="hasta",
                font=("Arial", 12),
                bg=self.color_fondo, fg=self.color_texto).pack(side="left", padx=5)

        self.entry_fecha_fin = ttk.Entry(frame_filtros, width=15, font=("Arial", 12))
        self.entry_fecha_fin.pack(side="left", padx=5)
        self.entry_fecha_fin.insert(0, "DD/MM/AAAA")

        btn_buscar = tk.Button(frame_filtros, text="Buscar",
                                width=8, height=1,
                                bg=self.color_boton, fg="white",
                                activebackground=self.color_boton_hover,
                                font=("Arial", 10, "bold"),
                                command=self.controller.buscar_ventas_por_fecha)
        btn_buscar.pack(side="left", padx=5)

        btn_mostrar_todo = tk.Button(frame_filtros, text="Mostrar Todo",
                                width=10, height=1,
                                bg=self.color_boton, fg="white",
                                activebackground=self.color_boton_hover,
                                font=("Arial", 10, "bold"),
                                command=self.controller.mostrar_todo_historial)
        btn_mostrar_todo.pack(side="left", padx=5)

        # Tabla de historial
        frame_tabla = tk.Frame(main_container, bg=self.color_fondo)
        frame_tabla.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        # Crear tabla con Treeview
        self.tabla_historial = ttk.Treeview(frame_tabla, 
                                        columns=("codigo", "fecha", "producto", "cantidad", "precio_unitario", "total"),
                                        show="headings", height=15,
                                        yscrollcommand=scrollbar.set)
        self.tabla_historial.pack(fill="both", expand=True)
        scrollbar.config(command=self.tabla_historial.yview)

        # Configurar columnas
        self.tabla_historial.heading("codigo", text="Código")
        self.tabla_historial.heading("fecha", text="Fecha")
        self.tabla_historial.heading("producto", text="Producto")
        self.tabla_historial.heading("cantidad", text="Cantidad")
        self.tabla_historial.heading("precio_unitario", text="Precio Unit.")
        self.tabla_historial.heading("total", text="Total")

        self.tabla_historial.column("codigo", width=100)
        self.tabla_historial.column("fecha", width=150)
        self.tabla_historial.column("producto", width=200)
        self.tabla_historial.column("cantidad", width=80)
        self.tabla_historial.column("precio_unitario", width=100)
        self.tabla_historial.column("total", width=100)

        # Botón para volver al menú
        btn_volver_menu = tk.Button(main_container, text="Volver al Menú",
                                    width=15, height=1,
                                    bg=self.color_boton, fg="white",
                                    activebackground=self.color_boton_hover,
                                    font=("Arial", 12, "bold"),
                                    command=lambda: self.mostrar_frame(self.frame_menu))
        btn_volver_menu.grid(row=3, column=0, columnspan=2, pady=20)

        # Configurar grid
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(2, weight=1)

    def cargar_historial_tabla(self, historial):
        # Limpiar tabla
        for item in self.tabla_historial.get_children():
            self.tabla_historial.delete(item)
            
        # Cargar historial en la tabla
        for registro in historial:
            for producto in registro["productos"]:
                self.tabla_historial.insert("", "end", values=(
                    registro["codigo"],
                    registro["fecha"],
                    producto["producto"],
                    producto["cantidad"],
                    f"S/.{producto['precio_unitario']:.2f}",
                    f"S/.{producto['subtotal']:.2f}"
                ))
