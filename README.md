# Nexo Gestión

Aplicación de escritorio desarrollada en Python para la gestión comercial de pequeños negocios.

El proyecto permite administrar productos, controlar el inventario, registrar ventas y generar comprobantes en PDF.

## Tecnologías utilizadas

- Python
- SQLite
- Tkinter
- ttkbootstrap
- ReportLab

## Funcionalidades

- Registro y administración de productos.
- Control de precios y stock.
- Búsqueda de productos.
- Registro e historial de ventas.
- Descuento automático del stock al registrar una venta.
- Consulta de ventas y sus detalles.
- Generación de comprobantes en PDF.
- Reportes de ventas.

## Instalación

1. Instalar Python en la computadora.
2. Descargar o clonar este repositorio.
3. Abrir una terminal en la carpeta del proyecto.
4. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

5. Ejecutar la aplicación:

```bash
python main.py
```

## Base de datos

La aplicación utiliza SQLite y crea las tablas necesarias mediante `base_datos.py`. La base de datos `nexo.db` se genera localmente al iniciar la conexión, si todavía no existe.

## Estado del proyecto

En desarrollo. Proyecto personal de aprendizaje, con mejoras continuas en funcionalidades, diseño y corrección de errores.

## Objetivo

Aplicar y fortalecer mis conocimientos de Python mediante el desarrollo de una herramienta práctica para pequeños comercios.
