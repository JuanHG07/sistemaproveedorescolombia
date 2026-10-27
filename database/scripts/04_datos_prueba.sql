USE proveedores_db;

INSERT INTO categoria (nombre, descripcion) VALUES
    ('Lacteos', 'Leche, queso y derivados'),
    ('Aseo', 'Productos de limpieza'),
    ('Granos', 'Arroz, frijol, lentejas'),
    ('Bebidas', 'Gaseosas, jugos y agua');

INSERT INTO producto (codigo, nombre, descripcion, unidad_medida, id_categoria) VALUES
    ('LAC001', 'Leche entera 1L', 'Leche UHT', 'unidad', (SELECT id_categoria FROM categoria WHERE nombre='Lacteos')),
    ('ASE001', 'Detergente 1kg', 'Detergente en polvo', 'unidad', (SELECT id_categoria FROM categoria WHERE nombre='Aseo')),
    ('GRA001', 'Arroz 500g', 'Arroz blanco', 'unidad', (SELECT id_categoria FROM categoria WHERE nombre='Granos')),
    ('BEB001', 'Jugo de naranja 1L', 'Jugo natural', 'unidad', (SELECT id_categoria FROM categoria WHERE nombre='Bebidas'));

INSERT INTO proveedor (nit, razon_social, contacto, telefono, correo, direccion, id_ciudad) VALUES
    ('900111222-1', 'Distribuidora Andina SAS', 'Laura Gomez', '3001112233', 'ventas@andina.co', 'Cra 14 # 10-20',
        (SELECT id_ciudad FROM ciudad WHERE nombre='Armenia')),
    ('900333444-5', 'Alimentos del Valle SA', 'Carlos Ruiz', '3104445566', 'pedidos@valle.co', 'Calle 5 # 38-10',
        (SELECT id_ciudad FROM ciudad WHERE nombre='Cali')),
    ('900555666-7', 'Aseo Total Ltda', 'Marta Lopez', '3207778899', 'info@aseototal.co', 'Av 30 # 45-12',
        (SELECT id_ciudad FROM ciudad WHERE nombre='Medellin'));

INSERT INTO proveedor_producto (id_proveedor, id_producto, precio_unitario, dias_entrega) VALUES
    (1, 1, 3800.00, 2), (1, 3, 2500.00, 3), (2, 1, 3650.00, 4),
    (2, 3, 2400.00, 5), (2, 4, 5200.00, 4), (3, 2, 8900.00, 3), (1, 2, 9100.00, 2);
