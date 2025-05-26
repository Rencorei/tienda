import datetime
import mysql.connector
from db_config import DatabaseConnection

# Clase principal que maneja los datos y la lógica de negocio de la aplicación
# Implementa el patrón MVC (Modelo-Vista-Controlador) - Componente Modelo
class CajaRegistradoraModel:
    def __init__(self):
        # Inicializar la conexión a la base de datos
        self.db = DatabaseConnection()
        
        # Variables para gestionar la venta actual
        self.total_venta = 0.0
        self.productos_venta = []
        self.usuario_actual = None  # Para almacenar el usuario que ha iniciado sesión
        
        # Cargar productos desde la base de datos
        self.productos_disponibles = self.obtener_todos_productos()
    
    # Métodos de autenticación
    def validar_usuario(self, usuario, password):
        # Usar la contraseña en texto plano para la autenticación
        # Nota: En un entorno de producción, se recomienda usar contraseñas hasheadas
        query = "SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s"
        success, result = self.db.execute_query(query, (usuario, password))
        
        if success and result:
            self.usuario_actual = result[0]  # Guardar los datos del usuario actual
            return True, self.usuario_actual
        else:
            return False, "Usuario o contraseña incorrectos"
    
    def cerrar_sesion(self):
        self.usuario_actual = None
    
    # Genera un código único para cada venta (formato: F01-XXXX)
    def generar_codigo_venta(self):
        query = "SELECT MAX(CAST(SUBSTRING(codigo_venta, 5) AS UNSIGNED)) as ultimo FROM ventas"
        success, result = self.db.execute_query(query)
        
        if success and result and result[0]['ultimo'] is not None:
            ultimo_numero = result[0]['ultimo']
            nuevo_numero = ultimo_numero + 1
        else:
            nuevo_numero = 1
            
        return f"F01-{nuevo_numero:04d}"
    
    # Genera un código único para cada movimiento de inventario (formato: B01-XXXX)
    def generar_codigo_movimiento(self):
        query = "SELECT MAX(CAST(SUBSTRING(codigo_mov, 5) AS UNSIGNED)) as ultimo FROM movimientos_inventario"
        success, result = self.db.execute_query(query)
        
        if success and result and result[0]['ultimo'] is not None:
            ultimo_numero = result[0]['ultimo']
            nuevo_numero = ultimo_numero + 1
        else:
            nuevo_numero = 1
            
        return f"B01-{nuevo_numero:04d}"
    
    # Registra una venta completada en la base de datos
    def agregar_venta_al_historial(self, codigo_venta, fecha, productos, total):
        # Convertir fecha de string a objeto datetime si es necesario
        if isinstance(fecha, str):
            fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")
        
        # Insertar en la tabla ventas
        query_venta = "INSERT INTO ventas (codigo_venta, usuario_id, fecha, total) VALUES (%s, %s, %s, %s)"
        success, result = self.db.execute_query(query_venta, (codigo_venta, self.usuario_actual['id'], fecha, total))
        
        if not success:
            return False, "Error al registrar la venta"
        
        # Obtener el ID de la venta insertada
        query_id = "SELECT id FROM ventas WHERE codigo_venta = %s"
        success, result = self.db.execute_query(query_id, (codigo_venta,))
        
        if not success or not result:
            return False, "Error al obtener el ID de la venta"
        
        venta_id = result[0]['id']
        
        # Insertar cada producto en la tabla venta_items
        for item in productos:
            # Obtener el ID del producto
            query_producto = "SELECT id FROM productos WHERE nombre = %s"
            success, result_producto = self.db.execute_query(query_producto, (item['producto'],))
            
            if not success or not result_producto:
                continue  # Saltar este producto si no se encuentra
            
            producto_id = result_producto[0]['id']
            
            # Insertar en venta_items
            query_item = "INSERT INTO venta_items (venta_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
            self.db.execute_query(query_item, (venta_id, producto_id, item['cantidad'], item['precio']))
            
            # Registrar movimiento de inventario
            self.registrar_movimiento_inventario(producto_id, 'venta', item['cantidad'], item['precio'])
        
        return True, "Venta registrada correctamente"
    
    # Registra un movimiento de inventario
    def registrar_movimiento_inventario(self, producto_id, tipo, cantidad, precio_unitario):
        codigo_mov = self.generar_codigo_movimiento()
        query = "INSERT INTO movimientos_inventario (codigo_mov, producto_id, tipo, cantidad, precio_unitario) VALUES (%s, %s, %s, %s, %s)"
        self.db.execute_query(query, (codigo_mov, producto_id, tipo, cantidad, precio_unitario))
    
    # Métodos para obtener datos del historial
    def obtener_historial_ventas(self):
        query = """
        SELECT v.id, v.codigo_venta as codigo, v.fecha, v.total, u.usuario as vendedor
        FROM ventas v
        JOIN usuarios u ON v.usuario_id = u.id
        ORDER BY v.fecha DESC
        """
        success, result = self.db.execute_query(query)
        
        if success:
            # Para cada venta, obtener sus productos
            for venta in result:
                query_items = """
                SELECT vi.cantidad, vi.precio_unitario, vi.subtotal, p.nombre as producto
                FROM venta_items vi
                JOIN productos p ON vi.producto_id = p.id
                WHERE vi.venta_id = %s
                """
                success_items, items = self.db.execute_query(query_items, (venta['id'],))
                
                if success_items:
                    venta['productos'] = items
                else:
                    venta['productos'] = []
            
            return result
        else:
            return []
    
    # Obtener todos los productos de la base de datos
    def obtener_todos_productos(self):
        query = "SELECT id, codigo, nombre, precio_unitario as precio, stock FROM productos ORDER BY nombre"
        success, result = self.db.execute_query(query)
        
        if success:
            return result
        else:
            return []
    
    # Filtra ventas por rango de fechas
    def buscar_ventas_por_fecha(self, fecha_inicio, fecha_fin):
        query = """
        SELECT v.id, v.codigo_venta as codigo, v.fecha, v.total, u.usuario as vendedor
        FROM ventas v
        JOIN usuarios u ON v.usuario_id = u.id
        WHERE v.fecha BETWEEN %s AND %s
        ORDER BY v.fecha DESC
        """
        success, result = self.db.execute_query(query, (fecha_inicio, fecha_fin))
        
        if success:
            # Para cada venta, obtener sus productos
            for venta in result:
                query_items = """
                SELECT vi.cantidad, vi.precio_unitario, vi.subtotal, p.nombre as producto
                FROM venta_items vi
                JOIN productos p ON vi.producto_id = p.id
                WHERE vi.venta_id = %s
                """
                success_items, items = self.db.execute_query(query_items, (venta['id'],))
                
                if success_items:
                    venta['productos'] = items
                else:
                    venta['productos'] = []
            
            return result
        else:
            return []
    
    # CRUD de productos - Agregar nuevo producto al inventario
    def agregar_producto(self, codigo, nombre, precio, stock):
        query = "INSERT INTO productos (codigo, nombre, precio_unitario, stock) VALUES (%s, %s, %s, %s)"
        success, result = self.db.execute_query(query, (codigo, nombre, float(precio), int(stock)))
        
        if success:
            # Actualizar la lista de productos disponibles
            self.productos_disponibles = self.obtener_todos_productos()
            return True, "Producto agregado correctamente"
        else:
            return False, "Error al agregar el producto"
    
    # CRUD de productos - Actualizar un producto existente
    def actualizar_producto(self, codigo, nombre, precio, stock):
        query = "UPDATE productos SET nombre = %s, precio_unitario = %s, stock = %s WHERE codigo = %s"
        success, result = self.db.execute_query(query, (nombre, float(precio), int(stock), codigo))
        
        if success and result > 0:
            # Actualizar la lista de productos disponibles
            self.productos_disponibles = self.obtener_todos_productos()
            return True, "Producto actualizado correctamente"
        else:
            return False, "No se encontró el producto con ese código"
    
    # CRUD de productos - Eliminar un producto
    def eliminar_producto(self, codigo):
        # Primero verificar si el producto está en alguna venta
        query_check = """
        SELECT COUNT(*) as count FROM venta_items vi
        JOIN productos p ON vi.producto_id = p.id
        WHERE p.codigo = %s
        """
        success, result = self.db.execute_query(query_check, (codigo,))
        
        if success and result[0]['count'] > 0:
            return False, "No se puede eliminar el producto porque está asociado a ventas"
        
        # Si no está en ventas, proceder a eliminar
        query = "DELETE FROM productos WHERE codigo = %s"
        success, result = self.db.execute_query(query, (codigo,))
        
        if success and result > 0:
            # Actualizar la lista de productos disponibles
            self.productos_disponibles = self.obtener_todos_productos()
            return True, "Producto eliminado correctamente"
        else:
            return False, "No se encontró el producto con ese código"
    
    # Busca productos según criterio (Código, Nombre o Todos)
    def buscar_productos(self, texto, criterio="Todos"):
        if criterio == "Todos" and not texto:
            # Si no hay texto y el criterio es Todos, devolver todos los productos
            return self.obtener_todos_productos()
        
        if criterio == "Código":
            query = "SELECT id, codigo, nombre, precio_unitario as precio, stock FROM productos WHERE codigo LIKE %s ORDER BY nombre"
            params = (f"%{texto}%",)
        elif criterio == "Nombre":
            query = "SELECT id, codigo, nombre, precio_unitario as precio, stock FROM productos WHERE nombre LIKE %s ORDER BY nombre"
            params = (f"%{texto}%",)
        else:  # Todos
            query = "SELECT id, codigo, nombre, precio_unitario as precio, stock FROM productos WHERE codigo LIKE %s OR nombre LIKE %s ORDER BY nombre"
            params = (f"%{texto}%", f"%{texto}%")
        
        success, result = self.db.execute_query(query, params)
        
        if success:
            return result
        else:
            return []
