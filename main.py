

import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
import shutil
from datetime import datetime
from pathlib import Path
from base_datos import conectar
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth


# COLORES
AZUL = "#172554"
FONDO = "#F1F5F9"
BLANCO = "#FFFFFF"
TEXTO = "#1E293B"
VERDE = "#0F9D85"
GRIS = "#64748B"

# VENTANA
app = tb.Window(themename="flatly")
app.title("Nexo Gestion")
app.geometry("1150x700")
app.minsize(950, 600)
app.configure(bg=FONDO)

# ESTILOS
estilo = ttk.Style()
estilo.configure(
    "Treeview",
    rowheight=34,
    font=("Segoe UI", 10),
    background=BLANCO,
    fieldbackground=BLANCO
)
estilo.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    padding=10
)

# ESTRUCTURA PRINCIPAL
menu = tk.Frame(app, bg=AZUL, width=220)
menu.pack(side="left", fill="y")
menu.pack_propagate(False)

principal = tk.Frame(app, bg=FONDO)
principal.pack(side="left", fill="both", expand=True)

# LOGO
tk.Label(
    menu, text="NEXO",
    font=("Segoe UI", 24, "bold"),
    bg=AZUL, fg=BLANCO
).pack(anchor="w", padx=25, pady=(28, 0))

tk.Label(
    menu, text="GESTION COMERCIAL",
    font=("Segoe UI", 9, "bold"),
    bg=AZUL, fg="#94A3B8"
).pack(anchor="w", padx=27, pady=(0, 35))

# ENCABEZADO
encabezado = tk.Frame(principal, bg=FONDO)
encabezado.pack(fill="x", padx=28, pady=(25, 15))

titulo = tk.Label(
    encabezado, text="Panel principal",
    font=("Segoe UI", 23, "bold"),
    bg=FONDO, fg=AZUL
)
titulo.pack(anchor="w")

subtitulo = tk.Label(
    encabezado, text="Administra tu negocio desde un solo lugar",
    font=("Segoe UI", 10),
    bg=FONDO, fg=GRIS
)
subtitulo.pack(anchor="w", pady=(4, 0))

# AREA DE CONTENIDO
contenido = tk.Frame(principal, bg=FONDO)
contenido.pack(fill="both", expand=True, padx=28, pady=(0, 25))


def limpiar():
    for widget in contenido.winfo_children():
        widget.destroy()


def obtener_productos():
    conexion = conectar()
    filas = conexion.execute(
        "SELECT id, nombre, precio, stock "
        "FROM productos ORDER BY nombre"
    ).fetchall()
    conexion.close()
    return filas



def mostrar_inicio():
    limpiar()
    titulo.config(text="Panel principal")

    productos = obtener_productos()

    total_stock = sum(p[3] for p in productos)
    valor_stock = sum(p[2] * p[3] for p in productos)

    agotados = sum(1 for p in productos if int(p[3]) == 0)
    stock_bajo = sum(
        1 for p in productos
        if 0 < int(p[3]) <= 3
    )

    tk.Label(
        contenido,
        text="Resumen de tu negocio",
        font=("Segoe UI", 15, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(anchor="w", pady=(5, 15))

    
    fila = tk.Frame(contenido, bg=FONDO)
    fila.pack(fill="x")

    fila2 = tk.Frame(contenido, bg=FONDO)
    fila2.pack(fill="x")


    datos = [
        ("PRODUCTOS REGISTRADOS", str(len(productos)), AZUL),
        ("UNIDADES EN STOCK", str(total_stock), AZUL),
        ("VALOR DEL INVENTARIO", f"$ {valor_stock:,.2f}", AZUL),
        ("PRODUCTOS AGOTADOS", str(agotados), "#DC2626"),
        ("STOCK BAJO (1 A 3)", str(stock_bajo), "#D97706")
    ]

    
    for i, (etiqueta, valor, color) in enumerate(datos):

        contenedor = fila if i < 3 else fila2

        tarjeta = tk.Frame(
            contenedor,
            bg=BLANCO,
            highlightbackground="#E2E8F0",
            highlightthickness=1
    )

        tarjeta.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8),
            pady=5
        )

        
        contenedor = fila if i < 3 else fila2

        tarjeta.pack(
            in_=contenedor,
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8),
            pady=5
        )


        tk.Label(
            tarjeta,
            text=etiqueta,
            font=("Segoe UI", 9, "bold"),
            bg=BLANCO,
            fg=GRIS,
            wraplength=150,
            justify="center"
        ).pack(
            fill="x",
            padx=8,
            pady=(18, 8)
        )

        tk.Label(
            tarjeta,
            text=valor,
            font=("Segoe UI", 20, "bold"),
            bg=BLANCO,
            fg=color
        ).pack(
            fill="x",
            padx=8,
            pady=(0, 18)
        )

    tk.Label(
        contenido,
        text="Usa el menú lateral para gestionar tus productos.",
        font=("Segoe UI", 11),
        bg=FONDO,
        fg=GRIS
    ).pack(anchor="w", pady=25)


