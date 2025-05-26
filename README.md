# Caja Registradora Tienda

Aplicación de caja registradora para tiendas, desarrollada en Python usando el patrón MVC, con interfaz gráfica en Tkinter y conexión a base de datos MySQL.

## Características

- **Gestión de usuarios:** Login seguro con roles (admin/cajero).
- **Inventario:** Alta, edición, eliminación y búsqueda de productos.
- **Ventas:** Registro de ventas, control de stock y generación de tickets.
- **Historial:** Consulta de ventas y movimientos de inventario por fecha.
- **Interfaz amigable:** Visual moderna y fácil de usar.
- **Persistencia:** Todos los datos se almacenan en MySQL.

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación.
- `controller.py`: Lógica de control y comunicación entre vista y modelo.
- `model.py`: Acceso y lógica de datos (MySQL).
- `view.py`: Interfaz gráfica de usuario (Tkinter).
- `db_config.py`: Configuración y utilidades para la base de datos.
- `caja_registradoraBD.sql`: Script para crear y poblar la base de datos.

## Requisitos

- Python 3.10+
- MySQL Server
- Paquetes Python:
  - `mysql-connector-python`
  - `tkinter` (incluido en la mayoría de instalaciones de Python)

Instala dependencias con:
```sh
pip install mysql-connector-python
```

## Instalación y Configuración

1. **Clona o descarga este repositorio.**

2. **Crea la base de datos:**
   - Abre MySQL Workbench, consola o phpMyAdmin.
   - Ejecuta el script [`caja_registradoraBD.sql`](caja_registradoraBD.sql).

3. **Configura la conexión a la base de datos:**
   - Edita [`db_config.py`](db_config.py) si tu usuario, contraseña o puerto de MySQL son diferentes.

4. **Ejecuta la aplicación:**
   ```sh
   python main.py
   ```

## Uso

1. **Inicia sesión** con uno de los usuarios predefinidos:
   - admin / 1234 (rol admin)
   - cajera01 / ventas01 (rol cajero)
   - cajero02 / ventas02 (rol cajero)

2. **Navega** por los módulos:
   - **Ventas:** Agrega productos, finaliza ventas y genera tickets.
   - **Inventario:** Agrega, edita, elimina y busca productos.
   - **Historial:** Consulta ventas y movimientos por fecha.

## Estructura de la Base de Datos

- **usuarios:** Usuarios del sistema (con roles).
- **productos:** Inventario de productos.
- **ventas:** Registro de ventas.
- **venta_items:** Detalle de productos vendidos por venta.
- **movimientos_inventario:** Historial de ingresos y ventas de productos.

Consulta el archivo [`caja_registradoraBD.sql`](caja_registradoraBD.sql) para detalles de las tablas y datos de ejemplo.

## Capturas de Pantalla

*(Agrega aquí imágenes de la interfaz si lo deseas)*

## Créditos

Desarrollado por SkynetSoft Code  
Hecho con café y algo de sarcasmo ☕️

---

**Licencia:** MIT