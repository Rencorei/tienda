import mysql.connector
import hashlib
from mysql.connector import Error

# Clase para gestionar la conexión a la base de datos MySQL
class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '1234',
            'database': 'caja_registradora',
            #'auth_plugin': 'mysql_native_password'
        }
        self.connection = None
    
    # Establece la conexión a la base de datos
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None
    
    # Cierra la conexión a la base de datos
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    # Ejecuta una consulta SQL y devuelve el resultado
    def execute_query(self, query, params=None):
        try:
            connection = self.connect()
            if connection is None:
                return False, "Error de conexión a la base de datos"
            
            cursor = connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = None
            if query.strip().upper().startswith(('SELECT', 'SHOW')):
                result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.rowcount
            
            cursor.close()
            return True, result
        except Error as e:
            if connection:
                connection.rollback()
            return False, f"Error en la consulta: {e}"
        finally:
            self.close()
    
    # Función para hashear contraseñas
    @staticmethod
    def hash_password(password):
        # Utiliza SHA-256 para hashear la contraseña
        return hashlib.sha256(password.encode()).hexdigest()