def mostrar_productos():
    limpiar()
    titulo.config(text="Productos")

    barra = tk.Frame(contenido, bg=FONDO)
    barra.pack(fill="x", pady=(0, 15))

    busqueda = tk.StringVar()

    entrada = tb.Entry(
        barra, textvariable=busqueda,
        width=35, bootstyle="secondary"
    )
    entrada.pack(side="left", ipady=5)

    tabla_frame = tk.Frame(contenido, bg=BLANCO)
    tabla_frame.pack(fill="both", expand=True)

    columnas = ("id", "nombre", "precio", "stock")
    tabla = ttk.Treeview(
        tabla_frame, columns=columnas,
        show="headings", selectmode="browse"
    )
    
    tabla.tag_configure(
        "normal",
        background="#FFFFFF",
        foreground="#1E293B"
    )

    tabla.tag_configure(
        "seleccionado",
        background="#2563EB",
        foreground="#FFFFFF"
    )

    estilo.map(
        "Treeview",
        background=[("selected", "#2563EB")],
        foreground=[("selected", "#FFFFFF")]
    )


    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="PRODUCTO")
    tabla.heading("precio", text="PRECIO")
    tabla.heading("stock", text="STOCK")

    tabla.column("id", width=55, anchor="center")
    tabla.column("nombre", width=360)
    tabla.column("precio", width=150, anchor="e")
    tabla.column("stock", width=100, anchor="center")

    scroll = ttk.Scrollbar(
        tabla_frame, orient="vertical",
        command=tabla.yview
    )
    tabla.configure(yscrollcommand=scroll.set)
    tabla.pack(side="left", fill="both", expand=True, padx=8, pady=8)
    scroll.pack(side="right", fill="y", pady=8)

    def cargar():
        for item in tabla.get_children():
            tabla.delete(item)

        texto = busqueda.get().strip().lower()

        for p in obtener_productos():
            if texto and texto not in p[1].lower():
                continue

           
            tabla.insert(
                "", "end",
                values=(p[0], p[1], f"$ {p[2]:,.2f}", p[3]),
                tags=("normal",)
            )


    def guardar():
        nombre = campo_nombre.get().strip()
        precio_texto = campo_precio.get().strip().replace(",", ".")
        stock_texto = campo_stock.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Dato faltante", "Escribe el nombre del producto."
            )
            return

        try:
            precio = float(precio_texto)
            stock = int(stock_texto)

            if precio < 0 or stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Datos incorrectos",
                "Ingresa un precio no negativo y un stock "
                "entero no negativo."
            )
            return

        conexion = conectar()

        if id_edicion.get() == "":
            conexion.execute(
                "INSERT INTO productos (nombre, precio, stock) "
                "VALUES (?, ?, ?)",
                (nombre, precio, stock)
            )
        else:
            conexion.execute(
                "UPDATE productos SET nombre=?, precio=?, stock=? "
                "WHERE id=?",
                (nombre, precio, stock, int(id_edicion.get()))
            )

        conexion.commit()
        conexion.close()
        cancelar_edicion()
        cargar()
        messagebox.showinfo("Nexo Gestion", "Producto guardado.")
        mostrar_inicio_desde_productos()

    def mostrar_inicio_desde_productos():
        # Actualiza el resumen al volver al inicio.
        pass

    def seleccionar(event=None):
        seleccionado = tabla.selection()
        if not seleccionado:
            return

        valores = tabla.item(seleccionado[0], "values")
        id_edicion.set(str(valores[0]))
        campo_nombre.delete(0, tk.END)
        campo_nombre.insert(0, valores[1])
        campo_precio.delete(0, tk.END)
        campo_precio.insert(0, str(valores[2]).replace("$", "").replace(",", "").strip())
        campo_stock.delete(0, tk.END)
        campo_stock.insert(0, str(valores[3]))
        boton_guardar.config(text="Guardar cambios")

    def cancelar_edicion():
        id_edicion.set("")
        campo_nombre.delete(0, tk.END)
        campo_precio.delete(0, tk.END)
        campo_stock.delete(0, tk.END)
        boton_guardar.config(text="Agregar producto")

    def eliminar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning(
                "Selecciona un producto",
                "Primero selecciona una fila de la tabla."
            )
            return

        valores = tabla.item(seleccionado[0], "values")
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar el producto '{valores[1]}'?"
        )

        if confirmar:
            conexion = conectar()
            conexion.execute(
                "DELETE FROM productos WHERE id=?",
                (int(valores[0]),)
            )
            conexion.commit()
            conexion.close()
            cancelar_edicion()
            cargar()

    busqueda.trace_add("write", lambda *_: cargar())

    # FORMULARIO
    formulario = tk.Frame(contenido, bg=BLANCO)
    formulario.pack(fill="x", pady=(15, 0), padx=0)

    tk.Label(
        formulario, text="Nombre",
        bg=BLANCO, fg=TEXTO
    ).grid(row=0, column=0, sticky="w", padx=10, pady=(12, 2))

    tk.Label(
        formulario, text="Precio",
        bg=BLANCO, fg=TEXTO
    ).grid(row=0, column=1, sticky="w", padx=10, pady=(12, 2))

    tk.Label(
        formulario, text="Stock",
        bg=BLANCO, fg=TEXTO
    ).grid(row=0, column=2, sticky="w", padx=10, pady=(12, 2))

    campo_nombre = tb.Entry(formulario, width=28)
    campo_precio = tb.Entry(formulario, width=15)
    campo_stock = tb.Entry(formulario, width=10)

    campo_nombre.grid(row=1, column=0, padx=10, pady=(0, 12))
    campo_precio.grid(row=1, column=1, padx=10, pady=(0, 12))
    campo_stock.grid(row=1, column=2, padx=10, pady=(0, 12))

    id_edicion = tk.StringVar()

    botonera = tk.Frame(contenido, bg=FONDO)
    botonera.pack(fill="x", pady=12)

   
    boton_guardar = tb.Button(
        botonera,
        text="Agregar producto",
        bootstyle="success",
     command=guardar
    )
    boton_guardar.pack(side="left", padx=(0, 8))

    tb.Button(
        botonera,
        text="Cancelar edición",
        bootstyle="secondary-outline",
        command=cancelar_edicion
    ).pack(side="left", padx=8)


    tb.Button(
        botonera, text="Cargar seleccionado para editar",
        bootstyle="primary", command=seleccionar
    ).pack(side="left", padx=8)

    tb.Button(
        botonera, text="Eliminar seleccionado",
        bootstyle="danger", command=eliminar
    ).pack(side="left", padx=8)

    tb.Button(
        botonera, text="Limpiar",
        bootstyle="secondary-outline", command=cancelar_edicion
    ).pack(side="left", padx=8)

    tabla.bind("<<TreeviewSelect>>", seleccionar)
    cargar()


