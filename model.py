import datetime

class CajaRegistradoraModel:
    def __init__(self):
        self.productos_disponibles = [
            {"codigo": "LAP001", "nombre": "Laptop HP 15", "precio": 2200.00, "stock": 10},
            {"codigo": "MON001", "nombre": "Monitor Dell 24\"", "precio": 450.00, "stock": 15},
            {"codigo": "TEC001", "nombre": "Teclado Logitech K120", "precio": 120.00, "stock": 20},
            {"codigo": "MOU001", "nombre": "Mouse Inalámbrico HP", "precio": 110.00, "stock": 25},
            {"codigo": "IMP001", "nombre": "Impresora Canon MX490", "precio": 860.00, "stock": 8},
            {"codigo": "HDD001", "nombre": "Disco Duro Externo 1TB", "precio": 420.00, "stock": 12},
            {"codigo": "USB001", "nombre": "Memoria USB 32GB", "precio": 25.00, "stock": 30},
            {"codigo": "WEB001", "nombre": "Webcam Logitech C920", "precio": 140.00, "stock": 18},
            {"codigo": "AUD001", "nombre": "Auriculares Sony WH-1000XM4", "precio": 320.00, "stock": 15},
            {"codigo": "ROU001", "nombre": "Router TP-Link AC1200", "precio": 86.00, "stock": 22}
        ]
        self.total_venta = 0.0
        self.productos_venta = []
        self.contador_ventas = 0  # Contador para generar códigos de venta
        self.contador_ingresos = 0  # Contador para generar códigos de ingreso
        self.historial_ventas = []  # Lista para almacenar el historial de ventas
        self.historial_ingresos = []  # Lista para almacenar el historial de ingresos
        
    def generar_codigo_venta(self):
        self.contador_ventas += 1
        return f"F01-{self.contador_ventas:04d}"
    
    def generar_codigo_ingreso(self):
        self.contador_ingresos += 1
        return f"B01-{self.contador_ingresos:04d}"
    
    def agregar_venta_al_historial(self, codigo_venta, fecha, productos, total):
        venta = {
            "codigo": codigo_venta,
            "fecha": fecha,
            "productos": productos,
            "total": total,
            "tipo": "venta"
        }
        self.historial_ventas.append(venta)
    
    def agregar_ingreso_al_historial(self, codigo_ingreso, fecha, producto, cantidad, precio):
        ingreso = {
            "codigo": codigo_ingreso,
            "fecha": fecha,
            "producto": producto,
            "cantidad": cantidad,
            "precio": precio,
            "tipo": "ingreso"
        }
        self.historial_ingresos.append(ingreso)
    
    def obtener_historial_ventas(self):
        return self.historial_ventas
    
    def obtener_historial_ingresos(self):
        return self.historial_ingresos
    
    def obtener_historial_completo(self):
        historial_completo = []
        historial_completo.extend(self.historial_ventas)
        historial_completo.extend(self.historial_ingresos)
        return sorted(historial_completo, key=lambda x: x["fecha"], reverse=True)
    
    def buscar_ventas_por_fecha(self, fecha_inicio, fecha_fin):
        resultados = []
        for venta in self.historial_ventas:
            fecha_venta = datetime.datetime.strptime(venta["fecha"], "%d/%m/%Y %H:%M:%S")
            if fecha_inicio <= fecha_venta <= fecha_fin:
                resultados.append(venta)
        return resultados
    
    def agregar_producto(self, codigo, nombre, precio, stock):
        # Verificar si ya existe un producto con el mismo código
        for producto in self.productos_disponibles:
            if producto["codigo"] == codigo:
                return False, "Ya existe un producto con ese código"
        
        # Agregar nuevo producto
        nuevo_producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": float(precio),
            "stock": int(stock)
        }
        self.productos_disponibles.append(nuevo_producto)
        return True, "Producto agregado correctamente"
    
    def actualizar_producto(self, codigo, nombre, precio, stock):
        # Buscar producto por código
        for i, producto in enumerate(self.productos_disponibles):
            if producto["codigo"] == codigo:
                # Actualizar datos
                self.productos_disponibles[i]["nombre"] = nombre
                self.productos_disponibles[i]["precio"] = float(precio)
                self.productos_disponibles[i]["stock"] = int(stock)
                return True, "Producto actualizado correctamente"
        
        return False, "No se encontró el producto con ese código"
    
    def eliminar_producto(self, codigo):
        # Buscar producto por código
        for i, producto in enumerate(self.productos_disponibles):
            if producto["codigo"] == codigo:
                # Eliminar producto
                self.productos_disponibles.pop(i)
                return True, "Producto eliminado correctamente"
        
        return False, "No se encontró el producto con ese código"
    
    def buscar_productos(self, texto, criterio="Todos"):
        resultados = []
        
        if criterio == "Todos" and not texto:
            # Si no hay texto y el criterio es Todos, devolver todos los productos
            return self.productos_disponibles
        
        texto = texto.lower()
        for producto in self.productos_disponibles:
            if criterio == "Código" and texto in producto["codigo"].lower():
                resultados.append(producto)
            elif criterio == "Nombre" and texto in producto["nombre"].lower():
                resultados.append(producto)
            elif criterio == "Todos" and (texto in producto["codigo"].lower() or 
                                        texto in producto["nombre"].lower()):
                resultados.append(producto)
        
        return resultados
