# Backend de Burbuja

API REST desarrollada con **Python y Flask** para la gestión de una plataforma de venta de regalos personalizados.

El backend proporciona los servicios necesarios para gestionar usuarios, productos, opciones de productos, personalizaciones, fotografías, órdenes y pagos, utilizando **MySQL** como sistema de base de datos.

---

# Descripción

**Burbuja** es una plataforma web orientada a la venta de regalos personalizados.

El backend fue desarrollado para digitalizar diferentes procesos del negocio, permitiendo gestionar productos y sus características, personalizaciones realizadas por los clientes, fotografías, pedidos, inventario y el flujo inicial de pagos.

El proyecto utiliza una arquitectura organizada por dominios y una API REST que permite la comunicación con el frontend desarrollado en React.

Actualmente el proyecto se encuentra en desarrollo como parte de mi proceso de formación como desarrollador de software y como proyecto aplicado a un negocio real.

---

# Tecnologías utilizadas

- Python
- Flask
- SQLAlchemy
- MySQL
- PyMySQL
- Flask-Migrate
- Alembic
- Marshmallow
- JWT
- Git
- GitHub

---

# Arquitectura

El backend utiliza una **arquitectura organizada por dominios**.

Cada dominio separa las responsabilidades principales del sistema:

- **Modelos:** representan las entidades y relaciones de la base de datos.
- **Repositorios:** gestionan las operaciones de acceso a datos.
- **Servicios:** contienen la lógica de negocio y las validaciones.
- **Controladores:** reciben las peticiones HTTP y construyen las respuestas de la API.
- **DTOs:** validan y estructuran los datos recibidos desde las peticiones.

Esta organización permite mantener el código separado por responsabilidades y facilita su mantenimiento y crecimiento.

---

# Dominios implementados

Actualmente el backend cuenta con los siguientes dominios:

## Usuarios

Permite gestionar:

- Registro de usuarios.
- Inicio de sesión.
- Autenticación mediante JWT.
- Roles de usuario y administrador.
- Protección de endpoints administrativos.

## Productos

Permite gestionar:

- Información de productos.
- Precio.
- Stock.
- Disponibilidad.
- Categorías.
- Configuración de personalización.
- Imágenes de productos.

## Opciones de productos

Permite definir características adicionales de los productos, por ejemplo:

- Colores.
- Accesorios.
- Opciones dependientes de otras opciones.
- Activación o desactivación de opciones.

## Personalizaciones

Permite gestionar:

- Grabados personalizados.
- Mensajes para tarjetas.
- Fotografías proporcionadas por el cliente.
- Opciones seleccionadas para la personalización.

Las fotografías de personalización son almacenadas mediante el sistema de archivos del backend.

## Órdenes

Permite gestionar:

- Creación de órdenes.
- Productos incluidos en cada orden.
- Cantidades.
- Precio unitario.
- Precio del grabado.
- Subtotal.
- Estado de la orden.
- Validación de stock.
- Asociación entre productos y personalizaciones.

## Pagos

El backend cuenta con un módulo preparado para el flujo de pagos mediante una pasarela externa.

Actualmente permite:

- Crear registros de pago.
- Generar referencias únicas.
- Asociar pagos con órdenes.
- Consultar pagos.
- Generar los datos necesarios para el checkout.
- Generar la firma de integridad para Wompi.

La integración completa con la pasarela de pagos y la confirmación mediante webhook forman parte de las siguientes etapas del proyecto.

---

# Seguridad

El backend utiliza **JWT (JSON Web Tokens)** para la autenticación de usuarios.

Los endpoints protegidos pueden requerir:

- Token de autenticación.
- Identificación del usuario.
- Rol de administrador cuando corresponde.

También se realizan validaciones de permisos para evitar que un usuario consulte o modifique información perteneciente a otro usuario.

---

# Validación de datos

Las solicitudes de la API utilizan **Marshmallow** para validar los datos recibidos.

Esto permite controlar:

- Campos obligatorios.
- Tipos de datos.
- Longitud de textos.
- Valores permitidos.
- Datos inválidos antes de ejecutar la lógica de negocio.

---

# Base de datos

El proyecto utiliza **MySQL** como sistema de gestión de base de datos.

La comunicación con la base de datos se realiza mediante:

- SQLAlchemy.
- PyMySQL.

La estructura de la base de datos se administra mediante **Flask-Migrate y Alembic**, permitiendo versionar los cambios realizados sobre los modelos.

---

# API REST

Los diferentes dominios están expuestos mediante endpoints REST organizados por recursos.

Ejemplos:

```text
/api/v1/usuarios
/api/v1/productos
/api/v1/opciones-productos
/api/v1/personalizaciones
/api/v1/ordenes
/api/v1/pagos