def mostrar_stock():
    limpiar()
    titulo.config(text="Control de stock")

    tk.Label(
        contenido,
        text="Control de inventario",
        font=("Segoe UI", 18, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(anchor="w", pady=(0, 5))

    tk.Label(
        contenido,
        text="Los productos con 3 unidades o menos necesitan atención.",
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=GRIS
    ).pack(anchor="w", pady=(0, 15))

    resumen = tk.Frame(contenido, bg=FONDO)
    resumen.pack(fill="x", pady=(0, 15))

    tabla_frame = tk.Frame(contenido, bg=BLANCO)
    tabla_frame.pack(fill="both", expand=True)

    columnas = ("id", "nombre", "precio", "stock", "estado")

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="PRODUCTO")
    tabla.heading("precio", text="PRECIO")
    tabla.heading("stock", text="UNIDADES")
    tabla.heading("estado", text="ESTADO")
    
    for columna in columnas:
        tabla.heading(columna, anchor="center")

    
    tabla.column("id", width=70, anchor="center")
    tabla.column("nombre", width=300, anchor="center")
    tabla.column("precio", width=150, anchor="center")
    tabla.column("stock", width=120, anchor="center")
    tabla.column("estado", width=160, anchor="center")


    tabla.tag_configure(
        "agotado",
        background="#FEE2E2",
        foreground="#991B1B"
    )

    tabla.tag_configure(
        "bajo",
        background="#FEF3C7",
        foreground="#92400E"
    )

    tabla.tag_configure(
        "normal",
        background="#FFFFFF",
        foreground="#1E293B"
    )
    estilo.configure(
        "Treeview",
        rowheight=32,
        borderwidth=1,
        relief="solid"
    )

    estilo.configure(
        "Treeview.Heading",
        relief="solid",
        borderwidth=1
    )

    scroll = ttk.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview
    )
    tabla.configure(yscrollcommand=scroll.set)

    tabla.pack(side="left", fill="both", expand=True, padx=12, pady=12)
    scroll.pack(side="right", fill="y", pady=8)

    productos = obtener_productos()

    agotados = 0
    stock_bajo = 0
    normales = 0

    for p in productos:
        cantidad = int(p[3])

        if cantidad == 0:
            estado = "AGOTADO"
            etiqueta = "agotado"
            agotados += 1
        elif cantidad <= 3:
            estado = "STOCK BAJO"
            etiqueta = "bajo"
            stock_bajo += 1
        else:
            estado = "NORMAL"
            etiqueta = "normal"
            normales += 1

        tabla.insert(
            "",
            "end",
            values=(
                p[0],
                p[1],
                f"$ {p[2]:,.2f}",
                cantidad,
                estado
            ),
            tags=(etiqueta,)
        )

    tk.Label(
        resumen,
        text=f"AGOTADOS: {agotados}",
        font=("Segoe UI", 12, "bold"),
        bg="#FEE2E2",
        fg="#991B1B",
        padx=12,
        pady=10
    ).pack(side="left", padx=(0, 8))

    tk.Label(
        resumen,
        text=f"STOCK BAJO: {stock_bajo}",
        font=("Segoe UI", 12, "bold"),
        bg="#FEF3C7",
        fg="#92400E",
        padx=12,
        pady=10
    ).pack(side="left", padx=8)

    tk.Label(
        resumen,
        text=f"NORMAL: {normales}",
        font=("Segoe UI", 12, "bold"),
        bg="#DCFCE7",
        fg="#166534",
        padx=12,
        pady=10
    ).pack(side="left", padx=8)




