-- Requiere MySQL 8.0.16+ (CHECK se aplica desde esa version)
CREATE DATABASE IF NOT EXISTS proveedores_db
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE proveedores_db;

CREATE TABLE departamento (
    id_departamento INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(80) NOT NULL,
    PRIMARY KEY (id_departamento),
    UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE ciudad (
    id_ciudad INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    id_departamento INT NOT NULL,
    PRIMARY KEY (id_ciudad),
    CONSTRAINT fk_ciudad_departamento FOREIGN KEY (id_departamento)
        REFERENCES departamento (id_departamento)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE categoria (
    id_categoria INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255) NULL,
    PRIMARY KEY (id_categoria),
    UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE producto (
    id_producto INT NOT NULL AUTO_INCREMENT,
    codigo VARCHAR(30) NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion VARCHAR(255) NULL,
    unidad_medida VARCHAR(30) NOT NULL,
    id_categoria INT NOT NULL,
    estado CHAR(1) NOT NULL DEFAULT 'A',
    PRIMARY KEY (id_producto),
    UNIQUE (codigo),
    CONSTRAINT ck_producto_estado CHECK (estado IN ('A', 'I')),
    CONSTRAINT fk_producto_categoria FOREIGN KEY (id_categoria)
        REFERENCES categoria (id_categoria)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE proveedor (
    id_proveedor INT NOT NULL AUTO_INCREMENT,
    nit VARCHAR(20) NOT NULL,
    razon_social VARCHAR(150) NOT NULL,
    contacto VARCHAR(100) NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(100) NULL,
    direccion VARCHAR(200) NULL,
    id_ciudad INT NOT NULL,
    estado CHAR(1) NOT NULL DEFAULT 'A',
    PRIMARY KEY (id_proveedor),
    UNIQUE (nit),
    CONSTRAINT ck_proveedor_estado CHECK (estado IN ('A', 'I')),
    CONSTRAINT fk_proveedor_ciudad FOREIGN KEY (id_ciudad)
        REFERENCES ciudad (id_ciudad)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE proveedor_producto (
    id_proveedor INT NOT NULL,
    id_producto INT NOT NULL,
    precio_unitario DECIMAL(12,2) NULL,
    dias_entrega INT NULL,
    PRIMARY KEY (id_proveedor, id_producto),
    CONSTRAINT ck_pp_precio CHECK (precio_unitario >= 0),
    CONSTRAINT ck_pp_dias CHECK (dias_entrega >= 0),
    CONSTRAINT fk_pp_proveedor FOREIGN KEY (id_proveedor)
        REFERENCES proveedor (id_proveedor)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_pp_producto FOREIGN KEY (id_producto)
        REFERENCES producto (id_producto)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE tipo_usuario (
    id_tipo INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_tipo),
    UNIQUE (nombre),
    CONSTRAINT ck_tipo_nombre CHECK (nombre IN ('Administrador', 'Tradicional', 'Esporadico'))
) ENGINE=InnoDB;

CREATE TABLE usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nombre_completo VARCHAR(120) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    id_tipo INT NOT NULL,
    estado CHAR(1) NOT NULL DEFAULT 'A',
    PRIMARY KEY (id_usuario),
    UNIQUE (username),
    CONSTRAINT ck_usuario_estado CHECK (estado IN ('A', 'I')),
    CONSTRAINT fk_usuario_tipo FOREIGN KEY (id_tipo)
        REFERENCES tipo_usuario (id_tipo)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE bitacora (
    id_bitacora INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    fecha_hora_entrada DATETIME NOT NULL,
    fecha_hora_salida DATETIME NULL,
    PRIMARY KEY (id_bitacora),
    CONSTRAINT ck_bitacora_fechas CHECK (fecha_hora_salida >= fecha_hora_entrada),
    CONSTRAINT fk_bitacora_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;
