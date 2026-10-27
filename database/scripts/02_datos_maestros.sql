USE proveedores_db;

INSERT INTO tipo_usuario (nombre) VALUES ('Administrador'), ('Tradicional'), ('Esporadico');

-- Muestra de departamentos y ciudades. TODO: completar con los 32 departamentos y sus municipios.
INSERT INTO departamento (nombre) VALUES
    ('Quindio'), ('Risaralda'), ('Caldas'), ('Valle del Cauca'),
    ('Antioquia'), ('Cundinamarca'), ('Atlantico'), ('Santander');

INSERT INTO ciudad (nombre, id_departamento) VALUES
    ('Armenia', (SELECT id_departamento FROM departamento WHERE nombre = 'Quindio')),
    ('Calarca', (SELECT id_departamento FROM departamento WHERE nombre = 'Quindio')),
    ('La Tebaida', (SELECT id_departamento FROM departamento WHERE nombre = 'Quindio')),
    ('Pereira', (SELECT id_departamento FROM departamento WHERE nombre = 'Risaralda')),
    ('Manizales', (SELECT id_departamento FROM departamento WHERE nombre = 'Caldas')),
    ('Cali', (SELECT id_departamento FROM departamento WHERE nombre = 'Valle del Cauca')),
    ('Medellin', (SELECT id_departamento FROM departamento WHERE nombre = 'Antioquia')),
    ('Bogota D.C.', (SELECT id_departamento FROM departamento WHERE nombre = 'Cundinamarca')),
    ('Barranquilla', (SELECT id_departamento FROM departamento WHERE nombre = 'Atlantico')),
    ('Bucaramanga', (SELECT id_departamento FROM departamento WHERE nombre = 'Santander'));
