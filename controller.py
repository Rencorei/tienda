import tkinter as tk
from tkinter import messagebox
import datetime
from model import CajaRegistradoraModel
from view import CajaRegistradoraView

class CajaRegistradoraController:
    def __init__(self, root):
        self.model = CajaRegistradoraModel()
        self.view = CajaRegistradoraView(root, self)

    def validar_login(self):
        usuario = self.view.entry_usuario.get()
        password = self.view.entry_password.get()
        if usuario == "admin" and password == "1234":
            self.view.mostrar_frame(self.view.frame_menu)
        else:
            messagebox.showerror("Error de Login",
                                "Usuario o contraseña incorrectos.\nQuizá deberías revisar tu memoria.")

    def cerrar_sesion(self):
        self.view.entry_usuario.delete(0, tk.END)
        self.view.entry_password.delete(0, tk.END)
        self.view.mostrar_frame(self.view.frame_login)

    def actualizar_precio(self, event=None):
        nombre_producto = self.view.producto_seleccionado.get()
        for producto in self.model.productos_disponibles:
            if producto["nombre"] == nombre_producto:
                self.view.entry_precio.config(state="normal")
                self.view.entry_precio.delete(0, tk.END)
                self.view.entry_precio.insert(0, f"{producto['precio']:.2f}")
                self.view.entry_precio.config(state="readonly")
                break

    def agregar_producto(self):
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

        precio = 0
        for producto in self.model.productos_disponibles:
            if producto["nombre"] == nombre_producto:
                precio = producto["precio"]
                break

        subtotal = precio * cantidad
        self.model.productos_venta.append({
            "producto": nombre_producto,
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": subtotal,
            "index": len(self.model.productos_venta)
        })
        self.model.total_venta += subtotal
        self.view.lista_ventas.insert(tk.END, f"{nombre_producto} - {cantidad} x S/.{precio:.2f} = S/.{subtotal:.2f}")
        self.view.label_total.config(text=f"Total: S/.{self.model.total_venta:.2f}")

        # Limpiar campos
        self.view.combo_productos.set('')
        self.view.entry_precio.config(state="normal")
        self.view.entry_precio.delete(0, tk.END)
        self.view.entry_precio.config(state="readonly")
        self.view.entry_cantidad.delete(0, tk.END)
        self.view.entry_cantidad.insert(0, "1")

    def eliminar_producto(self):
        try:
            index = self.view.lista_ventas.curselection()[0]
            self.view.lista_ventas.delete(index)
            producto_eliminado = self.model.productos_venta[index]
            self.model.total_venta -= producto_eliminado["subtotal"]
            self.view.label_total.config(text=f"Total: S/.{self.model.total_venta:.2f}")
            self.model.productos_venta.pop(index)
        except IndexError:
            messagebox.showerror("Error", "Debe seleccionar un producto para eliminar.")

    def finalizar_venta(self):
        if self.model.total_venta == 0:
            messagebox.showinfo("Venta", "No hay nada que cobrar. ¿Vendiendo aire?")
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
            
        # Generar código de venta
        codigo_venta = self.model.generar_codigo_venta()
        fecha_venta = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
        # Generar resumen de venta
        resumen = "RESUMEN DE VENTA\n" + "=" * 40 + "\n\n"
        resumen += f"Código de Venta: {codigo_venta}\n"
        resumen += f"Fecha: {fecha_venta}\n\n"
        for i, item in enumerate(self.model.productos_venta):
            resumen += f"{i+1}. {item['producto']}\n"
            resumen += f"   {item['cantidad']} x S/.{item['precio']:.2f} = S/.{item['subtotal']:.2f}\n"
        resumen += "\n" + "=" * 40 + "\n"
        resumen += f"Total de productos: {len(self.model.productos_venta)}\n"
        resumen += f"Total a pagar: S/.{self.model.total_venta:.2f}\n\n"
        resumen += "¡Gracias por su compra!"
        
        # Actualizar el inventario
        actualizaciones_stock = []
        for item in self.model.productos_venta:
            nombre_producto = item['producto']
            cantidad_venta = item['cantidad']
            
            # Buscar el producto en el inventario y actualizar stock
            for producto in self.model.productos_disponibles:
                if producto["nombre"] == nombre_producto:
                    codigo = producto["codigo"]
                    precio = producto["precio"]
                    stock_anterior = producto["stock"]
                    nuevo_stock = producto["stock"] - cantidad_venta
                    self.model.actualizar_producto(codigo, nombre_producto, precio, nuevo_stock)
                    actualizaciones_stock.append(f"{nombre_producto}: {stock_anterior} → {nuevo_stock}")
                    break
        
        # Guardar la venta en el historial
        self.model.agregar_venta_al_historial(codigo_venta, fecha_venta, self.model.productos_venta, self.model.total_venta)
        
        # Mostrar ticket y limpiar venta actual
        self.mostrar_ticket(resumen)
        
        # Mostrar resumen de actualización de stock
        mensaje_stock = "Actualización de Stock:\n\n"
        for actualizacion in actualizaciones_stock:
            mensaje_stock += f"- {actualizacion}\n"
        messagebox.showinfo("Stock Actualizado", mensaje_stock)
        
        self.view.lista_ventas.delete(0, tk.END)
        self.model.total_venta = 0
        self.model.productos_venta = []
        self.view.label_total.config(text="Total: S/.0.00")
        
        # Actualizar la tabla de productos en el módulo de inventario
        self.view.cargar_productos_tabla()
        
        # Actualizar el ComboBox de productos en el módulo de ventas
        self.view.combo_productos['values'] = [p["nombre"] for p in self.model.productos_disponibles]
        
        # Actualizar la tabla de historial si está visible
        if self.view.frame_historial.winfo_viewable():
            self.view.cargar_historial_tabla(self.model.obtener_historial_ventas())

    def mostrar_ticket(self, texto):
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
    def actualizar_precio_inventario(self, event):
        nombre_producto = self.view.producto_seleccionado_inventario.get()
        for producto in self.model.productos_disponibles:
            if producto["nombre"] == nombre_producto:
                # Actualizar código
                self.view.entry_codigo_producto.config(state="normal")
                self.view.entry_codigo_producto.delete(0, tk.END)
                self.view.entry_codigo_producto.insert(0, producto["codigo"])
                self.view.entry_codigo_producto.config(state="readonly")
                
                # Actualizar precio
                self.view.entry_precio_producto.config(state="normal")
                self.view.entry_precio_producto.delete(0, tk.END)
                self.view.entry_precio_producto.insert(0, f"{producto['precio']:.2f}")
                self.view.entry_precio_producto.config(state="readonly")
                break
                
    def agregar_producto_inventario(self):
        # Obtener datos del formulario
        codigo = self.view.entry_codigo_producto.get().strip()
        nombre_producto = self.view.producto_seleccionado_inventario.get().strip()
        precio_str = self.view.entry_precio_producto.get().strip()
        stock_str = self.view.entry_stock_producto.get().strip()
        
        # Validar datos
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
        
        # Verificar si estamos en modo edición
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
                    codigo_ingreso = self.model.generar_codigo_ingreso()
                    fecha_ingreso = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    self.model.agregar_ingreso_al_historial(codigo_ingreso, fecha_ingreso, nombre_producto, stock, precio)
                    
                    messagebox.showinfo("Éxito", f"Stock actualizado correctamente\nCódigo de ingreso: {codigo_ingreso}")
                    self.limpiar_formulario_inventario()
                    self.view.cargar_productos_tabla()
                    
                    # Actualizar la tabla de historial si está visible
                    if self.view.frame_historial.winfo_viewable():
                        self.view.cargar_historial_tabla(self.model.obtener_historial_completo())
                else:
                    messagebox.showerror("Error", mensaje)
            else:
                # Si el producto no existe, agregarlo como nuevo
                exito, mensaje = self.model.agregar_producto(codigo, nombre_producto, precio, stock)
                if exito:
                    # Generar código de ingreso y registrar en el historial
                    codigo_ingreso = self.model.generar_codigo_ingreso()
                    fecha_ingreso = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    self.model.agregar_ingreso_al_historial(codigo_ingreso, fecha_ingreso, nombre_producto, stock, precio)
                    
                    messagebox.showinfo("Éxito", f"{mensaje}\nCódigo de ingreso: {codigo_ingreso}")
                    self.limpiar_formulario_inventario()
                    self.view.cargar_productos_tabla()
                    
                    # Actualizar la tabla de historial si está visible
                    if self.view.frame_historial.winfo_viewable():
                        self.view.cargar_historial_tabla(self.model.obtener_historial_completo())
                else:
                    messagebox.showerror("Error", mensaje)
    
    def editar_producto(self):
        # Obtener el producto seleccionado en la tabla
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
        # Limpiar el formulario y restablecer el estado
        self.limpiar_formulario_inventario()
        self.view.entry_codigo_producto.config(state="normal")
        self.view.btn_agregar_producto.config(text="Agregar Producto")
        self.view.btn_cancelar_edicion.config(state="disabled")
        self.producto_en_edicion = None
    
    def limpiar_formulario_inventario(self):
        # Limpiar todos los campos del formulario
        self.view.entry_codigo_producto.config(state="normal")
        self.view.entry_codigo_producto.delete(0, tk.END)
        self.view.combo_productos_inventario.set('')
        self.view.entry_precio_producto.config(state="normal")
        self.view.entry_precio_producto.delete(0, tk.END)
        self.view.entry_precio_producto.config(state="readonly")
        self.view.entry_stock_producto.delete(0, tk.END)
    
    def eliminar_producto_inventario(self):
        # Obtener el producto seleccionado en la tabla
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
        # Obtener texto de búsqueda y criterio
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

    def buscar_ventas_por_fecha(self):
        try:
            fecha_inicio = datetime.datetime.strptime(self.view.entry_fecha_inicio.get(), "%d/%m/%Y")
            fecha_fin = datetime.datetime.strptime(self.view.entry_fecha_fin.get(), "%d/%m/%Y")
            fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)
            
            historial_completo = self.model.obtener_historial_completo()
            resultados = []
            
            for registro in historial_completo:
                fecha_registro = datetime.datetime.strptime(registro["fecha"], "%d/%m/%Y %H:%M:%S")
                if fecha_inicio <= fecha_registro <= fecha_fin:
                    resultados.append(registro)
            
            self.view.cargar_historial_tabla(resultados)
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use DD/MM/AAAA")
    
    def mostrar_todo_historial(self):
        historial_completo = self.model.obtener_historial_completo()
        self.view.cargar_historial_tabla(historial_completo)
