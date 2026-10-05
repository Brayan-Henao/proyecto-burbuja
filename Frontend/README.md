# Burbuja - Frontend

Frontend de la plataforma web de **Burbuja**, un negocio dedicado a la venta de regalos personalizados.

Este proyecto corresponde a la interfaz de usuario desarrollada con React y Vite, conectada al backend mediante una API REST desarrollada con Flask.

## Tecnologías

- React
- Vite
- JavaScript
- HTML5
- CSS3
- React Router
- Fetch API

## Funcionalidades actuales

- Página de inicio de Burbuja.
- Navegación entre las diferentes secciones de la tienda.
- Visualización de productos obtenidos desde la API.
- Página de detalle de cada producto.
- Visualización de información, precio y disponibilidad.
- Personalización de productos.
- Ingreso de texto para grabados.
- Ingreso de mensajes para tarjetas.
- Selección de fotografías para personalización.
- Vista previa de la fotografía seleccionada.
- Envío de fotografías al backend.
- Integración con el módulo de personalizaciones del backend.
- Diseño responsive para diferentes tamaños de pantalla.

## Estructura principal

```text
src/
├── components/
│   ├── Categorias.jsx
│   ├── Footer.jsx
│   ├── Header.jsx
│   ├── Hero.jsx
│   ├── PersonalizacionCTA.jsx
│   ├── PorQueBurbuja.jsx
│   ├── ProductoDetalle.jsx
│   └── ProductosDestacados.jsx
│
├── services/
│   ├── personalizacionesService.js
│   └── productosService.js
│
├── App.jsx
├── main.jsx
├── App.css
└── index.css

public/
└── videos/
    ├── video1.mp4
    ├── video2.mp4
    └── video3.mp4
