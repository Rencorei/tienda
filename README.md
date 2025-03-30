# Sistema de Caja Registradora

Sistema de gestión de ventas e inventario desarrollado en Python con interfaz gráfica Tkinter.

## Características Principales

### 1. Módulo de Ventas
- Registro de ventas con múltiples productos
- Cálculo automático de totales
- Generación de tickets de venta
- Control de stock automático
- Códigos de venta únicos (F01-XXXX)

### 2. Módulo de Inventario
- Gestión completa de productos
- Control de stock
- Registro de ingresos de productos
- Códigos de ingreso únicos (B01-XXXX)
- Búsqueda de productos por código o nombre

### 3. Historial de Movimientos
- Registro de todas las ventas realizadas
- Registro de todos los ingresos de productos
- Filtrado por fecha
- Visualización detallada de cada movimiento
- Códigos únicos para cada operación

## Requisitos del Sistema

- Python 3.x
- Tkinter (incluido en la instalación estándar de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Navegar al directorio del proyecto:
```bash
cd caja-registradora
```

3. Ejecutar el programa:
```bash
python main.py
```

## Credenciales de Acceso

- Usuario: admin
- Contraseña: 1234

## Estructura del Proyecto

```
caja-registradora/
├── main.py              # Punto de entrada de la aplicación
├── controller.py        # Controlador de la aplicación
├── model.py            # Modelo de datos
├── view.py             # Interfaz de usuario
└── README.md           # Documentación
```

## Funcionalidades Detalladas

### Gestión de Ventas
- Selección de productos desde una lista desplegable
- Ingreso de cantidades
- Cálculo automático de subtotales y total
- Eliminación de productos de la venta
- Generación de tickets de venta con código único

### Gestión de Inventario
- Agregar nuevos productos
- Editar productos existentes
- Eliminar productos
- Control de stock automático
- Registro de ingresos de productos

### Historial de Movimientos
- Visualización de todas las operaciones
- Filtrado por fecha
- Detalles de cada operación:
  - Código único
  - Fecha y hora
  - Producto
  - Cantidad
  - Precio unitario
  - Total

## Notas de Uso

1. Al realizar una venta:
   - El sistema verifica el stock disponible
   - Genera un código único de venta
   - Actualiza automáticamente el inventario
   - Registra la operación en el historial

2. Al agregar productos al inventario:
   - Se genera un código único de ingreso
   - Se actualiza el stock
   - Se registra la operación en el historial

3. El historial muestra:
   - Ventas con código F01-XXXX
   - Ingresos con código B01-XXXX
   - Cantidades positivas para ventas
   - Cantidades con "+" para ingresos

## Soporte

Para reportar problemas o solicitar ayuda, por favor crear un issue en el repositorio del proyecto.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 