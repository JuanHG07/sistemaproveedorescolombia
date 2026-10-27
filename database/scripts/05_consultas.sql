USE proveedores_db;

-- JOIN 1: proveedor + ciudad + departamento
SELECT pr.nit, pr.razon_social, c.nombre AS ciudad, d.nombre AS departamento
FROM proveedor pr
JOIN ciudad c ON c.id_ciudad = pr.id_ciudad
JOIN departamento d ON d.id_departamento = c.id_departamento;

-- JOIN 2: producto + categoria + proveedor_producto + proveedor
SELECT p.codigo, p.nombre, ca.nombre AS categoria, pr.razon_social, pp.precio_unitario, pp.dias_entrega
FROM producto p
JOIN categoria ca ON ca.id_categoria = p.id_categoria
JOIN proveedor_producto pp ON pp.id_producto = p.id_producto
JOIN proveedor pr ON pr.id_proveedor = pp.id_proveedor;

-- JOIN 3: usuario + tipo_usuario + bitacora
SELECT u.username, t.nombre AS tipo, b.fecha_hora_entrada, b.fecha_hora_salida
FROM usuario u
JOIN tipo_usuario t ON t.id_tipo = u.id_tipo
JOIN bitacora b ON b.id_usuario = u.id_usuario;

-- Subconsulta 1: precio por encima del promedio
SELECT p.codigo, p.nombre, pp.precio_unitario
FROM producto p JOIN proveedor_producto pp ON pp.id_producto = p.id_producto
WHERE pp.precio_unitario > (SELECT AVG(precio_unitario) FROM proveedor_producto);

-- Subconsulta 2: proveedores con mas de 2 productos
SELECT pr.nit, pr.razon_social FROM proveedor pr
WHERE (SELECT COUNT(*) FROM proveedor_producto pp WHERE pp.id_proveedor = pr.id_proveedor) > 2;
