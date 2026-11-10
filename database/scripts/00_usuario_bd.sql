CREATE USER IF NOT EXISTS 'app_proveedores'@'localhost' IDENTIFIED BY 'Proveedores2026*';
CREATE USER IF NOT EXISTS 'app_proveedores'@'127.0.0.1' IDENTIFIED BY 'Proveedores2026*';

GRANT ALL PRIVILEGES ON proveedores_db.* TO 'app_proveedores'@'localhost';
GRANT ALL PRIVILEGES ON proveedores_db.* TO 'app_proveedores'@'127.0.0.1';

FLUSH PRIVILEGES;
