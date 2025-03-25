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
        else:
            resumen = "RESUMEN DE VENTA\n" + "=" * 40 + "\n\n"
            for i, item in enumerate(self.model.productos_venta):
                resumen += f"{i+1}. {item['producto']}\n"
                resumen += f"   {item['cantidad']} x S/.{item['precio']:.2f} = S/.{item['subtotal']:.2f}\n"
            resumen += "\n" + "=" * 40 + "\n"
            resumen += f"Total de productos: {len(self.model.productos_venta)}\n"
            resumen += f"Total a pagar: S/.{self.model.total_venta:.2f}\n\n"
            resumen += "¡Gracias por su compra!"
            self.mostrar_ticket(resumen)
            self.view.lista_ventas.delete(0, tk.END)
            self.model.total_venta = 0
            self.model.productos_venta = []
            self.view.label_total.config(text="Total: S/.0.00")

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
