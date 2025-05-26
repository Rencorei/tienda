-- Base de datos
CREATE DATABASE IF NOT EXISTS caja_registradora;
USE caja_registradora;

-- Usuarios 
CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(50) NOT NULL UNIQUE,
  contraseña VARCHAR(255) NOT NULL,   -- hashéala antes de guardar
  rol ENUM('admin','cajero') NOT NULL DEFAULT 'cajero'
);

-- Productos
CREATE TABLE productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(20) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  precio_unitario DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL DEFAULT 0,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ventas (ahora sí vinculada al usuario que vendió)
CREATE TABLE ventas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo_venta VARCHAR(20) NOT NULL UNIQUE,
  usuario_id INT NOT NULL,
  fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total DECIMAL(12,2) NOT NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Detalle de Venta
CREATE TABLE venta_items (
  venta_id INT NOT NULL,
  producto_id INT NOT NULL,
  cantidad INT NOT NULL,
  precio_unitario DECIMAL(10,2) NOT NULL,
  subtotal DECIMAL(12,2) AS (cantidad * precio_unitario) STORED,
  PRIMARY KEY (venta_id, producto_id),
  FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Movimientos de Inventario (ingresos y egresos)
CREATE TABLE movimientos_inventario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo_mov VARCHAR(20) NOT NULL UNIQUE,
  producto_id INT NOT NULL,
  tipo ENUM('ingreso','venta') NOT NULL,
  cantidad INT NOT NULL,
  precio_unitario DECIMAL(10,2),    -- para reflejar tu historial de ingresos
  fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Registros de Tabla productos
INSERT INTO productos (codigo, nombre, precio_unitario, stock) VALUES
  ('LAP001', 'Laptop HP 15',           2200.00, 10),
  ('MON001', 'Monitor Dell 24"',         450.00, 15),
  ('TEC001', 'Teclado Logitech K120',    120.00, 20),
  ('MOU001', 'Mouse Inalámbrico HP',     110.00, 25),
  ('IMP001', 'Impresora Canon MX490',    860.00,  8),
  ('HDD001', 'Disco Duro Externo 1TB',   420.00, 12),
  ('USB001', 'Memoria USB 32GB',          25.00, 30),
  ('WEB001', 'Webcam Logitech C920',     140.00, 18),
  ('AUD001', 'Auriculares Sony WH-1000XM4',320.00,15),
  ('ROU001', 'Router TP‑Link AC1200',     86.00, 22);
  
INSERT INTO usuarios (usuario, contraseña, rol) VALUES
('admin',    '1234',       'admin'),
('cajera01', 'ventas01',   'cajero'),
('cajero02', 'ventas02',   'cajero');


SELECT*FROM productos;
SELECT*FROM usuarios;
SELECT*FROM movimientos_inventario;
SELECT*FROM venta_items;
