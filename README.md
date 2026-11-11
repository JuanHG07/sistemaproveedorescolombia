# SPC - Sistema de Proveedores Colombianos

SPC es una aplicación de escritorio que ayuda a una empresa comercial a saber a qué proveedores puede hacerle pedidos de sus productos. Permite registrar proveedores ubicados en cualquier ciudad de Colombia, los productos que cada uno ofrece con su precio y tiempo de entrega, y las categorías en las que se agrupan esos productos.

El sistema cuenta con un ingreso por usuario y contraseña con tres perfiles. El Administrador, que es uno solo, puede hacer todo y es el único que crea usuarios. El usuario Tradicional registra, modifica y elimina información. El usuario Esporádico solo puede ver consultas y reportes. Cada ingreso y salida queda guardado en una bitácora con su fecha y hora.

La aplicación está organizada en módulos de Entidades (categorías, productos, proveedores, departamentos y ciudades), Transacciones (asignación de productos a proveedores), Consultas, Reportes en PDF con vista previa y Auditoría (usuarios y bitácora). Es el proyecto final de Bases de Datos I de la Universidad del Quindío, desarrollado por Juan Sebastián Hernández y Santiago Ospina Sánchez.

## Tecnologías usadas

El proyecto está hecho en Python sin usar frameworks, siguiendo el patrón Modelo Vista Controlador junto con los patrones DAO y DTO para separar el acceso a la base de datos del resto del programa.

| Tecnología | Versión | Uso en el proyecto |
| --- | --- | --- |
| Python | 3.14 | Lenguaje de programación de toda la aplicación |
| Tkinter y ttk | Incluido en Python | Ventanas, formularios y tablas de la interfaz |
| MySQL Server | 8.0.16 o superior | Motor de base de datos |
| MySQL Workbench | Cualquiera reciente | Ejecución de los scripts y revisión de la base |
| mysql-connector-python | 8.0 o superior | Conexión entre Python y MySQL |
| bcrypt | 4.0 o superior | Guardado seguro de las contraseñas |
| reportlab | 4.0 o superior | Creación de los reportes en PDF |
| PyMuPDF | 1.24 o superior | Vista previa del PDF dentro de la aplicación |
| python-dotenv | 1.0 o superior | Lectura de los datos de conexión desde el archivo `.env` |

## Cómo arrancar la aplicación

Antes de empezar se necesita tener instalado Python 3.14, MySQL Server 8.0.16 o superior con MySQL Workbench, y el repositorio descargado en el computador.

### 1. Crear el usuario de la base de datos

En MySQL Workbench se entra con el usuario `root`, se abre el script `database/scripts/00_usuario_bd.sql` y se ejecuta completo. Este script crea el usuario `app_proveedores` con la clave `Proveedores2026*`, que solo tiene permisos sobre la base de datos del proyecto.

### 2. Crear la base de datos

En Workbench se crea una conexión nueva con el host `127.0.0.1`, el puerto en el que está instalado MySQL (por defecto es 3306), el usuario `app_proveedores` y la clave `Proveedores2026*`. Con esa conexión se ejecutan, uno por uno y en este orden, los scripts `01_schema.sql`, `02_datos_maestros.sql`, `03_usuario_admin.sql` y `04_datos_prueba.sql` de la carpeta `database/scripts`. Al terminar debe aparecer la base `proveedores_db` con nueve tablas.

### 3. Configurar la conexión

En la raíz del proyecto se crea un archivo llamado `.env` con el siguiente contenido, cambiando `DB_PORT` si MySQL usa otro puerto. Este archivo no se sube al repositorio, por eso cada integrante tiene el suyo.

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=app_proveedores
DB_PASSWORD=Proveedores2026*
DB_NAME=proveedores_db
```

### 4. Preparar el entorno de Python

Desde una terminal de tipo Command Prompt ubicada en la raíz del proyecto se crea el entorno virtual, se activa y se instalan las librerías.

```
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

Cuando el entorno está activo, la línea de la terminal empieza con `(.venv)`. Si se usa PowerShell en lugar de Command Prompt, antes de activar el entorno se debe ejecutar `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, que da permiso solo mientras esa terminal esté abierta.

### 5. Ejecutar

Con el entorno activo se inicia la aplicación con el siguiente comando. Se abre la ventana de ingreso, donde se puede entrar con el usuario administrador que aparece en los datos de prueba.

```
python main.py
```

## Reiniciar la base de datos

Si después de hacer pruebas se quiere dejar la base como estaba al principio, en Workbench, con la conexión de `app_proveedores`, se da clic derecho sobre `proveedores_db`, se elige la opción para eliminar el schema (Drop Schema) y se vuelven a ejecutar los scripts 01 a 04 en orden. También se puede ejecutar `DROP DATABASE proveedores_db;` en el editor de consultas antes de correr los scripts. El script 00 no se vuelve a ejecutar, porque el usuario `app_proveedores` no se borra al eliminar la base.

Al reiniciar se pierde todo lo que se haya agregado desde la aplicación, incluidos los usuarios creados y los registros de la bitácora. Los reportes en PDF guardados en la carpeta `reportes_generados` no se borran, porque son archivos del computador y no de la base de datos.

## Datos de prueba

Al ejecutar los scripts la base queda con la siguiente información inicial.

### Usuario de la aplicación

Solo existe el usuario administrador. Los usuarios de tipo Tradicional y Esporádico se crean desde la aplicación en el menú Auditoría, opción Usuarios. Se recomienda cambiar la clave del administrador desde el menú Archivo después del primer ingreso.

| Usuario | Clave | Perfil |
| --- | --- | --- |
| admin | Admin123* | Administrador |

### Datos maestros

La tabla de tipos de usuario tiene los perfiles Administrador, Tradicional y Esporádico. La tabla de departamentos tiene los 32 departamentos de Colombia y Bogotá D.C., y la tabla de ciudades tiene 42 ciudades repartidas entre ellos. El Quindío es el departamento con más ciudades: Armenia, Calarcá, La Tebaida, Montenegro y Circasia.

### Categorías y productos

| Código | Producto | Categoría | Unidad |
| --- | --- | --- | --- |
| LAC001 | Leche entera 1L | Lácteos | unidad |
| ASE001 | Detergente 1kg | Aseo | unidad |
| GRA001 | Arroz 500g | Granos | unidad |
| BEB001 | Jugo de naranja 1L | Bebidas | unidad |

### Proveedores

| NIT | Razón social | Contacto | Teléfono | Ciudad |
| --- | --- | --- | --- | --- |
| 900111222-1 | Distribuidora Andina SAS | Laura Gómez | 3001112233 | Armenia |
| 900333444-5 | Alimentos del Valle SA | Carlos Ruiz | 3104445566 | Cali |
| 900555666-7 | Aseo Total Ltda | Marta López | 3207778899 | Medellín |

### Productos que ofrece cada proveedor

| Proveedor | Producto | Precio unitario | Días de entrega |
| --- | --- | --- | --- |
| Distribuidora Andina SAS | Leche entera 1L | 3.800,00 | 2 |
| Distribuidora Andina SAS | Detergente 1kg | 9.100,00 | 2 |
| Distribuidora Andina SAS | Arroz 500g | 2.500,00 | 3 |
| Alimentos del Valle SA | Leche entera 1L | 3.650,00 | 4 |
| Alimentos del Valle SA | Arroz 500g | 2.400,00 | 5 |
| Alimentos del Valle SA | Jugo de naranja 1L | 5.200,00 | 4 |
| Aseo Total Ltda | Detergente 1kg | 8.900,00 | 3 |
