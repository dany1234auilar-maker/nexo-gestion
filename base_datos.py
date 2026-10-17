
import sqlite3


def conectar():
    conexion = sqlite3.connect("nexo.db")

    # Activar las relaciones entre tablas
    conexion.execute("PRAGMA foreign_keys = ON")

    # Tabla de productos: conserva los productos existentes
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # Tabla principal de ventas
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL
        )
    """)

    # Productos incluidos en cada venta
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            producto_id INTEGER,
            nombre_producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,

            FOREIGN KEY (venta_id)
                REFERENCES ventas(id)
                ON DELETE CASCADE,

            FOREIGN KEY (producto_id)
                REFERENCES productos(id)
                ON DELETE SET NULL
        )
    """)

    conexion.commit()
    return conexion


if __name__ == "__main__":
    conexion = conectar()
    conexion.close()
    print("Base de datos de Nexo Gestion preparada.")
