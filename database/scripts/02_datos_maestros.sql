USE proveedores_db;

INSERT INTO tipo_usuario (nombre) VALUES
    ('Administrador'), ('Tradicional'), ('Esporadico');

INSERT INTO departamento (nombre) VALUES
    ('Amazonas'), ('Antioquia'), ('Arauca'), ('Atlántico'), ('Bolívar'),
    ('Boyacá'), ('Caldas'), ('Caquetá'), ('Casanare'), ('Cauca'),
    ('Cesar'), ('Chocó'), ('Córdoba'), ('Cundinamarca'), ('Guainía'),
    ('Guaviare'), ('Huila'), ('La Guajira'), ('Magdalena'), ('Meta'),
    ('Nariño'), ('Norte de Santander'), ('Putumayo'), ('Quindío'), ('Risaralda'),
    ('San Andrés y Providencia'), ('Santander'), ('Sucre'), ('Tolima'),
    ('Valle del Cauca'), ('Vaupés'), ('Vichada'), ('Bogotá D.C.');

INSERT INTO ciudad (nombre, id_departamento)
SELECT v.ciudad, d.id_departamento
FROM (
    SELECT 'Leticia' AS ciudad, 'Amazonas' AS depto
    UNION ALL SELECT 'Medellín', 'Antioquia'
    UNION ALL SELECT 'Rionegro', 'Antioquia'
    UNION ALL SELECT 'Arauca', 'Arauca'
    UNION ALL SELECT 'Barranquilla', 'Atlántico'
    UNION ALL SELECT 'Cartagena', 'Bolívar'
    UNION ALL SELECT 'Tunja', 'Boyacá'
    UNION ALL SELECT 'Manizales', 'Caldas'
    UNION ALL SELECT 'Florencia', 'Caquetá'
    UNION ALL SELECT 'Yopal', 'Casanare'
    UNION ALL SELECT 'Popayán', 'Cauca'
    UNION ALL SELECT 'Valledupar', 'Cesar'
    UNION ALL SELECT 'Quibdó', 'Chocó'
    UNION ALL SELECT 'Montería', 'Córdoba'
    UNION ALL SELECT 'Soacha', 'Cundinamarca'
    UNION ALL SELECT 'Girardot', 'Cundinamarca'
    UNION ALL SELECT 'Inírida', 'Guainía'
    UNION ALL SELECT 'San José del Guaviare', 'Guaviare'
    UNION ALL SELECT 'Neiva', 'Huila'
    UNION ALL SELECT 'Riohacha', 'La Guajira'
    UNION ALL SELECT 'Santa Marta', 'Magdalena'
    UNION ALL SELECT 'Villavicencio', 'Meta'
    UNION ALL SELECT 'Pasto', 'Nariño'
    UNION ALL SELECT 'Cúcuta', 'Norte de Santander'
    UNION ALL SELECT 'Mocoa', 'Putumayo'
    UNION ALL SELECT 'Armenia', 'Quindío'
    UNION ALL SELECT 'Calarcá', 'Quindío'
    UNION ALL SELECT 'La Tebaida', 'Quindío'
    UNION ALL SELECT 'Montenegro', 'Quindío'
    UNION ALL SELECT 'Circasia', 'Quindío'
    UNION ALL SELECT 'Pereira', 'Risaralda'
    UNION ALL SELECT 'Dosquebradas', 'Risaralda'
    UNION ALL SELECT 'San Andrés', 'San Andrés y Providencia'
    UNION ALL SELECT 'Bucaramanga', 'Santander'
    UNION ALL SELECT 'Sincelejo', 'Sucre'
    UNION ALL SELECT 'Ibagué', 'Tolima'
    UNION ALL SELECT 'Cali', 'Valle del Cauca'
    UNION ALL SELECT 'Palmira', 'Valle del Cauca'
    UNION ALL SELECT 'Buenaventura', 'Valle del Cauca'
    UNION ALL SELECT 'Mitú', 'Vaupés'
    UNION ALL SELECT 'Puerto Carreño', 'Vichada'
    UNION ALL SELECT 'Bogotá', 'Bogotá D.C.'
) AS v
JOIN departamento d ON d.nombre = v.depto;