def mostrar_ventas():
    limpiar()
    titulo.config(text="Ventas")

    carrito = {}
    catalogo = {}

    # ENCABEZADO
    tk.Label(
        contenido,
        text="Registrar una venta",
        font=("Segoe UI", 16, "bold"),
        bg=FONDO,
        fg=AZUL
    ).pack(anchor="w", pady=(0, 12))

    # SELECCION DE PRODUCTOS
    panel = tk.Frame(contenido, bg=BLANCO)
    panel.pack(fill="x", pady=(0, 15))

    tk.Label(
        panel,
        text="Producto",
        bg=BLANCO,
        fg=TEXTO
    ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

    tk.Label(
        panel,
        text="Cantidad",
        bg=BLANCO,
        fg=TEXTO
    ).grid(row=0, column=1, sticky="w", padx=12, pady=(12, 4))

    selector = ttk.Combobox(
        panel,
        state="readonly",
        width=55
    )
    selector.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="w")

    campo_cantidad = tb.Entry(panel, width=12)
    campo_cantidad.insert(0, "1")
    campo_cantidad.grid(
        row=1, column=1, padx=12, pady=(0, 12), sticky="w"
    )

    def cargar_catalogo():
        catalogo.clear()
        opciones = []

        for p in obtener_productos():
            producto_id, nombre, precio, stock = p

            if stock > 0:
                etiqueta = (
                    f"{producto_id} - {nombre} "
                    f"(Stock: {stock}) - ${precio:,.2f}"
                )
                catalogo[etiqueta] = {
                    "id": producto_id,
                    "nombre": nombre,
                    "precio": precio,
                    "stock": stock
                }
                opciones.append(etiqueta)

        selector["values"] = opciones

        if opciones:
            selector.current(0)
        else:
            selector.set("No hay productos con stock disponible")

    # TABLA DEL CARRITO
    tabla_frame = tk.Frame(contenido, bg=BLANCO)
    tabla_frame.pack(fill="both", expand=True)

    columnas = ("id", "nombre", "cantidad", "precio", "subtotal")

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )
    
    estilo.map(
        "Treeview",
        background=[("selected", "#2563EB")],
        foreground=[("selected", "#FFFFFF")]
    )


    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="PRODUCTO")
    tabla.heading("cantidad", text="CANTIDAD")
    tabla.heading("precio", text="PRECIO UNIT.")
    tabla.heading("subtotal", text="SUBTOTAL")

    tabla.column("id", width=50, anchor="center")
    tabla.column("nombre", width=250)
    tabla.column("cantidad", width=90, anchor="center")
    tabla.column("precio", width=120, anchor="e")
    tabla.column("subtotal", width=130, anchor="e")

    tabla.pack(fill="both", expand=True, padx=8, pady=8)

    # TOTAL
    total_var = tk.StringVar(value="$ 0.00")

    pie = tk.Frame(contenido, bg=FONDO)
    pie.pack(fill="x", pady=12)

    tk.Label(
        pie,
        text="TOTAL DE LA VENTA:",
        font=("Segoe UI", 14, "bold"),
        bg=FONDO,
        fg=AZUL
    ).pack(side="left")

    tk.Label(
        pie,
        textvariable=total_var,
        font=("Segoe UI", 18, "bold"),
        bg=FONDO,
        fg=VERDE
    ).pack(side="left", padx=12)

    def actualizar_carrito():
        for item in tabla.get_children():
            tabla.delete(item)

        total = 0

        for producto_id, item in carrito.items():
            subtotal = round(item["precio"] * item["cantidad"], 2)
            total += subtotal

            tabla.insert(
                "",
                "end",
                iid=str(producto_id),
                values=(
                    producto_id,
                    item["nombre"],
                    item["cantidad"],
                    f"$ {item['precio']:,.2f}",
                    f"$ {subtotal:,.2f}"
                )
            )

        total_var.set(f"$ {total:,.2f}")

    def agregar_producto():
        etiqueta = selector.get()

        if etiqueta not in catalogo:
            messagebox.showwarning(
                "Producto",
                "Seleccioná un producto con stock disponible."
            )
            return

        try:
            cantidad = int(campo_cantidad.get().strip())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Cantidad incorrecta",
                "Ingresá una cantidad entera mayor que cero."
            )
            return

        producto = catalogo[etiqueta]
        producto_id = producto["id"]

        cantidad_actual = carrito.get(
            producto_id, {"cantidad": 0}
        )["cantidad"]

        if cantidad_actual + cantidad > producto["stock"]:
            messagebox.showwarning(
                "Stock insuficiente",
                f"Solo hay {producto['stock']} unidades disponibles."
            )
            return

        if producto_id in carrito:
            carrito[producto_id]["cantidad"] += cantidad
        else:
            carrito[producto_id] = {
                "nombre": producto["nombre"],
                "precio": producto["precio"],
                "cantidad": cantidad
            }

        campo_cantidad.delete(0, tk.END)
        campo_cantidad.insert(0, "1")
        actualizar_carrito()

    def quitar_producto():
        seleccionado = tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Seleccioná un producto",
                "Elegí una fila del carrito para quitarla."
            )
            return

        producto_id = int(seleccionado[0])
        carrito.pop(producto_id, None)
        actualizar_carrito()

    def finalizar_venta():
        if not carrito:
            messagebox.showwarning(
                "Venta vacía",
                "Agregá al menos un producto antes de finalizar."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar venta",
            "¿Querés registrar esta venta y descontar el stock?"
        )

        if not confirmar:
            return

        conexion = conectar()

        try:
            # Evita que otra operación modifique el stock
            # mientras se registra esta venta.
            conexion.execute("BEGIN IMMEDIATE")

            detalles = []
            total = 0

            for producto_id, item in carrito.items():
                producto = conexion.execute(
                    "SELECT nombre, precio, stock "
                    "FROM productos WHERE id = ?",
                    (producto_id,)
                ).fetchone()

                if producto is None:
                    raise ValueError(
                        f"El producto ID {producto_id} ya no existe."
                    )

                nombre, precio, stock = producto
                cantidad = item["cantidad"]

                if cantidad > stock:
                    raise ValueError(
                        f"Stock insuficiente para {nombre}. "
                        f"Disponible: {stock}."
                    )

                precio = float(precio)
                subtotal = round(precio * cantidad, 2)
                total += subtotal

                detalles.append((
                    producto_id,
                    nombre,
                    cantidad,
                    precio,
                    subtotal
                ))

            total = round(total, 2)

            cursor = conexion.execute(
                "INSERT INTO ventas (total) VALUES (?)",
                (total,)
            )
            venta_id = cursor.lastrowid

            for producto_id, nombre, cantidad, precio, subtotal in detalles:
                conexion.execute(
                    """
                    INSERT INTO detalle_venta
                    (venta_id, producto_id, nombre_producto,
                     cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        venta_id, producto_id, nombre,
                        cantidad, precio, subtotal
                    )
                )

                conexion.execute(
                    "UPDATE productos SET stock = stock - ? WHERE id = ?",
                    (cantidad, producto_id)
                )

            conexion.commit()

        except (ValueError, Exception) as error:
            conexion.rollback()
            conexion.close()

            messagebox.showerror(
                "No se pudo registrar la venta",
                str(error)
            )
            return

        conexion.close()
        carrito.clear()
        actualizar_carrito()
        cargar_catalogo()

        messagebox.showinfo(
            "Venta registrada",
            f"Venta N.º {venta_id} guardada correctamente.\n"
            f"Total: $ {total:,.2f}\n\n"
            "El stock fue actualizado."
        )

    # BOTONES
    botones = tk.Frame(contenido, bg=FONDO)
    botones.pack(fill="x", pady=(0, 5))

    tb.Button(
        botones,
        text="Agregar producto",
        bootstyle="primary",
        command=agregar_producto
    ).pack(side="left", padx=(0, 8))

    tb.Button(
        botones,
        text="Quitar del carrito",
        bootstyle="secondary-outline",
        command=quitar_producto
    ).pack(side="left", padx=8)

    tb.Button(
        botones,
        text="FINALIZAR VENTA",
        bootstyle="success",
        command=finalizar_venta
    ).pack(side="right")

    cargar_catalogo()




def mostrar_historial_ventas():
    limpiar()
    titulo.config(text="Historial de ventas")

    tk.Label(
        contenido,
        text="Ventas registradas",
        font=("Segoe UI", 16, "bold"),
        bg=FONDO,
        fg=AZUL
    ).pack(anchor="w", pady=(0, 15))

    # BARRA DE BUSQUEDA Y FILTROS
    filtros = tk.Frame(contenido, bg=FONDO)
    filtros.pack(fill="x", pady=(0, 12))

    tk.Label(
        filtros, text="N.º de venta:",
        bg=FONDO, fg=TEXTO
    ).pack(side="left", padx=(0, 6))

    buscar_id = tk.StringVar()

    entrada_busqueda = tb.Entry(
        filtros,
        textvariable=buscar_id,
        width=12,
        bootstyle="secondary"
    )
    entrada_busqueda.pack(side="left", padx=(0, 12), ipady=4)

    tk.Label(
        filtros, text="Desde (AAAA-MM-DD):",
        bg=FONDO, fg=TEXTO
    ).pack(side="left", padx=(0, 6))

    fecha_desde = tb.Entry(
        filtros, width=14, bootstyle="secondary"
    )
    fecha_desde.pack(side="left", padx=(0, 10), ipady=4)

    tk.Label(
        filtros, text="Hasta:",
        bg=FONDO, fg=TEXTO
    ).pack(side="left", padx=(0, 6))

    fecha_hasta = tb.Entry(
        filtros, width=14, bootstyle="secondary"
    )
    fecha_hasta.pack(side="left", padx=(0, 10), ipady=4)

    # TARJETAS DE RESUMEN
    resumen = tk.Frame(contenido, bg=FONDO)
    resumen.pack(fill="x", pady=(0, 12))

    tarjeta_ventas = tk.Frame(
        resumen,
        bg=BLANCO,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    tarjeta_ventas.pack(
        side="left", fill="both",
        expand=True, padx=(0, 8)
    )

    tk.Label(
        tarjeta_ventas,
        text="VENTAS ENCONTRADAS",
        font=("Segoe UI", 9, "bold"),
        bg=BLANCO, fg=GRIS
    ).pack(anchor="w", padx=15, pady=(12, 4))

    lbl_cantidad_ventas = tk.Label(
        tarjeta_ventas,
        text="0",
        font=("Segoe UI", 20, "bold"),
        bg=BLANCO, fg=AZUL
    )
    lbl_cantidad_ventas.pack(
        anchor="w", padx=15, pady=(0, 12)
    )

    tarjeta_total = tk.Frame(
        resumen,
        bg=BLANCO,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    tarjeta_total.pack(
        side="left", fill="both",
        expand=True, padx=(8, 0)
    )

    tk.Label(
        tarjeta_total,
        text="FACTURACIÓN TOTAL",
        font=("Segoe UI", 9, "bold"),
        bg=BLANCO, fg=GRIS
    ).pack(anchor="w", padx=15, pady=(12, 4))

    lbl_total_facturado = tk.Label(
        tarjeta_total,
        text="$ 0,00",
        font=("Segoe UI", 20, "bold"),
        bg=BLANCO, fg=VERDE
    )
    lbl_total_facturado.pack(
        anchor="w", padx=15, pady=(0, 12)
    )

    # TABLA DEL HISTORIAL
    tabla_frame = tk.Frame(contenido, bg=BLANCO)
    tabla_frame.pack(fill="both", expand=True)

    columnas = ("id", "fecha", "total")

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    estilo.map(
        "Treeview",
        background=[("selected", "#2563EB")],
        foreground=[("selected", "#FFFFFF")]
    )

    tabla.heading("id", text="N.º VENTA", anchor="center")
    tabla.heading("fecha", text="FECHA Y HORA", anchor="center")
    tabla.heading("total", text="TOTAL", anchor="center")

    tabla.column("id", width=100, anchor="center")
    tabla.column("fecha", width=220, anchor="center")
    tabla.column("total", width=160, anchor="center")

    tabla.pack(
        side="left", fill="both", expand=True,
        padx=8, pady=8
    )

    scroll = ttk.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview
    )
    tabla.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y", pady=8)

    # CARGAR VENTAS DESDE SQLITE
    try:
        conexion = conectar()

        ventas = conexion.execute("""
            SELECT id, fecha, total
            FROM ventas
            ORDER BY id DESC
        """).fetchall()

        conexion.close()

    except Exception as error:
        messagebox.showerror(
            "Error al cargar el historial", str(error)
        )
        return

    def cargar_ventas():
        texto_id = buscar_id.get().strip()
        desde = fecha_desde.get().strip()
        hasta = fecha_hasta.get().strip()

        if texto_id and not texto_id.isdigit():
            messagebox.showwarning(
                "Número incorrecto",
                "Ingresá un número de venta válido."
            )
            return

        for fecha in (desde, hasta):
            if fecha:
                try:
                    datetime.strptime(fecha, "%Y-%m-%d")
                except ValueError:
                    messagebox.showwarning(
                        "Fecha incorrecta",
                        "Usá AAAA-MM-DD, por ejemplo 2026-10-16."
                    )
                    return

        if desde and hasta and desde > hasta:
            messagebox.showwarning(
                "Fechas incorrectas",
                "La fecha inicial no puede superar la final."
            )
            return

        for item in tabla.get_children():
            tabla.delete(item)

        cantidad_encontrada = 0
        total_encontrado = 0.0

        for venta in ventas:
            venta_id = str(venta[0])
            fecha_venta = str(venta[1])
            fecha_dia = fecha_venta[:10]

            if texto_id and texto_id != venta_id:
                continue

            if desde and fecha_dia < desde:
                continue

            if hasta and fecha_dia > hasta:
                continue

            tabla.insert(
                "",
                "end",
                values=(
                    venta[0],
                    venta[1],
                    f"$ {venta[2]:,.2f}"
                )
            )

            cantidad_encontrada += 1
            total_encontrado += float(venta[2])

        # ACTUALIZAR TARJETAS
        lbl_cantidad_ventas.config(
            text=str(cantidad_encontrada)
        )

        lbl_total_facturado.config(
            text=f"$ {total_encontrado:,.2f}"
        )

    def limpiar_filtros():
        buscar_id.set("")
        fecha_desde.delete(0, tk.END)
        fecha_hasta.delete(0, tk.END)
        cargar_ventas()

    def ver_detalle():
        seleccionado = tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Seleccioná una venta",
                "Elegí una venta de la tabla."
            )
            return

        valores = tabla.item(seleccionado[0], "values")
        venta_id = int(valores[0])

        try:
            conexion = conectar()

            detalles = conexion.execute("""
                SELECT nombre_producto, cantidad,
                       precio_unitario, subtotal
                FROM detalle_venta
                WHERE venta_id = ?
            """, (venta_id,)).fetchall()

            conexion.close()

        except Exception as error:
            messagebox.showerror(
                "Error al consultar el detalle", str(error)
            )
            return

        if not detalles:
            messagebox.showinfo(
                "Detalle de venta",
                "No se encontraron productos para esta venta."
            )
            return

        mensaje = f"Venta N.º {venta_id}\n"
        mensaje += f"Fecha: {valores[1]}\n\n"

        for nombre, cantidad, precio, subtotal in detalles:
            mensaje += (
                f"{nombre}\n"
                f"  Cantidad: {cantidad}\n"
                f"  Precio unitario: $ {precio:,.2f}\n"
                f"  Subtotal: $ {subtotal:,.2f}\n\n"
            )

        mensaje += f"TOTAL: {valores[2]}"

        messagebox.showinfo("Detalle de venta", mensaje)
        
    
    def generar_comprobante():
        seleccionado = tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Seleccioná una venta",
                "Elegí una venta de la tabla."
            )
            return

        valores = tabla.item(seleccionado[0], "values")
        venta_id = int(valores[0])

        try:
            
            conexion = conectar()

            detalles = conexion.execute("""
                SELECT nombre_producto, cantidad,
                       precio_unitario, subtotal
                FROM detalle_venta
                WHERE venta_id = ?
            """, (venta_id,)).fetchall()

            negocio = conexion.execute("""
                SELECT nombre, cuit, direccion, telefono
                FROM datos_negocio
                WHERE id = 1
            """).fetchone()

            conexion.close()

            if negocio:
                nombre_negocio, cuit_negocio, direccion_negocio, telefono_negocio = negocio
            else:
                nombre_negocio = "Mi negocio"
                cuit_negocio = ""
                direccion_negocio = ""
                telefono_negocio = ""


        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo consultar la venta:\n{error}"
            )
            return

        if not detalles:
            messagebox.showwarning(
                "Sin detalles",
                "Esta venta no tiene productos registrados."
            )
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar comprobante PDF",
            defaultextension=".pdf",
            initialfile=f"comprobante_venta_{venta_id}.pdf",
            filetypes=[("Documento PDF", "*.pdf")]
        )

        if not ruta:
            return

        
        try:
            ancho, alto = A4
            pdf = canvas.Canvas(ruta, pagesize=A4)

            azul = colors.HexColor("#172554")
            verde = colors.HexColor("#0F9D85")
            gris = colors.HexColor("#64748B")
            claro = colors.HexColor("#F1F5F9")
            texto = colors.HexColor("#1E293B")
            blanco = colors.white

            margen = 42
            ancho_util = ancho - 2 * margen

            def dibujar_encabezado():
                # Franja superior
                pdf.setFillColor(azul)
                pdf.rect(0, alto - 145, ancho, 145, fill=1, stroke=0)

                # Marca
                pdf.setFillColor(blanco)
                pdf.setFont("Helvetica-Bold", 28)
                pdf.drawString(margen, alto - 48, "NEXO")

                pdf.setFont("Helvetica", 9)
                pdf.drawString(
                    margen, alto - 65, "GESTION COMERCIAL"
                )

                # Nombre del comercio
                pdf.setFont("Helvetica-Bold", 13)
                pdf.drawString(
                    margen, alto - 91, str(nombre_negocio)[:42]
                )

                pdf.setFont("Helvetica", 8)

                if cuit_negocio:
                    pdf.drawString(
                        margen, alto - 106,
                        f"CUIT: {str(cuit_negocio)[:35]}"
                    )

                if direccion_negocio:
                    pdf.drawString(
                        margen, alto - 120,
                        str(direccion_negocio)[:45]
                    )

                if telefono_negocio:
                    pdf.drawString(
                        margen + 230, alto - 120,
                        f"Tel.: {str(telefono_negocio)[:25]}"
                    )

                # Tipo de comprobante
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawRightString(
                    ancho - margen, alto - 48, "COMPROBANTE"
                )

                pdf.setFont("Helvetica", 10)
                pdf.drawRightString(
                    ancho - margen, alto - 66, "DE VENTA"
                )

                # Número y fecha
                pdf.setFillColor(texto)
                pdf.setFont("Helvetica-Bold", 11)
                pdf.drawString(
                    margen, alto - 173, f"Venta N.º {venta_id}"
                )

                pdf.setFillColor(gris)
                pdf.setFont("Helvetica", 9)
                pdf.drawRightString(
                    ancho - margen, alto - 173,
                    f"Fecha: {str(valores[1])}"
                )

            def dibujar_tabla():
                y_tabla = alto - 210

                pdf.setFillColor(claro)
                pdf.roundRect(
                    margen, y_tabla - 7,
                    ancho_util, 27, 5, fill=1, stroke=0
                )

                pdf.setFillColor(azul)
                pdf.setFont("Helvetica-Bold", 8)

                pdf.drawString(margen + 10, y_tabla + 2, "PRODUCTO")
                pdf.drawRightString(ancho - 205, y_tabla + 2, "CANT.")
                pdf.drawRightString(ancho - 120, y_tabla + 2, "PRECIO")
                pdf.drawRightString(
                    ancho - margen - 10, y_tabla + 2, "SUBTOTAL"
                )

                return y_tabla - 25

            dibujar_encabezado()
            y = dibujar_tabla()
            total_calculado = 0.0

            for nombre, cantidad, precio, subtotal in detalles:
                nombre = str(nombre)
                precio = float(precio)
                subtotal = float(subtotal)
                total_calculado += subtotal

                # Nueva página si no hay espacio para otra fila
                if y < 105:
                    pdf.showPage()
                    y = alto - 65

                    pdf.setFillColor(azul)
                    pdf.setFont("Helvetica-Bold", 13)
                    pdf.drawString(margen, y, "NEXO - Detalle de venta")

                    pdf.setFillColor(gris)
                    pdf.setFont("Helvetica", 9)
                    pdf.drawRightString(
                        ancho - margen, y, f"Venta N.º {venta_id}"
                    )

                    y -= 30
                    y = dibujar_tabla()

                pdf.setFillColor(texto)
                pdf.setFont("Helvetica", 9)

                # Ajustar el nombre para que no invada otras columnas
                max_ancho = ancho - 2 * margen - 220
                nombre_visible = nombre

                while (
                    nombre_visible
                    and stringWidth(
                        nombre_visible, "Helvetica", 9
                    ) > max_ancho
                ):
                    nombre_visible = nombre_visible[:-1]

                if nombre_visible != nombre:
                    nombre_visible = nombre_visible[:-3] + "..."

                pdf.drawString(
                    margen + 10, y, nombre_visible
                )
                pdf.drawRightString(
                    ancho - 205, y, str(cantidad)
                )
                pdf.drawRightString(
                    ancho - 120, y, f"$ {precio:,.2f}"
                )
                pdf.drawRightString(
                    ancho - margen - 10, y, f"$ {subtotal:,.2f}"
                )

                y -= 23

                pdf.setStrokeColor(claro)
                pdf.line(margen, y + 11, ancho - margen, y + 11)

            # Reservar espacio para el total
            if y < 100:
                pdf.showPage()
                y = alto - 75

            y -= 8

            pdf.setFillColor(verde)
            pdf.roundRect(
                margen, y - 15, ancho_util, 48,
                7, fill=1, stroke=0
            )

            pdf.setFillColor(blanco)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(margen + 15, y + 2, "TOTAL DE LA VENTA")

            pdf.setFont("Helvetica-Bold", 17)
            pdf.drawRightString(
                ancho - margen - 15, y,
                f"$ {total_calculado:,.2f}"
            )

            # Pie de página
            pdf.setFillColor(gris)
            pdf.setFont("Helvetica", 9)
            pdf.drawCentredString(
                ancho / 2, 38, "Gracias por su compra."
            )

            pdf.setFont("Helvetica", 7)
            pdf.drawCentredString(
                ancho / 2, 25, "NEXO GESTION COMERCIAL"
            )

            pdf.save()

            messagebox.showinfo(
                "PDF generado",
                f"El comprobante se guardó correctamente:\n{ruta}"
            )

        except Exception as error:
            messagebox.showerror(
                "Error al generar el PDF",
                str(error)
            )



    # BOTONES
    tb.Button(
        filtros,
        text="Buscar",
        bootstyle="primary",
        command=cargar_ventas
    ).pack(side="left", padx=4)

    tb.Button(
        filtros,
        text="Mostrar todas",
        bootstyle="secondary-outline",
        command=limpiar_filtros
    ).pack(side="left", padx=4)

    botones = tk.Frame(contenido, bg=FONDO)
    botones.pack(fill="x", pady=12)

    tb.Button(
        botones,
        text="Ver detalle de la venta seleccionada",
        bootstyle="primary",
        command=ver_detalle
    ).pack(side="left")
    
    tb.Button(
        botones,
        text="Generar comprobante",
        bootstyle="success",
        command=generar_comprobante
    ).pack(side="left", padx=10)

    entrada_busqueda.bind(
        "<Return>",
        lambda event: cargar_ventas()
    )

    cargar_ventas()



def mostrar_reportes():
    limpiar()
    titulo.config(text="Reportes")

    tk.Label(
        contenido,
        text="Informes de tu negocio",
        font=("Segoe UI", 16, "bold"),
        bg=FONDO,
        fg=AZUL
    ).pack(anchor="w", pady=(0, 5))

    tk.Label(
        contenido,
        text="Consultá tus ingresos y los productos más vendidos.",
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=GRIS
    ).pack(anchor="w", pady=(0, 15))

    # PESTAÑAS DE LOS REPORTES
    pestañas = ttk.Notebook(contenido)
    pestañas.pack(fill="both", expand=True)

    pagina_diaria = tk.Frame(pestañas, bg=BLANCO)
    pagina_mensual = tk.Frame(pestañas, bg=BLANCO)
    pagina_productos = tk.Frame(pestañas, bg=BLANCO)

    pestañas.add(pagina_diaria, text="Ingresos diarios")
    pestañas.add(pagina_mensual, text="Ingresos mensuales")
    pestañas.add(pagina_productos, text="Más vendidos")

    def crear_tabla(pagina, columnas, encabezados, anchos):
        marco = tk.Frame(pagina, bg=BLANCO)
        marco.pack(fill="both", expand=True, padx=10, pady=10)

        tabla = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )
        
        estilo.map(
            "Treeview",
            background=[("selected", "#2563EB")],
            foreground=[("selected", "#FFFFFF")]
        )


        for columna, encabezado, ancho in zip(
            columnas, encabezados, anchos
        ):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=ancho, anchor="center")

        tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=tabla.yview
        )
        tabla.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        return tabla

    # TABLA DE INGRESOS DIARIOS
    tabla_diaria = crear_tabla(
        pagina_diaria,
        ("fecha", "cantidad", "total"),
        ("FECHA", "VENTAS REGISTRADAS", "INGRESOS"),
        (180, 180, 200)
    )

    # TABLA DE INGRESOS MENSUALES
    tabla_mensual = crear_tabla(
        pagina_mensual,
        ("mes", "cantidad", "total"),
        ("MES", "VENTAS REGISTRADAS", "INGRESOS"),
        (180, 180, 200)
    )

    # TABLA DE PRODUCTOS MAS VENDIDOS
    tabla_productos = crear_tabla(
        pagina_productos,
        ("producto", "unidades", "ingresos"),
        ("PRODUCTO", "UNIDADES VENDIDAS", "INGRESOS"),
        (280, 160, 200)
    )

    def cargar_reportes():
        for tabla in (
            tabla_diaria,
            tabla_mensual,
            tabla_productos
        ):
            for item in tabla.get_children():
                tabla.delete(item)

        conexion = conectar()

        try:
            # INGRESOS POR DIA
            diarios = conexion.execute("""
                SELECT date(fecha), COUNT(*), ROUND(SUM(total), 2)
                FROM ventas
                GROUP BY date(fecha)
                ORDER BY date(fecha) DESC
            """).fetchall()

            for fecha, cantidad, total in diarios:
                tabla_diaria.insert(
                    "",
                    "end",
                    values=(
                        fecha,
                        cantidad,
                        f"$ {total:,.2f}"
                    )
                )

            # INGRESOS POR MES
            mensuales = conexion.execute("""
                SELECT strftime('%Y-%m', fecha),
                       COUNT(*),
                       ROUND(SUM(total), 2)
                FROM ventas
                GROUP BY strftime('%Y-%m', fecha)
                ORDER BY strftime('%Y-%m', fecha) DESC
            """).fetchall()

            for mes, cantidad, total in mensuales:
                tabla_mensual.insert(
                    "",
                    "end",
                    values=(
                        mes,
                        cantidad,
                        f"$ {total:,.2f}"
                    )
                )

            # PRODUCTOS MAS VENDIDOS
            mas_vendidos = conexion.execute("""
                SELECT nombre_producto,
                       SUM(cantidad),
                       ROUND(SUM(subtotal), 2)
                FROM detalle_venta
                GROUP BY nombre_producto
                ORDER BY SUM(cantidad) DESC,
                         SUM(subtotal) DESC
            """).fetchall()

            for nombre, unidades, ingresos in mas_vendidos:
                tabla_productos.insert(
                    "",
                    "end",
                    values=(
                        nombre,
                        unidades,
                        f"$ {ingresos:,.2f}"
                    )
                )

        except Exception as error:
            messagebox.showerror(
                "Error en los reportes",
                str(error)
            )
        finally:
            conexion.close()

    cargar_reportes()

    tb.Button(
        contenido,
        text="Actualizar reportes",
        bootstyle="primary",
        command=cargar_reportes
    ).pack(anchor="e", pady=10)



def mostrar_datos_negocio():
    limpiar()
    titulo.config(text="Datos del negocio")

    # Crear una tabla de configuración si todavía no existe.
    # Esto conserva las tablas y los datos actuales.
    conexion = conectar()
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS datos_negocio (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            nombre TEXT NOT NULL DEFAULT '',
            cuit TEXT NOT NULL DEFAULT '',
            direccion TEXT NOT NULL DEFAULT '',
            telefono TEXT NOT NULL DEFAULT ''
        )
    """)
    conexion.execute("""
        INSERT OR IGNORE INTO datos_negocio
        (id, nombre, cuit, direccion, telefono)
        VALUES (1, '', '', '', '')
    """)
    conexion.commit()

    datos = conexion.execute("""
        SELECT nombre, cuit, direccion, telefono
        FROM datos_negocio
        WHERE id = 1
    """).fetchone()
    conexion.close()

    tk.Label(
        contenido,
        text="Información del comercio",
        font=("Segoe UI", 16, "bold"),
        bg=FONDO,
        fg=AZUL
    ).pack(anchor="w", pady=(0, 5))

    tk.Label(
        contenido,
        text="Estos datos se utilizarán en los comprobantes de venta.",
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=GRIS
    ).pack(anchor="w", pady=(0, 20))

    formulario = tk.Frame(contenido, bg=BLANCO)
    formulario.pack(fill="x", anchor="n")

    campos = [
        ("Nombre del comercio", datos[0]),
        ("CUIT", datos[1]),
        ("Dirección", datos[2]),
        ("Teléfono", datos[3])
    ]

    entradas = {}

    for etiqueta, valor in campos:
        tk.Label(
            formulario,
            text=etiqueta,
            font=("Segoe UI", 10, "bold"),
            bg=BLANCO,
            fg=TEXTO
        ).pack(anchor="w", padx=20, pady=(14, 4))

        entrada = tb.Entry(formulario, width=55)
        entrada.pack(fill="x", padx=20, pady=(0, 4), ipady=5)
        entrada.insert(0, valor or "")

        entradas[etiqueta] = entrada

    def guardar_datos():
        nombre = entradas["Nombre del comercio"].get().strip()
        cuit = entradas["CUIT"].get().strip()
        direccion = entradas["Dirección"].get().strip()
        telefono = entradas["Teléfono"].get().strip()

        if not nombre:
            messagebox.showwarning(
                "Falta el nombre",
                "Ingresá el nombre del comercio."
            )
            return

        conexion = conectar()

        try:
            conexion.execute("""
                UPDATE datos_negocio
                SET nombre = ?, cuit = ?, direccion = ?, telefono = ?
                WHERE id = 1
            """, (nombre, cuit, direccion, telefono))

            conexion.commit()

        except Exception as error:
            messagebox.showerror(
                "Error al guardar",
                f"No se pudieron guardar los datos:\n{error}"
            )
            return

        finally:
            conexion.close()

        messagebox.showinfo(
            "Datos guardados",
            "Los datos del negocio se guardaron correctamente."
        )

    tb.Button(
        contenido,
        text="Guardar datos del negocio",
        bootstyle="success",
        command=guardar_datos
    ).pack(anchor="w", pady=15)


def mostrar_seccion(nombre):
    if nombre == "Inicio":
        mostrar_inicio()
    elif nombre == "Productos":
        mostrar_productos()
    elif nombre == "Ventas":
        mostrar_ventas()
    elif nombre == "Stock":
        mostrar_stock() 
    elif nombre == "Historial de ventas":
        mostrar_historial_ventas() 
    elif nombre == "Reportes":
        mostrar_reportes() 
    elif nombre == "Datos del negocio":
        mostrar_datos_negocio() 
    
    else:
        limpiar()
        titulo.config(text=nombre)
        tk.Label(
            contenido,
            text="Estamos construyendo esta sección.",
            font=("Segoe UI", 14),
            bg=FONDO, fg=GRIS
        ).pack(anchor="w", pady=25)


# MENU
for nombre in [
    "Inicio",
    "Productos",
    "Ventas",
    "Historial de ventas",
    "Stock",
    "Reportes",
    "Datos del negocio"
]:
    tb.Button(
        menu,
        text=nombre,
        bootstyle="secondary",
        command=lambda n=nombre: mostrar_seccion(n)
    ).pack(fill="x", padx=15, pady=5, ipady=5)

mostrar_inicio()
app.mainloop()
