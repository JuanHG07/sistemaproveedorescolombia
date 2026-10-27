# Proyecto Final - Bases de Datos I (Universidad del Quindio)

Aplicacion de escritorio (Python + Tkinter + MySQL), patron MVC con DAO y DTO, sin frameworks.

## Puesta en marcha
1. `python -m venv .venv` y activarlo.
2. `pip install -r requirements.txt`
3. Copiar `.env.example` a `.env` y ajustar credenciales.
4. En MySQL 8.0.16+ ejecutar en orden los scripts de `database/scripts/` (01 a 04).
5. `python main.py`

Usuario inicial: `admin` / `Admin123*` (cambiar la clave tras el primer ingreso).

## Capas
- `modelo/`: DTO + DAO (unico lugar con SQL).
- `controlador/`: validaciones, permisos por rol, orquesta DAO.
- `vista/`: Tkinter, sin SQL ni reglas de negocio.
