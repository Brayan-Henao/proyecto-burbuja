# Burbuja Backend

API REST desarrollada con **Python, Flask y MySQL** para la gestión de una tienda de regalos personalizados.

# Descripción

Burbuja es un proyecto de comercio electrónico especializado en regalos personalizados como llaveros, pulseras y accesorios con fotograbado.

El sistema permite administrar usuarios, productos, accesorios y pedidos personalizados mediante una API REST segura utilizando autenticación JWT.

Actualmente el proyecto se encuentra en desarrollo y hace parte de mi proceso de formación como desarrollador de software.

---

# Tecnologías utilizadas

* Python
* Flask
* SQLAlchemy
* MySQL
* Flask-Migrate (Alembic)
* JWT
* Git
* GitHub

---

# Arquitectura

El proyecto sigue una arquitectura por dominios separando cada módulo en:

* Modelos
* Repositorios
* Servicios
* Controladores

Esto facilita el mantenimiento y el crecimiento del proyecto.

---

# Funcionalidades implementadas

* Registro de usuarios
* Inicio de sesión con JWT
* Roles de usuario y administrador
* Gestión de productos
* Gestión de accesorios
* Creación de pedidos
* Personalización de productos
* Gestión de estados de pedidos
* Migraciones con Alembic

---

# Estructura del proyecto

```
app/
 ├── dominios/
 ├── seguridad/
 ├── extensiones.py
 ├── config.py

migrations/

run.py
requirements.txt
```

---

# Autor

**Brayan Henao**

Proyecto real actualmente en desarrollo, creado como parte de mi proceso de formación en desarrollo de software utilizando Python, Flask y MySQL.
