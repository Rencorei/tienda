class CajaRegistradoraModel:
    def __init__(self):
        self.productos_disponibles = [
            {"nombre": "Laptop HP 15", "precio": 2200.00},
            {"nombre": "Monitor Dell 24\"", "precio": 450.00},
            {"nombre": "Teclado Logitech K120", "precio": 120.00},
            {"nombre": "Mouse Inalámbrico HP", "precio": 110.00},
            {"nombre": "Impresora Canon MX490", "precio": 860.00},
            {"nombre": "Disco Duro Externo 1TB", "precio": 420.00},
            {"nombre": "Memoria USB 32GB", "precio": 25.00},
            {"nombre": "Webcam Logitech C920", "precio": 140.00},
            {"nombre": "Auriculares Sony WH-1000XM4", "precio": 320.00},
            {"nombre": "Router TP-Link AC1200", "precio": 86.00}
        ]
        self.total_venta = 0.0
        self.productos_venta = []
