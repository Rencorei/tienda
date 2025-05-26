import tkinter as tk
from tkinter import messagebox
import datetime
from model import CajaRegistradoraModel
from view import CajaRegistradoraView

# Clase principal que implementa el controlador en el patrón MVC
# Gestiona la lógica de la aplicación y la comunicación entre el modelo y la vista
class CajaRegistradoraController:
    def __init__(self, root):
        self.model = CajaRegistradoraModel()  # Inicializa el modelo (datos)
        self.view = CajaRegistradoraView(root, self)  # Inicializa la vista (interfaz)

    # ---------- Métodos para el Módulo de Login ----------
    def validar_login(self):
        # Autenticación usando la base de datos
        usuario = self.view.entry_usuario.get()
        password = self.view.entry_password.get()
        
        if not usuario or not password:
            messagebox.showerror("Error de Login", "Debe ingresar usuario y contraseña.")
            return
            
        success, result = self.model.validar_usuario(usuario, password)
        
        if success:
            self.view.mostrar_frame(self.view.frame_menu)
            # Mostrar mensaje de bienvenida con el rol del usuario
            messagebox.showinfo("Bienvenido", f"Bienvenido {usuario}\nRol: {result['rol']}")
        else:
            messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")


    def cerrar_sesion(self):
        # Limpia los campos y vuelve a la pantalla de login
        self.view.entry_usuario.delete(0, tk.END)
        self.view.entry_password.delete(0, tk.END)
        self.model.cerrar_sesion()
        self.view.mostrar_frame(self.view.frame_login)

    # ---------- Métodos para el Módulo de Ventas ----------
    def actualizar_precio(self, event=None):
        # Actualiza el precio mostrado cuando se selecciona un producto
        nombre_producto = self.view.producto_seleccionado.get()
        for producto in self.model.productos_disponibles:
            if producto["nombre"] == nombre_producto:
                self.view.entry_precio.config(state="normal")
                self.view.entry_precio.delete(0, tk.END)
                self.view.entry_precio.insert(0, f"{producto['precio']:.2f}")
                self.view.entry_precio.config(state="readonly")
                break

    def agregar_producto(self):
        # Agrega un producto a la venta actual
        nombre_producto = self.view.producto_seleccionado.get()
        if not nombre_producto:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return

        try:
            cantidad = int(self.view.entry_cantidad.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser un valor positivo.")
                return
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida. ¿Te saltaste la clase de matemáticas?")
            return

        # Buscar el precio del producto seleccionado
        precio = 0
        for producto in self.model.productos_disponibles:
            if producto["nombre"] == nombre_producto:
                precio = producto["precio"]
                break

        # Calcular subtotal y agregar a la lista de productos en venta
        subtotal = precio * cantidad
        self.model.productos_venta.append({
            "producto": nombre_producto,
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": subtotal,
            "index": len(self.model.productos_venta)
        })
        # Convertir subtotal a float antes de sumarlo para evitar error de tipos incompatibles
        self.model.total_venta += float(subtotal)
        self.view.lista_ventas.insert(tk.END, f"{nombre_producto} - {cantidad} x S/.{precio:.2f} = S/.{subtotal:.2f}")
        self.view.label_total.config(text=f"Total: S/.{self.model.total_venta:.2f}")

        # Limpiar campos para el siguiente producto
        self.view.combo_productos.set('')
        self.view.entry_precio.config(state="normal")
        self.view.entry_precio.delete(0, tk.END)
        self.view.entry_precio.config(state="readonly")
        self.view.entry_cantidad.delete(0, tk.END)
        self.view.entry_cantidad.insert(0, "1")

    def eliminar_producto(self):
        # Elimina un producto de la venta actual
        try:
            index = self.view.lista_ventas.curselection()[0]
            self.view.lista_ventas.delete(index)
            producto_eliminado = self.model.productos_venta[index]
            # Convertir subtotal a float antes de restarlo para evitar error de tipos incompatibles
            self.model.total_venta -= float(producto_eliminado["subtotal"])
            self.view.label_total.config(text=f"Total: S/.{self.model.total_venta:.2f}")
            self.model.productos_venta.pop(index)
        except IndexError:
            messagebox.showerror("Error", "Debe seleccionar un producto para eliminar.")

    def finalizar_venta(self):
        # Procesa y finaliza la venta actual
        if self.model.total_venta == 0:
            messagebox.showinfo("Venta", "No hay nada que cobrar. ¿Vendiendo aire?")
            return
        
        # Verificar que haya un usuario con sesión activa
        if not self.model.usuario_actual:
            messagebox.showerror("Error", "Debe iniciar sesión para realizar una venta.")
            return
            
        # Verificar stock suficiente antes de finalizar la venta
        productos_sin_stock = []
        for item in self.model.productos_venta:
            nombre_producto = item['producto']
            cantidad_venta = item['cantidad']
            
            # Buscar el producto en el inventario
            for producto in self.model.productos_disponibles:
                if producto["nombre"] == nombre_producto:
                    if producto["stock"] < cantidad_venta:
                        productos_sin_stock.append(f"{nombre_producto} (disponible: {producto['stock']}, solicitado: {cantidad_venta})")
                    break
        
        # Si hay productos sin stock suficiente, mostrar mensaje y cancelar venta
        if productos_sin_stock:
            mensaje_error = "No hay suficiente stock para los siguientes productos:\n\n"
            for prod in productos_sin_stock:
                mensaje_error += f"- {prod}\n"
            messagebox.showerror("Error de Inventario", mensaje_error)
            return
            
        # Generar código de venta y fecha
        codigo_venta = self.model.generar_codigo_venta()
        fecha_venta = datetime.datetime.now()
            
        # Generar resumen de venta para el ticket
        resumen = "RESUMEN DE VENTA\n" + "=" * 40 + "\n\n"
        resumen += f"Código de Venta: {codigo_venta}\n"
        resumen += f"Fecha: {fecha_venta.strftime('%d/%m/%Y %H:%M:%S')}\n"
        resumen += f"Vendedor: {self.model.usuario_actual['usuario']}\n\n"
        for i, item in enumerate(self.model.productos_venta):
            resumen += f"{i+1}. {item['producto']}\n"
            resumen += f"   {item['cantidad']} x S/.{item['precio']:.2f} = S/.{item['subtotal']:.2f}\n"
        resumen += "\n" + "=" * 40 + "\n"
        resumen += f"Total de productos: {len(self.model.productos_venta)}\n"
        resumen += f"Total a pagar: S/.{self.model.total_venta:.2f}\n\n"
        resumen += "¡Gracias por su compra!"
        
        # Guardar la venta en la base de datos
        success, mensaje = self.model.agregar_venta_al_historial(codigo_venta, fecha_venta, self.model.productos_venta, self.model.total_venta)
        
        if not success:
            messagebox.showerror("Error", f"Error al registrar la venta: {mensaje}")
            return
        
        # Mostrar ticket y limpiar venta actual
        self.mostrar_ticket(resumen)
        
        # Reiniciar la venta actual
        self.view.lista_ventas.delete(0, tk.END)
        self.model.total_venta = 0
        self.model.productos_venta = []
        self.view.label_total.config(text="Total: S/.0.00")
        
        # Actualizar interfaces con los nuevos datos
        self.view.cargar_productos_tabla()
        self.view.combo_productos['values'] = [p["nombre"] for p in self.model.productos_disponibles]
        
        # Actualizar la tabla de historial si está visible
        if self.view.frame_historial.winfo_viewable():
            self.view.cargar_historial_tabla(self.model.obtener_historial_ventas())

    def mostrar_ticket(self, texto):
        # Crea y muestra una ventana con el ticket de venta
        ticket_window = tk.Toplevel(self.view.root)
        ticket_window.title("Ticket de Venta")
        ticket_window.geometry("400x550")
        ticket_window.resizable(False, False)
        ticket_window.configure(bg="white")
        ticket_window.transient(self.view.root)
        ticket_window.grab_set()
        ticket_window.geometry("+{}+{}".format(
            self.view.root.winfo_x() + int(self.view.root.winfo_width()/2 - 200),
            self.view.root.winfo_y() + int(self.view.root.winfo_height()/2 - 250)
        ))
        frame_ticket = tk.Frame(ticket_window, bg="white", padx=20, pady=20)
        frame_ticket.pack(fill="both", expand=True)
        tk.Label(frame_ticket, text="TICKET DE VENTA", font=("Courier", 16, "bold"),
                bg="white").pack(pady=(0, 10))
        
        tk.Label(frame_ticket, text="Corporacion SkynetSoft", font=("Courier", 12),
                bg="white").pack(pady=(0, 10))

        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tk.Label(frame_ticket, text=f"Fecha: {fecha_actual}", font=("Courier", 10),
                bg="white").pack(anchor="w")
        tk.Frame(frame_ticket, height=2, bg="black").pack(fill="x", pady=10)
        texto_ticket = tk.Text(frame_ticket, height=20, width=45, font=("Courier", 10),
                            bg="white", relief="flat")
        texto_ticket.pack(fill="both", expand=True)
        texto_ticket.insert("1.0", texto)
        texto_ticket.config(state="disabled")
        frame_botones = tk.Frame(frame_ticket, bg="white")
        frame_botones.pack(fill="x", pady=10)
        btn_imprimir = tk.Button(frame_botones, text="Imprimir", width=10, height=1,
                                bg=self.view.color_boton, fg="white",
                                activebackground=self.view.color_boton_hover,
                                font=("Arial", 10, "bold"),
                                command=lambda: messagebox.showinfo("Imprimir", "Enviando a impresora..."))
        btn_imprimir.pack(side="left", padx=5)
        btn_cerrar = tk.Button(frame_botones, text="Cerrar", width=10, height=1,
                                bg=self.view.color_acento, fg="white",
                                activebackground=self.view.color_acento_hover,
                                font=("Arial", 10, "bold"),
                                command=ticket_window.destroy)
        btn_cerrar.pack(side="right", padx=5)

    def mostrar_about(self):
        # Muestra la ventana "Acerca de" con información de la aplicación
        about_window = tk.Toplevel(self.view.root)
        about_window.title("Acerca de")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        about_window.configure(bg=self.view.color_fondo)
        about_window.transient(self.view.root)
        about_window.grab_set()
        about_window.geometry("+{}+{}".format(
            self.view.root.winfo_x() + int(self.view.root.winfo_width()/2 - 200),
            self.view.root.winfo_y() + int(self.view.root.winfo_height()/2 - 150)
        ))
        tk.Label(about_window, text="CAJA REGISTRADORA", font=("Arial", 18, "bold"),
                bg=self.view.color_fondo, fg=self.view.color_texto).pack(pady=(20, 10))
        tk.Label(about_window, text="Versión 1.02", font=("Arial", 12),
                bg=self.view.color_fondo, fg=self.view.color_texto).pack()
        tk.Label(about_window, text="", bg=self.view.color_fondo).pack(pady=10)
        tk.Label(about_window, text="Desarrollado por SkynetSoft Code", font=("Arial", 12),
                bg=self.view.color_fondo, fg=self.view.color_texto).pack()
        tk.Label(about_window, text="© 2025 Todos los derechos reservados", font=("Arial", 10),
                bg=self.view.color_fondo, fg=self.view.color_texto).pack(pady=5)
        tk.Label(about_window, text="Hecho con café y algo de sarcasmo", font=("Arial", 10, "italic"),
                bg=self.view.color_fondo, fg=self.view.color_texto).pack(pady=5)
        tk.Button(about_window, text="Cerrar", width=10, height=1,
                bg=self.view.color_boton, fg="white",
                activebackground=self.view.color_boton_hover,
                font=("Arial", 10, "bold"),
                command=about_window.destroy).pack(pady=20)
                
    # ---------- Métodos para el Módulo de Inventario ----------
    def actualizar_precio_inventario(self, event=None):
        # Actualiza los campos cuando se selecciona un producto en el inventario
        nombre_producto = self.view.producto_seleccionado_inventario.get()
        if nombre_producto:
            for producto in self.model.productos_disponibles:
                if producto["nombre"] == nombre_producto:
                    self.view.entry_codigo_producto.config(state="normal")
                    self.view.entry_codigo_producto.delete(0, tk.END)
                    self.view.entry_codigo_producto.insert(0, producto["codigo"])
                    self.view.entry_codigo_producto.config(state="readonly")
                    
                    self.view.entry_precio_producto.config(state="normal")
                    self.view.entry_precio_producto.delete(0, tk.END)
                    self.view.entry_precio_producto.insert(0, f"{producto['precio']:.2f}")
                    self.view.entry_precio_producto.config(state="readonly")
                    
                    self.view.entry_stock_producto.delete(0, tk.END)
                    self.view.entry_stock_producto.insert(0, producto["stock"])
                    # Deshabilitar edición del código si es un producto existente
                    self.view.btn_agregar_producto.config(text="Actualizar Producto")
                    self.view.btn_cancelar_edicion.config(state="normal")
                    break
                
    def agregar_producto_inventario(self):
        # Agrega o actualiza un producto en el inventario
        # Obtener datos del formulario
        codigo = self.view.entry_codigo_producto.get().strip()
        nombre_producto = self.view.producto_seleccionado_inventario.get().strip()
        precio_str = self.view.entry_precio_producto.get().strip()
        stock_str = self.view.entry_stock_producto.get().strip()
        
        # Validar datos ingresados
        if not codigo or not nombre_producto or not precio_str or not stock_str:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
            
        try:
            precio = float(precio_str)
            if precio <= 0:
                messagebox.showerror("Error", "El precio debe ser un valor positivo.")
                return
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un valor numérico.")
            return
            
        try:
            stock = int(stock_str)
            if stock < 0:
                messagebox.showerror("Error", "El stock no puede ser negativo.")
                return
        except ValueError:
            messagebox.showerror("Error", "El stock debe ser un valor entero.")
            return
        
        # Verificar si estamos en modo edición o agregando nuevo producto
        if hasattr(self, 'producto_en_edicion') and self.producto_en_edicion:
            # Actualizar producto existente
            exito, mensaje = self.model.actualizar_producto(codigo, nombre_producto, precio, stock)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cancelar_edicion()
                self.view.cargar_productos_tabla()
            else:
                messagebox.showerror("Error", mensaje)
        else:
            # Verificar si el producto ya existe en el inventario
            producto_existente = None
            for producto in self.model.productos_disponibles:
                if producto["codigo"] == codigo:
                    producto_existente = producto
                    break
            
            if producto_existente:
                # Si el producto ya existe, actualizar su stock
                nuevo_stock = producto_existente["stock"] + stock
                exito, mensaje = self.model.actualizar_producto(codigo, nombre_producto, precio, nuevo_stock)
                if exito:
                    # Generar código de ingreso y registrar en el historial
                    codigo_ingreso = self.model.generar_codigo_movimiento()
                    fecha_ingreso = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    
                    # Obtener el ID del producto
                    for producto in self.model.productos_disponibles:
                        if producto["codigo"] == codigo:
                            producto_id = producto["id"]
                            break
                    
                    # Registrar el movimiento de inventario
                    self.model.registrar_movimiento_inventario(producto_id, 'ingreso', stock, precio)
                    
                    messagebox.showinfo("Éxito", f"Stock actualizado correctamente\nCódigo de ingreso: {codigo_ingreso}")
                    self.limpiar_formulario_inventario()
                    self.view.cargar_productos_tabla()
                    
                    # Actualizar la tabla de historial si está visible
                    if self.view.frame_historial.winfo_viewable():
                        self.view.cargar_historial_tabla(self.model.obtener_historial_ventas())
                else:
                    messagebox.showerror("Error", mensaje)
            else:
                # Si el producto no existe, agregarlo como nuevo
                exito, mensaje = self.model.agregar_producto(codigo, nombre_producto, precio, stock)
                if exito:
                    # Generar código de ingreso y registrar en el historial
                    codigo_ingreso = self.model.generar_codigo_movimiento()
                    fecha_ingreso = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    
                    # Obtener el ID del producto
                    for producto in self.model.productos_disponibles:
                        if producto["codigo"] == codigo:
                            producto_id = producto["id"]
                            break
                    
                    # Registrar el movimiento de inventario
                    self.model.registrar_movimiento_inventario(producto_id, 'ingreso', stock, precio)
                    
                    messagebox.showinfo("Éxito", f"{mensaje}\nCódigo de ingreso: {codigo_ingreso}")
                    self.limpiar_formulario_inventario()
                    self.view.cargar_productos_tabla()
                    
                    # Actualizar la tabla de historial si está visible
                    if self.view.frame_historial.winfo_viewable():
                        self.view.cargar_historial_tabla(self.model.obtener_historial_ventas())
                else:
                    messagebox.showerror("Error", mensaje)
    
    def editar_producto(self):
        # Carga los datos de un producto seleccionado para edición
        seleccion = self.view.tabla_productos.selection()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar un producto para editar.")
            return
            
        # Obtener los valores del producto seleccionado
        valores = self.view.tabla_productos.item(seleccion[0], 'values')
        codigo = valores[0]
        
        # Buscar el producto en el modelo
        for producto in self.model.productos_disponibles:
            if producto["codigo"] == codigo:
                # Guardar referencia al producto en edición
                self.producto_en_edicion = producto
                
                # Llenar el formulario con los datos del producto
                self.view.entry_codigo_producto.config(state="normal")
                self.view.entry_codigo_producto.delete(0, tk.END)
                self.view.entry_codigo_producto.insert(0, producto["codigo"])
                self.view.entry_codigo_producto.config(state="readonly")
                
                # Seleccionar el producto en el ComboBox
                self.view.combo_productos_inventario.set(producto["nombre"])
                
                # Actualizar precio
                self.view.entry_precio_producto.config(state="normal")
                self.view.entry_precio_producto.delete(0, tk.END)
                self.view.entry_precio_producto.insert(0, f"{producto['precio']:.2f}")
                self.view.entry_precio_producto.config(state="readonly")
                
                self.view.entry_stock_producto.delete(0, tk.END)
                self.view.entry_stock_producto.insert(0, producto["stock"])
                
                # Cambiar el texto del botón y habilitar el botón de cancelar
                self.view.btn_agregar_producto.config(text="Actualizar Producto")
                self.view.btn_cancelar_edicion.config(state="normal")
                break
    
    def cancelar_edicion(self):
        # Cancela el modo de edición y limpia el formulario
        self.limpiar_formulario_inventario()
        self.view.entry_codigo_producto.config(state="normal")
        self.view.btn_agregar_producto.config(text="Agregar Producto")
        self.view.btn_cancelar_edicion.config(state="disabled")
        self.producto_en_edicion = None
    
    def limpiar_formulario_inventario(self):
        # Limpia todos los campos del formulario de inventario
        self.view.entry_codigo_producto.config(state="normal")
        self.view.entry_codigo_producto.delete(0, tk.END)
        self.view.combo_productos_inventario.set('')
        self.view.entry_precio_producto.config(state="normal")
        self.view.entry_precio_producto.delete(0, tk.END)
        self.view.entry_precio_producto.config(state="readonly")
        self.view.entry_stock_producto.delete(0, tk.END)
    
    def eliminar_producto_inventario(self):
        # Elimina un producto del inventario
        seleccion = self.view.tabla_productos.selection()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar un producto para eliminar.")
            return
            
        # Obtener el código del producto seleccionado
        valores = self.view.tabla_productos.item(seleccion[0], 'values')
        codigo = valores[0]
        nombre = valores[1]
        
        # Confirmar eliminación
        confirmacion = messagebox.askyesno("Confirmar Eliminación", 
                                          f"¿Está seguro de eliminar el producto '{nombre}'?")
        if confirmacion:
            exito, mensaje = self.model.eliminar_producto(codigo)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.view.cargar_productos_tabla()
                
                # Si el producto estaba en edición, cancelar la edición
                if hasattr(self, 'producto_en_edicion') and self.producto_en_edicion and \
                   self.producto_en_edicion["codigo"] == codigo:
                    self.cancelar_edicion()
            else:
                messagebox.showerror("Error", mensaje)
    
    def buscar_producto(self):
        # Busca productos según criterio y texto ingresado
        texto = self.view.entry_buscar_producto.get().strip()
        criterio = self.view.combo_criterio_busqueda.get()
        
        # Realizar búsqueda
        resultados = self.model.buscar_productos(texto, criterio)
        
        # Actualizar tabla con resultados
        self.view.actualizar_tabla_con_resultados(resultados)
    
    def seleccionar_producto_tabla(self, event):
        # Este método se llama cuando se selecciona un producto en la tabla
        # Se puede usar para mostrar detalles adicionales o habilitar botones
        pass

    # ---------- Métodos para el Módulo de Historial ----------
    def buscar_ventas_por_fecha(self):
        # Filtra el historial por rango de fechas
        try:
            fecha_inicio = datetime.datetime.strptime(self.view.entry_fecha_inicio.get(), "%d/%m/%Y")
            fecha_fin = datetime.datetime.strptime(self.view.entry_fecha_fin.get(), "%d/%m/%Y")
            fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)
            
            historial_completo = self.model.obtener_historial_ventas()
            resultados = []
            
            for registro in historial_completo:
                fecha_registro = datetime.datetime.strptime(registro["fecha"], "%d/%m/%Y %H:%M:%S")
                if fecha_inicio <= fecha_registro <= fecha_fin:
                    resultados.append(registro)
            
            self.view.cargar_historial_tabla(resultados)
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use DD/MM/AAAA")
    
    def mostrar_todo_historial(self):
        # Muestra el historial completo sin filtros
        historial_completo = self.model.obtener_historial_ventas()
        self.view.cargar_historial_tabla(historial_completo)
