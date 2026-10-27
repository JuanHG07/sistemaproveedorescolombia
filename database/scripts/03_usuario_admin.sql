USE proveedores_db;

-- Unico Administrador. Clave inicial: Admin123*  (hash bcrypt). Cambiarla despues.
INSERT INTO usuario (nombre_completo, username, password_hash, id_tipo, estado)
VALUES ('Administrador del Sistema', 'admin',
        '$2b$12$vFxT.EtiPkE9a3JeyQjf5O/RnIyLTY9GI2xwV1f7Gnpy8j3Vix2eS',
        (SELECT id_tipo FROM tipo_usuario WHERE nombre = 'Administrador'), 'A');
