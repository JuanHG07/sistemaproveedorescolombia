# Proyecto Final - Bases de Datos I (Universidad del Quindio)

Aplicacion de escritorio (Python + Tkinter + MySQL), patron MVC con DAO y DTO, sin frameworks.

## Puesta en marcha
1. `python -m venv .venv` y activarlo.
2. `pip install -r requirements.txt`
3. Con el usuario `root` de MySQL ejecutar `database/scripts/00_usuario_bd.sql` (crea el usuario `app_proveedores`).
4. Con el usuario `app_proveedores` ejecutar en orden los scripts 01 a 04 de `database/scripts/` (MySQL 8.0.16+).
5. Copiar `.env.example` a `.env` y ajustar `DB_PORT` al puerto de su servidor MySQL.
6. `python main.py`

Usuario inicial de la aplicacion: `admin` / `Admin123*` (cambiar la clave tras el primer ingreso).

## Reiniciar la base de datos
Eliminar el schema `proveedores_db` y volver a ejecutar los scripts 01 a 04.

## Capas
- `config/`: lectura de la configuracion desde `.env`.
- `modelo/`: DTO + DAO (unico lugar con SQL).
- `controlador/`: validaciones, permisos por rol, orquesta DAO.
- `vista/`: Tkinter, sin SQL ni reglas de negocio.
