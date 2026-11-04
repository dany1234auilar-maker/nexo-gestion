import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import ttkbootstrap as tb
from base_datos import conectar
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

# ============================================================
# NEXO GESTION - interfaz renovada
# Conserva la base de datos existente: nexo.db / conectar()
# ============================================================

AZUL = "#172554"
AZUL_CLARO = "#243B70"
FONDO = "#F3F6FB"
BLANCO = "#FFFFFF"
TEXTO = "#1E293B"
GRIS = "#64748B"
TURQUESA = "#14B8A6"
VERDE = "#0F9D85"
BORDE = "#E2E8F0"
ROJO = "#DC2626"
NARANJA = "#D97706"

app = tb.Window(themename="flatly")
app.title("Nexo Gestión | Gestión comercial")
app.geometry("1250x780")
app.minsize(1000, 650)
app.configure(bg=FONDO)

# Estilos globales de tablas y pestañas
estilo = ttk.Style()
estilo.configure(
    "Nexo.Treeview",
    rowheight=36,
    font=("Segoe UI", 10),
    background=BLANCO,
    fieldbackground=BLANCO,
    foreground=TEXTO,
    borderwidth=0,
    relief="flat"
)
estilo.configure(
    "Nexo.Treeview.Heading",
    font=("Segoe UI", 9, "bold"),
    padding=(10, 11),
    background="#EAF0F8",
    foreground=AZUL,
    relief="flat"
)
estilo.map(
    "Nexo.Treeview",
    background=[("selected", "#CCFBF1")],
    foreground=[("selected", AZUL)]
)
estilo.map(
    "Nexo.Treeview.Heading",
    background=[("active", "#DCE7F5")]
)
estilo.configure("TNotebook", background=FONDO, borderwidth=0)
estilo.configure("TNotebook.Tab", padding=(16, 10), font=("Segoe UI", 9, "bold"))

# Estructura principal - estilo claro inspirado en el panel de referencia
menu = tk.Frame(app, bg=BLANCO, width=175, highlightbackground=BORDE, highlightthickness=1)
menu.pack(side="left", fill="y")
menu.pack_propagate(False)

zona_derecha = tk.Frame(app, bg=FONDO)
zona_derecha.pack(side="left", fill="both", expand=True)

# Marca y navegación lateral: estilo limpio inspirado en StockMind
top_marca = tk.Frame(menu, bg=BLANCO, height=62)
top_marca.pack(fill="x", padx=12, pady=(13, 10))
top_marca.pack_propagate(False)
icono_marca = tk.Canvas(top_marca, width=34, height=34, bg=BLANCO, highlightthickness=0)
icono_marca.pack(side="left", padx=(0, 9), pady=5)
icono_marca.create_rectangle(2, 2, 32, 32, fill="#2563EB", outline="#2563EB")
icono_marca.create_text(17, 17, text="◆", fill=BLANCO, font=("Segoe UI", 15, "bold"))
marca_textos = tk.Frame(top_marca, bg=BLANCO)
marca_textos.pack(side="left", fill="y", pady=4)
tk.Label(marca_textos, text="TIENDA", font=("Segoe UI", 11, "bold"), bg=BLANCO, fg="#172033").pack(anchor="w")
tk.Label(marca_textos, text="Gestión comercial", font=("Segoe UI", 8), bg=BLANCO, fg=GRIS).pack(anchor="w", pady=(2, 0))
tk.Frame(menu, bg="#E9EEF5", height=1).pack(fill="x")

# Encabezado de la zona de trabajo
encabezado = tk.Frame(zona_derecha, bg=BLANCO, height=82, highlightbackground=BORDE, highlightthickness=1)
encabezado.pack(fill="x")
encabezado.pack_propagate(False)
titulo = tk.Label(encabezado, text="NEXO GESTION", font=("Segoe UI", 20, "bold"), bg=BLANCO, fg=TEXTO)
titulo.pack(anchor="w", padx=26, pady=(10, 0))
subtitulo = tk.Label(encabezado, text="Vista general de tu negocio", font=("Segoe UI", 9), bg=BLANCO, fg=GRIS)
subtitulo.pack(anchor="w", padx=28, pady=(1, 7))
contenido = tk.Frame(zona_derecha, bg=FONDO)
contenido.pack(fill="both", expand=True, padx=24, pady=20)

seccion_activa = {"nombre": "Inicio", "boton": None}
botones_menu = {}


def limpiar():
    for widget in contenido.winfo_children():
        widget.destroy()


def obtener_productos():
    conexion = conectar()
    try:
        return conexion.execute(
            "SELECT id, nombre, precio, stock FROM productos ORDER BY nombre"
        ).fetchall()
    finally:
        conexion.close()


def tarjeta(parent, etiqueta, valor, color=AZUL, detalle=None):
    caja = tk.Frame(parent, bg=BLANCO, highlightbackground=BORDE, highlightthickness=1)
    tk.Frame(caja, bg=color, height=4).pack(fill="x")
    interior = tk.Frame(caja, bg=BLANCO)
    interior.pack(fill="both", expand=True, padx=18, pady=15)
    if detalle:
        tk.Label(interior, text=detalle.upper(), font=("Segoe UI", 8, "bold"), bg=BLANCO, fg=color).pack(anchor="w", pady=(0, 8))
    tk.Label(interior, text=etiqueta.upper(), font=("Segoe UI", 9, "bold"), bg=BLANCO, fg=GRIS, wraplength=230, justify="left").pack(anchor="w", pady=(0, 8))
    tk.Label(interior, text=valor, font=("Segoe UI", 22, "bold"), bg=BLANCO, fg=color).pack(anchor="w")
    return caja


def crear_tabla(parent, columnas, encabezados, anchos=None, anclajes=None):
    marco = tk.Frame(parent, bg=BLANCO, highlightbackground=BORDE, highlightthickness=1)
    tabla = ttk.Treeview(marco, columns=columnas, show="headings", selectmode="browse", style="Nexo.Treeview")
    for i, (columna, encabezado_texto) in enumerate(zip(columnas, encabezados)):
        tabla.heading(columna, text=encabezado_texto, anchor="center")
        ancho = anchos[i] if anchos and i < len(anchos) else 150
        ancla = anclajes[i] if anclajes and i < len(anclajes) else "w"
        tabla.column(columna, width=ancho, anchor=ancla, minwidth=60)
    scroll = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll.set)
    tabla.pack(side="left", fill="both", expand=True, padx=8, pady=8)
    scroll.pack(side="right", fill="y", pady=8, padx=(0, 6))
    return marco, tabla


def mostrar_inicio():
    limpiar()
    titulo.config(text="NEXO GESTION")
    subtitulo.config(text="Resumen general de tu negocio")

    productos = obtener_productos()
    total_stock = sum(int(p[3]) for p in productos)
    valor_stock = sum(float(p[2]) * int(p[3]) for p in productos)
    stock_bajo = sum(1 for p in productos if int(p[3]) <= 3)

    conexion = conectar()
    try:
        ventas_hoy = conexion.execute(
            "SELECT COUNT(*), COALESCE(SUM(total), 0) FROM ventas WHERE date(fecha)=date('now','localtime')"
        ).fetchone()
        # Ingresos agrupados por día para los últimos siete días.
        filas = conexion.execute(
            "SELECT date(fecha), COALESCE(SUM(total),0) FROM ventas "
            "WHERE date(fecha) >= date('now','localtime','-6 days') "
            "GROUP BY date(fecha) ORDER BY date(fecha)"
        ).fetchall()
        recientes = conexion.execute(
            "SELECT id, fecha, total FROM ventas ORDER BY id DESC LIMIT 5"
        ).fetchall()
    except Exception:
        ventas_hoy = (0, 0)
        filas, recientes = [], []
    finally:
        conexion.close()

    ingresos_por_dia = {str(f[0]): float(f[1] or 0) for f in filas if f[0]}
    from datetime import date, timedelta
    dias = [date.today() - timedelta(days=i) for i in range(6, -1, -1)]
    valores = [ingresos_por_dia.get(d.isoformat(), 0) for d in dias]
    nombres_dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    nombres_dias = [nombres_dias[d.weekday()] if d != date.today() else "Hoy" for d in dias]

    # Cuatro indicadores principales
    fila_tarjetas = tk.Frame(contenido, bg=FONDO)
    fila_tarjetas.pack(fill="x", pady=(0, 18))
    indicadores = [
        ("Productos", str(len(productos)), AZUL, "▦"),
        ("Alertas de stock", str(stock_bajo), ROJO if stock_bajo else VERDE, "⚠"),
        ("Ventas de hoy", str(ventas_hoy[0]), "#8B5CF6", "▣"),
        ("Valor del inventario", f"$ {valor_stock:,.2f}", VERDE, "$"),
    ]
    for etiqueta, valor, color, icono in indicadores:
        caja = tk.Frame(fila_tarjetas, bg=BLANCO, highlightbackground=BORDE, highlightthickness=1)
        caja.pack(side="left", fill="both", expand=True, padx=(0, 12))
        cabecera = tk.Frame(caja, bg=BLANCO)
        cabecera.pack(fill="x", padx=15, pady=(13, 3))
        tk.Label(cabecera, text=etiqueta, font=("Segoe UI", 9), bg=BLANCO, fg=GRIS).pack(side="left")
        tk.Label(cabecera, text=icono, font=("Segoe UI", 13, "bold"), bg="#EFF6FF", fg=color, padx=8, pady=3).pack(side="right")
        tk.Label(caja, text=valor, font=("Segoe UI", 19, "bold"), bg=BLANCO, fg=TEXTO).pack(anchor="w", padx=15, pady=(2, 14))

    # Panel inferior: gráfico de ventas y acciones rápidas
    fila_inferior = tk.Frame(contenido, bg=FONDO)
    fila_inferior.pack(fill="both", expand=True)

    panel_grafico = tk.Frame(fila_inferior, bg=BLANCO, highlightbackground=BORDE, highlightthickness=1)
    panel_grafico.pack(side="left", fill="both", expand=True, padx=(0, 14))
    tk.Label(panel_grafico, text="Ventas e ingresos", font=("Segoe UI", 12, "bold"), bg=BLANCO, fg=TEXTO).pack(anchor="w", padx=18, pady=(15, 0))
    tk.Label(panel_grafico, text="Ingresos de los últimos 7 días", font=("Segoe UI", 9), bg=BLANCO, fg=GRIS).pack(anchor="w", padx=18, pady=(2, 5))

    grafico = tk.Canvas(panel_grafico, bg=BLANCO, height=245, highlightthickness=0)
    grafico.pack(fill="both", expand=True, padx=12, pady=(0, 10))
    def dibujar_grafico(event=None):
        grafico.delete("all")
        w = max(grafico.winfo_width(), 300)
        h = max(grafico.winfo_height(), 220)
        izq, der, arriba, abajo = 48, w - 20, 18, h - 34
        maximo = max(valores) if valores else 0
        escala = maximo * 1.2 if maximo > 0 else 100
        for i in range(5):
            y = arriba + (abajo-arriba) * i / 4
            grafico.create_line(izq, y, der, y, fill="#E9EEF5", dash=(2, 3))
            etiqueta = escala * (4-i) / 4
            grafico.create_text(izq-8, y, text=f"${etiqueta:,.0f}", anchor="e", fill=GRIS, font=("Segoe UI", 8))
        puntos = []
        for i, v in enumerate(valores):
            x = izq + (der-izq) * i / 6
            y = abajo - (abajo-arriba) * v / escala
            puntos.extend((x, y))
            grafico.create_text(x, abajo+17, text=nombres_dias[i], fill=GRIS, font=("Segoe UI", 8))
        if len(puntos) >= 4:
            grafico.create_line(*puntos, fill="#2563EB", width=3, smooth=True)
            for i in range(0, len(puntos), 2):
                grafico.create_oval(puntos[i]-3, puntos[i+1]-3, puntos[i]+3, puntos[i+1]+3, fill="#2563EB", outline=BLANCO, width=1)
        elif puntos:
            grafico.create_oval(puntos[0]-4, puntos[1]-4, puntos[0]+4, puntos[1]+4, fill="#2563EB", outline="")
        if not any(valores):
            grafico.create_text((izq+der)/2, (arriba+abajo)/2, text="Todavía no hay ventas registradas en este período", fill=GRIS, font=("Segoe UI", 9))
    grafico.bind("<Configure>", dibujar_grafico)

    panel_acciones = tk.Frame(fila_inferior, bg=BLANCO, width=250, highlightbackground=BORDE, highlightthickness=1)
    panel_acciones.pack(side="right", fill="y")
    panel_acciones.pack_propagate(False)
    tk.Label(panel_acciones, text="Acciones rápidas", font=("Segoe UI", 12, "bold"), bg=BLANCO, fg=TEXTO).pack(anchor="w", padx=16, pady=(16, 3))
    tk.Label(panel_acciones, text="Tareas frecuentes", font=("Segoe UI", 9), bg=BLANCO, fg=GRIS).pack(anchor="w", padx=16, pady=(0, 12))
    for texto, detalle, destino in [
        ("＋  Nueva venta", "Registrar una venta", "Ventas"),
        ("▦  Productos", "Administrar el catálogo", "Productos"),
        ("⚠  Revisar stock", "Ver alertas de inventario", "Stock"),
    ]:
        btn = tb.Button(panel_acciones, text=f"{texto}\n{detalle}", bootstyle="light", command=lambda n=destino: mostrar_seccion(n), cursor="hand2")
        btn.pack(fill="x", padx=14, pady=5, ipady=8)

    # Resumen de las últimas operaciones
    panel_recientes = tk.Frame(contenido, bg=BLANCO, highlightbackground=BORDE, highlightthickness=1)
    panel_recientes.pack(fill="x", pady=(16, 0))
    tk.Label(panel_recientes, text="Ventas recientes", font=("Segoe UI", 11, "bold"), bg=BLANCO, fg=TEXTO).pack(anchor="w", padx=16, pady=(11, 5))
    if recientes:
        for venta_id, fecha, total in recientes[:3]:
            linea = tk.Frame(panel_recientes, bg=BLANCO)
            linea.pack(fill="x", padx=16, pady=3)
            tk.Label(linea, text=f"Venta #{venta_id}  ·  {fecha}", font=("Segoe UI", 9), bg=BLANCO, fg=GRIS).pack(side="left")
            tk.Label(linea, text=f"$ {float(total):,.2f}", font=("Segoe UI", 9, "bold"), bg=BLANCO, fg=TEXTO).pack(side="right")
    else:
        tk.Label(panel_recientes, text="Todavía no hay ventas registradas.", font=("Segoe UI", 9), bg=BLANCO, fg=GRIS).pack(anchor="w", padx=16, pady=(0, 12))


def mostrar_productos():
    limpiar()
    titulo.config(text="Productos")
    subtitulo.config(text="Administrá tu catálogo, precios y cantidades disponibles.")

    barra = tk.Frame(contenido, bg=FONDO)
    barra.pack(fill="x", pady=(0, 12))
    busqueda = tk.StringVar()
    tk.Label(barra, text="Buscar producto", font=("Segoe UI", 9, "bold"), bg=FONDO, fg=TEXTO).pack(side="left", padx=(0, 8))
    entrada = tb.Entry(barra, textvariable=busqueda, width=36)
    entrada.pack(side="left", ipady=5)

    marco_tabla, tabla = crear_tabla(contenido, ("id", "nombre", "precio", "stock"), ("ID", "PRODUCTO", "PRECIO", "STOCK"), (70, 400, 160, 110), ("center", "w", "e", "center"))
    marco_tabla.pack(fill="both", expand=True)

    formulario = tk.Frame(contenido, bg=BLANCO, highlightbackground=BORDE, highlightthickness=1)
    formulario.pack(fill="x", pady=(12, 0))
    tk.Label(formulario, text="Datos del producto", font=("Segoe UI", 11, "bold"), bg=BLANCO, fg=AZUL).grid(row=0, column=0, columnspan=6, sticky="w", padx=14, pady=(12, 8))
    id_edicion = tk.StringVar()
    campos = {}
    for col, (etiqueta, ancho) in enumerate((("Nombre", 30), ("Precio", 16), ("Stock", 12)), start=0):
        tk.Label(formulario, text=etiqueta, font=("Segoe UI", 9, "bold"), bg=BLANCO, fg=GRIS).grid(row=1, column=col, sticky="w", padx=14, pady=(0, 4))
        entrada_campo = tb.Entry(formulario, width=ancho)
        entrada_campo.grid(row=2, column=col, sticky="ew", padx=14, pady=(0, 13), ipady=4)
        campos[etiqueta] = entrada_campo

    def cancelar_edicion():
        id_edicion.set("")
        for campo in campos.values():
            campo.delete(0, tk.END)
        boton_guardar.config(text="Agregar producto")
        tabla.selection_remove(tabla.selection())

    def cargar():
        seleccion_anterior = tabla.selection()
        for item in tabla.get_children():
            tabla.delete(item)
        texto = busqueda.get().strip().casefold()
        for p in obtener_productos():
            if texto and texto not in str(p[1]).casefold():
                continue
            tabla.insert("", "end", values=(p[0], p[1], f"$ {float(p[2]):,.2f}", p[3]))

    def seleccionar(event=None):
        seleccionado = tabla.selection()
        if not seleccionado:
            return
        valores = tabla.item(seleccionado[0], "values")
        id_edicion.set(str(valores[0]))
        campos["Nombre"].delete(0, tk.END)
        campos["Nombre"].insert(0, valores[1])
        precio_limpio = str(valores[2]).replace("$", "").replace(",", "").strip()
        campos["Precio"].delete(0, tk.END)
        campos["Precio"].insert(0, precio_limpio)
        campos["Stock"].delete(0, tk.END)
        campos["Stock"].insert(0, str(valores[3]))
        boton_guardar.config(text="Guardar cambios")

    def guardar():
        nombre = campos["Nombre"].get().strip()
        precio_texto = campos["Precio"].get().strip().replace(",", ".")
        stock_texto = campos["Stock"].get().strip()
        if not nombre:
            messagebox.showwarning("Dato faltante", "Ingresá el nombre del producto.")
            return
        try:
            precio = float(precio_texto)
            stock = int(stock_texto)
            if precio < 0 or stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Datos incorrectos", "Ingresá un precio no negativo y un stock entero no negativo.")
            return
        conexion = conectar()
        try:
            if id_edicion.get():
                conexion.execute("UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?", (nombre, precio, stock, int(id_edicion.get())))
            else:
                conexion.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", (nombre, precio, stock))
            conexion.commit()
        except Exception as error:
            messagebox.showerror("Error al guardar", str(error))
            return
        finally:
            conexion.close()
        cancelar_edicion()
        cargar()
        messagebox.showinfo("Nexo Gestión", "Producto guardado correctamente.")

    def eliminar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccioná un producto", "Elegí una fila de la tabla.")
            return
        valores = tabla.item(seleccionado[0], "values")
        if not messagebox.askyesno("Confirmar eliminación", f"¿Eliminar el producto '{valores[1]}'?"):
            return
        conexion = conectar()
        try:
            conexion.execute("DELETE FROM productos WHERE id=?", (int(valores[0]),))
            conexion.commit()
        except Exception as error:
            messagebox.showerror("No se pudo eliminar", f"Es posible que el producto tenga ventas asociadas.\n\n{error}")
            return
        finally:
            conexion.close()
        cancelar_edicion()
        cargar()

    botonera = tk.Frame(contenido, bg=FONDO)
    botonera.pack(fill="x", pady=(10, 0))
    boton_guardar = tb.Button(botonera, text="Agregar producto", bootstyle="success", command=guardar, cursor="hand2")
    boton_guardar.pack(side="left", padx=(0, 8))
    tb.Button(botonera, text="Cancelar edición", bootstyle="secondary-outline", command=cancelar_edicion, cursor="hand2").pack(side="left", padx=4)
    tb.Button(botonera, text="Eliminar seleccionado", bootstyle="danger", command=eliminar, cursor="hand2").pack(side="left", padx=4)
    busqueda.trace_add("write", lambda *_: cargar())
    tabla.bind("<<TreeviewSelect>>", seleccionar)
    cargar()


def mostrar_stock():
    limpiar()
    titulo.config(text="Control de stock")
    subtitulo.config(text="Identificá productos agotados, con pocas unidades o disponibles.")
    productos = obtener_productos()
    agotados = sum(1 for p in productos if int(p[3]) == 0)
    bajos = sum(1 for p in productos if 0 < int(p[3]) <= 3)
    normales = sum(1 for p in productos if int(p[3]) > 3)

    resumen = tk.Frame(contenido, bg=FONDO)
    resumen.pack(fill="x", pady=(0, 14))
    for etiqueta, valor, color, fondo in (("Agotados", agotados, ROJO, "#FEE2E2"), ("Stock bajo", bajos, NARANJA, "#FEF3C7"), ("Stock normal", normales, VERDE, "#D1FAE5")):
        caja = tk.Frame(resumen, bg=fondo)
        caja.pack(side="left", padx=(0, 10))
        tk.Label(caja, text=etiqueta.upper(), font=("Segoe UI", 8, "bold"), bg=fondo, fg=color).pack(anchor="w", padx=15, pady=(10, 2))
        tk.Label(caja, text=str(valor), font=("Segoe UI", 17, "bold"), bg=fondo, fg=color).pack(anchor="w", padx=15, pady=(0, 10))

    marco, tabla = crear_tabla(contenido, ("id", "nombre", "precio", "stock", "estado"), ("ID", "PRODUCTO", "PRECIO", "UNIDADES", "ESTADO"), (70, 350, 150, 120, 150), ("center", "w", "e", "center", "center"))
    marco.pack(fill="both", expand=True)
    tabla.tag_configure("agotado", background="#FFF1F2", foreground="#9F1239")
    tabla.tag_configure("bajo", background="#FFFBEB", foreground="#92400E")
    tabla.tag_configure("normal", background="#FFFFFF", foreground=TEXTO)
    for p in productos:
        cantidad = int(p[3])
        if cantidad == 0:
            estado, tag = "AGOTADO", "agotado"
        elif cantidad <= 3:
            estado, tag = "STOCK BAJO", "bajo"
        else:
            estado, tag = "NORMAL", "normal"
        tabla.insert("", "end", values=(p[0], p[1], f"$ {float(p[2]):,.2f}", cantidad, estado), tags=(tag,))


def mostrar_ventas():
    limpiar()
    titulo.config(text="Ventas")
    subtitulo.config(text="Armá el carrito, revisá el total y registrá la operación.")
    carrito = {}
    catalogo = {}

    panel = tk.Frame(contenido, bg=BLANCO, highlightbackground=BORDE, highlightthickness=1)
    panel.pack(fill="x", pady=(0, 12))
    tk.Label(panel, text="Agregar productos al carrito", font=("Segoe UI", 11, "bold"), bg=BLANCO, fg=AZUL).grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(12, 8))
    tk.Label(panel, text="Producto", bg=BLANCO, fg=GRIS, font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=15, pady=(0, 4))
    tk.Label(panel, text="Cantidad", bg=BLANCO, fg=GRIS, font=("Segoe UI", 9, "bold")).grid(row=1, column=1, sticky="w", padx=10, pady=(0, 4))
    selector = ttk.Combobox(panel, state="readonly", width=58)
    selector.grid(row=2, column=0, sticky="w", padx=15, pady=(0, 14))
    campo_cantidad = tb.Entry(panel, width=12)
    campo_cantidad.insert(0, "1")
    campo_cantidad.grid(row=2, column=1, sticky="w", padx=10, pady=(0, 14), ipady=3)

    marco, tabla = crear_tabla(contenido, ("id", "nombre", "cantidad", "precio", "subtotal"), ("ID", "PRODUCTO", "CANTIDAD", "PRECIO UNIT.", "SUBTOTAL"), (65, 360, 100, 150, 150), ("center", "w", "center", "e", "e"))
    marco.pack(fill="both", expand=True)
    catalogo = {}

    def cargar_catalogo():
        catalogo.clear()
        opciones = []
        for p in obtener_productos():
            pid, nombre, precio, stock = p
            if int(stock) > 0:
                etiqueta = f"{pid} - {nombre} (Stock: {stock}) - $ {float(precio):,.2f}"
                catalogo[etiqueta] = {"id": int(pid), "nombre": nombre, "precio": float(precio), "stock": int(stock)}
                opciones.append(etiqueta)
        selector["values"] = opciones
        if opciones:
            selector.current(0)
        else:
            selector.set("No hay productos con stock disponible")

    total_var = tk.StringVar(value="$ 0.00")
    pie = tk.Frame(contenido, bg=FONDO)
    pie.pack(fill="x", pady=(12, 8))
    tk.Label(pie, text="TOTAL DE LA VENTA", font=("Segoe UI", 11, "bold"), bg=FONDO, fg=AZUL).pack(side="left")
    tk.Label(pie, textvariable=total_var, font=("Segoe UI", 21, "bold"), bg=FONDO, fg=VERDE).pack(side="left", padx=14)

    def actualizar_carrito():
        for item in tabla.get_children():
            tabla.delete(item)
        total = 0.0
        for pid, item in carrito.items():
            subtotal = round(item["precio"] * item["cantidad"], 2)
            total += subtotal
            tabla.insert("", "end", iid=str(pid), values=(pid, item["nombre"], item["cantidad"], f"$ {item['precio']:,.2f}", f"$ {subtotal:,.2f}"))
        total_var.set(f"$ {total:,.2f}")

    def agregar_producto():
        etiqueta = selector.get()
        if etiqueta not in catalogo:
            messagebox.showwarning("Producto", "Seleccioná un producto con stock disponible.")
            return
        try:
            cantidad = int(campo_cantidad.get().strip())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Cantidad incorrecta", "Ingresá una cantidad entera mayor que cero.")
            return
        p = catalogo[etiqueta]
        actual = carrito.get(p["id"], {"cantidad": 0})["cantidad"]
        if actual + cantidad > p["stock"]:
            messagebox.showwarning("Stock insuficiente", f"Solo hay {p['stock']} unidades disponibles.")
            return
        if p["id"] in carrito:
            carrito[p["id"]]["cantidad"] += cantidad
        else:
            carrito[p["id"]] = {"nombre": p["nombre"], "precio": p["precio"], "cantidad": cantidad}
        campo_cantidad.delete(0, tk.END)
        campo_cantidad.insert(0, "1")
        actualizar_carrito()

    def quitar_producto():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccioná un producto", "Elegí una fila del carrito para quitarla.")
            return
        carrito.pop(int(seleccionado[0]), None)
        actualizar_carrito()

    def finalizar_venta():
        if not carrito:
            messagebox.showwarning("Venta vacía", "Agregá al menos un producto antes de finalizar.")
            return
        if not messagebox.askyesno("Confirmar venta", "¿Registrar esta venta y descontar el stock?"):
            return
        conexion = conectar()
        try:
            conexion.execute("BEGIN IMMEDIATE")
            detalles = []
            total = 0.0
            for pid, item in carrito.items():
                producto = conexion.execute("SELECT nombre, precio, stock FROM productos WHERE id=?", (pid,)).fetchone()
                if producto is None:
                    raise ValueError(f"El producto ID {pid} ya no existe.")
                nombre, precio, stock = producto
                cantidad = int(item["cantidad"])
                if cantidad > int(stock):
                    raise ValueError(f"Stock insuficiente para {nombre}. Disponible: {stock}.")
                precio = float(precio)
                subtotal = round(precio * cantidad, 2)
                total += subtotal
                detalles.append((pid, nombre, cantidad, precio, subtotal))
            total = round(total, 2)
            cursor = conexion.execute("INSERT INTO ventas (total) VALUES (?)", (total,))
            venta_id = cursor.lastrowid
            for pid, nombre, cantidad, precio, subtotal in detalles:
                conexion.execute("INSERT INTO detalle_venta (venta_id, producto_id, nombre_producto, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?, ?)", (venta_id, pid, nombre, cantidad, precio, subtotal))
                conexion.execute("UPDATE productos SET stock=stock-? WHERE id=?", (cantidad, pid))
            conexion.commit()
        except Exception as error:
            conexion.rollback()
            messagebox.showerror("No se pudo registrar la venta", str(error))
            return
        finally:
            conexion.close()
        carrito.clear()
        actualizar_carrito()
        cargar_catalogo()
        messagebox.showinfo("Venta registrada", f"Venta N.º {venta_id} guardada correctamente.\nTotal: $ {total:,.2f}\n\nEl stock fue actualizado.")

    botones = tk.Frame(contenido, bg=FONDO)
    botones.pack(fill="x")
    tb.Button(botones, text="Agregar producto", bootstyle="primary", command=agregar_producto, cursor="hand2").pack(side="left", padx=(0, 8))
    tb.Button(botones, text="Quitar del carrito", bootstyle="secondary-outline", command=quitar_producto, cursor="hand2").pack(side="left", padx=4)
    tb.Button(botones, text="Finalizar venta", bootstyle="success", command=finalizar_venta, cursor="hand2").pack(side="right")
    cargar_catalogo()


def mostrar_historial_ventas():
    limpiar()
    titulo.config(text="Historial de ventas")
    subtitulo.config(text="Buscá operaciones anteriores, consultá su detalle o generá comprobantes PDF.")

    filtros = tk.Frame(contenido, bg=FONDO)
    filtros.pack(fill="x", pady=(0, 12))
    buscar_id = tk.StringVar()
    tk.Label(filtros, text="N.º de venta", bg=FONDO, fg=GRIS, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
    entrada_busqueda = tb.Entry(filtros, textvariable=buscar_id, width=10)
    entrada_busqueda.pack(side="left", padx=(0, 12), ipady=4)
    tk.Label(filtros, text="Desde (AAAA-MM-DD)", bg=FONDO, fg=GRIS, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
    fecha_desde = tb.Entry(filtros, width=14)
    fecha_desde.pack(side="left", padx=(0, 10), ipady=4)
    tk.Label(filtros, text="Hasta", bg=FONDO, fg=GRIS, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
    fecha_hasta = tb.Entry(filtros, width=14)
    fecha_hasta.pack(side="left", padx=(0, 10), ipady=4)

    resumen = tk.Frame(contenido, bg=FONDO)
    resumen.pack(fill="x", pady=(0, 12))
    tarjeta_cantidad = tarjeta(resumen, "Ventas encontradas", "0", AZUL, "Operaciones")
    tarjeta_cantidad.pack(side="left", fill="both", expand=True, padx=(0, 12))
    tarjeta_total = tarjeta(resumen, "Facturación total", "$ 0.00", VERDE, "Facturación")
    tarjeta_total.pack(side="left", fill="both", expand=True)
    lbl_cantidad = tarjeta_cantidad.winfo_children()[1].winfo_children()[-1]
    lbl_total = tarjeta_total.winfo_children()[1].winfo_children()[-1]

    marco, tabla = crear_tabla(contenido, ("id", "fecha", "total"), ("N.º VENTA", "FECHA Y HORA", "TOTAL"), (130, 300, 180), ("center", "center", "e"))
    marco.pack(fill="both", expand=True)

    def cargar_ventas():
        texto_id, desde, hasta = buscar_id.get().strip(), fecha_desde.get().strip(), fecha_hasta.get().strip()
        if texto_id and not texto_id.isdigit():
            messagebox.showwarning("Número incorrecto", "Ingresá un número de venta válido.")
            return
        for fecha in (desde, hasta):
            if fecha:
                try:
                    datetime.strptime(fecha, "%Y-%m-%d")
                except ValueError:
                    messagebox.showwarning("Fecha incorrecta", "Usá AAAA-MM-DD, por ejemplo 2026-10-21.")
                    return
        if desde and hasta and desde > hasta:
            messagebox.showwarning("Fechas incorrectas", "La fecha inicial no puede superar la final.")
            return
        conexion = conectar()
        try:
            ventas = conexion.execute("SELECT id, fecha, total FROM ventas ORDER BY id DESC").fetchall()
        except Exception as error:
            messagebox.showerror("Error al cargar el historial", str(error))
            return
        finally:
            conexion.close()
        for item in tabla.get_children():
            tabla.delete(item)
        cantidad, total_general = 0, 0.0
        for venta in ventas:
            venta_id, fecha_venta, total = venta
            fecha_dia = str(fecha_venta)[:10]
            if texto_id and texto_id != str(venta_id):
                continue
            if desde and fecha_dia < desde:
                continue
            if hasta and fecha_dia > hasta:
                continue
            tabla.insert("", "end", values=(venta_id, fecha_venta, f"$ {float(total):,.2f}"))
            cantidad += 1
            total_general += float(total)
        lbl_cantidad.config(text=str(cantidad))
        lbl_total.config(text=f"$ {total_general:,.2f}")

    def limpiar_filtros():
        buscar_id.set("")
        fecha_desde.delete(0, tk.END)
        fecha_hasta.delete(0, tk.END)
        cargar_ventas()

    def obtener_venta_seleccionada():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccioná una venta", "Elegí una venta de la tabla.")
            return None
        return tabla.item(seleccionado[0], "values")

    def ver_detalle():
        valores = obtener_venta_seleccionada()
        if not valores:
            return
        venta_id = int(valores[0])
        conexion = conectar()
        try:
            detalles = conexion.execute("SELECT nombre_producto, cantidad, precio_unitario, subtotal FROM detalle_venta WHERE venta_id=?", (venta_id,)).fetchall()
        except Exception as error:
            messagebox.showerror("Error al consultar el detalle", str(error))
            return
        finally:
            conexion.close()
        if not detalles:
            messagebox.showinfo("Detalle de venta", "No se encontraron productos para esta venta.")
            return
        ventana = tk.Toplevel(app)
        ventana.title(f"Detalle de venta N.º {venta_id}")
        ventana.geometry("650x430")
        ventana.configure(bg=FONDO)
        tk.Label(ventana, text=f"Venta N.º {venta_id}", font=("Segoe UI", 18, "bold"), bg=FONDO, fg=AZUL).pack(anchor="w", padx=20, pady=(18, 3))
        tk.Label(ventana, text=f"Fecha: {valores[1]}", font=("Segoe UI", 10), bg=FONDO, fg=GRIS).pack(anchor="w", padx=20, pady=(0, 12))
        marco, detalle_tabla = crear_tabla(ventana, ("producto", "cantidad", "precio", "subtotal"), ("PRODUCTO", "CANTIDAD", "PRECIO UNIT.", "SUBTOTAL"), (260, 90, 120, 120), ("w", "center", "e", "e"))
        marco.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        for nombre, cantidad, precio, subtotal in detalles:
            detalle_tabla.insert("", "end", values=(nombre, cantidad, f"$ {float(precio):,.2f}", f"$ {float(subtotal):,.2f}"))

    def generar_comprobante():
        valores = obtener_venta_seleccionada()
        if not valores:
            return
        venta_id = int(valores[0])
        conexion = conectar()
        try:
            detalles = conexion.execute("SELECT nombre_producto, cantidad, precio_unitario, subtotal FROM detalle_venta WHERE venta_id=?", (venta_id,)).fetchall()
            try:
                negocio = conexion.execute("SELECT nombre, cuit, direccion, telefono FROM datos_negocio WHERE id=1").fetchone()
            except Exception:
                negocio = None
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo consultar la venta:\n{error}")
            return
        finally:
            conexion.close()
        if not detalles:
            messagebox.showwarning("Sin detalles", "Esta venta no tiene productos registrados.")
            return
        nombre_negocio, cuit, direccion, telefono = negocio if negocio else ("Mi negocio", "", "", "")
        ruta = filedialog.asksaveasfilename(title="Guardar comprobante PDF", defaultextension=".pdf", initialfile=f"comprobante_venta_{venta_id}.pdf", filetypes=[("Documento PDF", "*.pdf")])
        if not ruta:
            return
        try:
            ancho, alto = A4
            pdf = canvas.Canvas(ruta, pagesize=A4)
            azul = colors.HexColor(AZUL)
            verde = colors.HexColor(VERDE)
            gris = colors.HexColor(GRIS)
            claro = colors.HexColor("#F1F5F9")
            texto = colors.HexColor(TEXTO)
            blanco = colors.white
            margen = 42
            ancho_util = ancho - 2 * margen

            def encabezado_pdf():
                pdf.setFillColor(azul)
                pdf.rect(0, alto - 150, ancho, 150, fill=1, stroke=0)
                pdf.setFillColor(blanco)
                pdf.setFont("Helvetica-Bold", 27)
                pdf.drawString(margen, alto - 43, "NEXO")
                pdf.setFont("Helvetica", 9)
                pdf.drawString(margen, alto - 60, "GESTIÓN COMERCIAL")
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(margen, alto - 87, str(nombre_negocio or "Mi negocio")[:45])
                pdf.setFont("Helvetica", 8)
                if cuit:
                    pdf.drawString(margen, alto - 103, f"CUIT: {str(cuit)[:38]}")
                if direccion:
                    pdf.drawString(margen, alto - 118, str(direccion)[:55])
                if telefono:
                    pdf.drawString(margen, alto - 133, f"Tel.: {str(telefono)[:30]}")
                pdf.setFont("Helvetica-Bold", 15)
                pdf.drawRightString(ancho - margen, alto - 45, "COMPROBANTE")
                pdf.setFont("Helvetica", 10)
                pdf.drawRightString(ancho - margen, alto - 63, "DE VENTA")
                pdf.setFillColor(texto)
                pdf.setFont("Helvetica-Bold", 10)
                pdf.drawString(margen, alto - 177, f"Venta N.º {venta_id}")
                pdf.setFillColor(gris)
                pdf.setFont("Helvetica", 9)
                pdf.drawRightString(ancho - margen, alto - 177, f"Fecha: {valores[1]}")

            def encabezado_tabla(y_base):
                pdf.setFillColor(claro)
                pdf.roundRect(margen, y_base - 7, ancho_util, 26, 4, fill=1, stroke=0)
                pdf.setFillColor(azul)
                pdf.setFont("Helvetica-Bold", 8)
                pdf.drawString(margen + 10, y_base + 1, "PRODUCTO")
                pdf.drawRightString(ancho - 205, y_base + 1, "CANT.")
                pdf.drawRightString(ancho - 120, y_base + 1, "PRECIO")
                pdf.drawRightString(ancho - margen - 10, y_base + 1, "SUBTOTAL")
                return y_base - 26

            encabezado_pdf()
            y = encabezado_tabla(alto - 213)
            total = 0.0
            for nombre, cantidad, precio, subtotal in detalles:
                precio, subtotal = float(precio), float(subtotal)
                total += subtotal
                if y < 105:
                    pdf.showPage()
                    y = alto - 65
                    pdf.setFillColor(azul)
                    pdf.setFont("Helvetica-Bold", 13)
                    pdf.drawString(margen, y, f"NEXO - Venta N.º {venta_id}")
                    y = encabezado_tabla(y - 30)
                nombre = str(nombre)
                max_ancho = ancho - 2 * margen - 220
                visible = nombre
                while visible and stringWidth(visible, "Helvetica", 9) > max_ancho:
                    visible = visible[:-1]
                if visible != nombre:
                    visible = visible[:-3] + "..."
                pdf.setFillColor(texto)
                pdf.setFont("Helvetica", 9)
                pdf.drawString(margen + 10, y, visible)
                pdf.drawRightString(ancho - 205, y, str(cantidad))
                pdf.drawRightString(ancho - 120, y, f"$ {precio:,.2f}")
                pdf.drawRightString(ancho - margen - 10, y, f"$ {subtotal:,.2f}")
                y -= 23
                pdf.setStrokeColor(claro)
                pdf.line(margen, y + 10, ancho - margen, y + 10)
            if y < 90:
                pdf.showPage()
                y = alto - 75
            y -= 8
            pdf.setFillColor(verde)
            pdf.roundRect(margen, y - 15, ancho_util, 46, 6, fill=1, stroke=0)
            pdf.setFillColor(blanco)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(margen + 15, y + 1, "TOTAL DE LA VENTA")
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawRightString(ancho - margen - 15, y, f"$ {total:,.2f}")
            pdf.setFillColor(gris)
            pdf.setFont("Helvetica", 9)
            pdf.drawCentredString(ancho / 2, 38, "Gracias por su compra.")
            pdf.setFont("Helvetica", 7)
            pdf.drawCentredString(ancho / 2, 25, "NEXO GESTIÓN COMERCIAL")
            pdf.save()
            messagebox.showinfo("PDF generado", f"El comprobante se guardó correctamente:\n{ruta}")
        except Exception as error:
            messagebox.showerror("Error al generar el PDF", str(error))

    tb.Button(filtros, text="Buscar", bootstyle="primary", command=cargar_ventas, cursor="hand2").pack(side="left", padx=3)
    tb.Button(filtros, text="Mostrar todas", bootstyle="secondary-outline", command=limpiar_filtros, cursor="hand2").pack(side="left", padx=3)
    botones = tk.Frame(contenido, bg=FONDO)
    botones.pack(fill="x", pady=(10, 0))
    tb.Button(botones, text="Ver detalle", bootstyle="primary", command=ver_detalle, cursor="hand2").pack(side="left", padx=(0, 8))
    tb.Button(botones, text="Generar comprobante PDF", bootstyle="success", command=generar_comprobante, cursor="hand2").pack(side="left", padx=4)
    entrada_busqueda.bind("<Return>", lambda event: cargar_ventas())
    cargar_ventas()


def mostrar_reportes():
    limpiar()
    titulo.config(text="Reportes")
    subtitulo.config(text="Analizá los ingresos y conocé cuáles son tus productos más vendidos.")
    pestañas = ttk.Notebook(contenido)
    pestañas.pack(fill="both", expand=True)
    pagina_diaria = tk.Frame(pestañas, bg=FONDO)
    pagina_mensual = tk.Frame(pestañas, bg=FONDO)
    pagina_productos = tk.Frame(pestañas, bg=FONDO)
    pestañas.add(pagina_diaria, text="Ingresos diarios")
    pestañas.add(pagina_mensual, text="Ingresos mensuales")
    pestañas.add(pagina_productos, text="Más vendidos")
    _, tabla_diaria = crear_tabla(pagina_diaria, ("fecha", "cantidad", "total"), ("FECHA", "VENTAS REGISTRADAS", "INGRESOS"), (220, 220, 220), ("center", "center", "e"))
    _, tabla_mensual = crear_tabla(pagina_mensual, ("mes", "cantidad", "total"), ("MES", "VENTAS REGISTRADAS", "INGRESOS"), (220, 220, 220), ("center", "center", "e"))
    _, tabla_productos = crear_tabla(pagina_productos, ("producto", "unidades", "ingresos"), ("PRODUCTO", "UNIDADES VENDIDAS", "INGRESOS"), (350, 200, 220), ("w", "center", "e"))
    for tabla in (tabla_diaria, tabla_mensual, tabla_productos):
        tabla.master.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_reportes():
        for tabla in (tabla_diaria, tabla_mensual, tabla_productos):
            for item in tabla.get_children():
                tabla.delete(item)
        conexion = conectar()
        try:
            diarios = conexion.execute("SELECT date(fecha), COUNT(*), ROUND(SUM(total), 2) FROM ventas GROUP BY date(fecha) ORDER BY date(fecha) DESC").fetchall()
            for fecha, cantidad, total in diarios:
                tabla_diaria.insert("", "end", values=(fecha, cantidad, f"$ {float(total or 0):,.2f}"))
            mensuales = conexion.execute("SELECT strftime('%Y-%m', fecha), COUNT(*), ROUND(SUM(total), 2) FROM ventas GROUP BY strftime('%Y-%m', fecha) ORDER BY strftime('%Y-%m', fecha) DESC").fetchall()
            for mes, cantidad, total in mensuales:
                tabla_mensual.insert("", "end", values=(mes or "Sin fecha", cantidad, f"$ {float(total or 0):,.2f}"))
            vendidos = conexion.execute("SELECT nombre_producto, SUM(cantidad), ROUND(SUM(subtotal), 2) FROM detalle_venta GROUP BY nombre_producto ORDER BY SUM(cantidad) DESC, SUM(subtotal) DESC").fetchall()
            for nombre, unidades, ingresos in vendidos:
                tabla_productos.insert("", "end", values=(nombre, unidades, f"$ {float(ingresos or 0):,.2f}"))
        except Exception as error:
            messagebox.showerror("Error en los reportes", str(error))
        finally:
            conexion.close()

    tb.Button(contenido, text="Actualizar reportes", bootstyle="primary", command=cargar_reportes, cursor="hand2").pack(anchor="e", pady=(10, 0))
    cargar_reportes()


def mostrar_datos_negocio():
    limpiar()
    titulo.config(text="Datos del negocio")
    subtitulo.config(text="Esta información aparecerá en los comprobantes PDF.")
    conexion = conectar()
    try:
        conexion.execute("CREATE TABLE IF NOT EXISTS datos_negocio (id INTEGER PRIMARY KEY CHECK (id = 1), nombre TEXT NOT NULL DEFAULT '', cuit TEXT NOT NULL DEFAULT '', direccion TEXT NOT NULL DEFAULT '', telefono TEXT NOT NULL DEFAULT '')")
        conexion.execute("INSERT OR IGNORE INTO datos_negocio (id, nombre, cuit, direccion, telefono) VALUES (1, '', '', '', '')")
        conexion.commit()
        datos = conexion.execute("SELECT nombre, cuit, direccion, telefono FROM datos_negocio WHERE id=1").fetchone()
    finally:
        conexion.close()

    tarjeta_form = tk.Frame(contenido, bg=BLANCO, highlightbackground=BORDE, highlightthickness=1)
    tarjeta_form.pack(fill="x", anchor="n")
    tk.Label(tarjeta_form, text="Información del comercio", font=("Segoe UI", 13, "bold"), bg=BLANCO, fg=AZUL).pack(anchor="w", padx=22, pady=(20, 5))
    tk.Label(tarjeta_form, text="Completá los datos que quieras mostrar en los comprobantes.", font=("Segoe UI", 9), bg=BLANCO, fg=GRIS).pack(anchor="w", padx=22, pady=(0, 12))
    entradas = {}
    for etiqueta, valor in zip(("Nombre del comercio", "CUIT", "Dirección", "Teléfono"), datos or ("", "", "", "")):
        tk.Label(tarjeta_form, text=etiqueta, font=("Segoe UI", 9, "bold"), bg=BLANCO, fg=TEXTO).pack(anchor="w", padx=22, pady=(8, 4))
        entrada = tb.Entry(tarjeta_form)
        entrada.pack(fill="x", padx=22, pady=(0, 5), ipady=5)
        entrada.insert(0, valor or "")
        entradas[etiqueta] = entrada

    def guardar_datos():
        nombre = entradas["Nombre del comercio"].get().strip()
        cuit = entradas["CUIT"].get().strip()
        direccion = entradas["Dirección"].get().strip()
        telefono = entradas["Teléfono"].get().strip()
        if not nombre:
            messagebox.showwarning("Falta el nombre", "Ingresá el nombre del comercio.")
            return
        conexion = conectar()
        try:
            conexion.execute("UPDATE datos_negocio SET nombre=?, cuit=?, direccion=?, telefono=? WHERE id=1", (nombre, cuit, direccion, telefono))
            conexion.commit()
        except Exception as error:
            messagebox.showerror("Error al guardar", str(error))
            return
        finally:
            conexion.close()
        messagebox.showinfo("Datos guardados", "Los datos del negocio se guardaron correctamente.")

    tb.Button(contenido, text="Guardar datos del negocio", bootstyle="success", command=guardar_datos, cursor="hand2").pack(anchor="w", pady=14)


def mostrar_seccion(nombre):
    seccion_activa["nombre"] = nombre
    for nombre_boton, boton in botones_menu.items():
        if nombre_boton == nombre:
            boton.configure(
                bg="#EAF1FF", fg="#2563EB",
                activebackground="#DFE9FF", activeforeground="#1D4ED8",
                font=("Segoe UI", 9, "bold")
            )
        else:
            boton.configure(
                bg=BLANCO, fg="#64748B",
                activebackground="#F4F7FB", activeforeground="#334155",
                font=("Segoe UI", 9)
            )
    funciones = {
        "Inicio": mostrar_inicio,
        "Productos": mostrar_productos,
        "Ventas": mostrar_ventas,
        "Historial de ventas": mostrar_historial_ventas,
        "Stock": mostrar_stock,
        "Reportes": mostrar_reportes,
        "Datos del negocio": mostrar_datos_negocio,
    }
    funcion = funciones.get(nombre)
    if funcion:
        funcion()


# Navegación lateral: botones planos, iconos y selección azul suave
opciones_menu = [
    ("▦", "Inicio", "Dashboard"),
    ("◇", "Productos", "Productos"),
    ("＋", "Ventas", "Ventas"),
    ("◷", "Historial de ventas", "Historial de ventas"),
    ("▤", "Stock", "Stock"),
    ("▥", "Reportes", "Reportes"),
    ("⚙", "Datos del negocio", "Datos del negocio"),
]
contenedor_nav = tk.Frame(menu, bg=BLANCO)
contenedor_nav.pack(fill="x", padx=8, pady=(12, 0))
for icono, nombre, etiqueta in opciones_menu:
    activo = nombre == "Inicio"
    boton = tk.Button(
        contenedor_nav,
        text=f"{icono}   {etiqueta}",
        command=lambda n=nombre: mostrar_seccion(n),
        cursor="hand2",
        anchor="w",
        padx=11,
        pady=9,
        bd=0,
        relief="flat",
        highlightthickness=0,
        bg="#EAF1FF" if activo else BLANCO,
        fg="#2563EB" if activo else "#64748B",
        activebackground="#DFE9FF" if activo else "#F4F7FB",
        activeforeground="#1D4ED8",
        font=("Segoe UI", 9, "bold" if activo else "normal")
    )
    boton.pack(fill="x", pady=2)
    botones_menu[nombre] = boton

# Pie del menú, similar al recuadro informativo de la referencia
pie_menu = tk.Frame(menu, bg=BLANCO)
pie_menu.pack(side="bottom", fill="x", padx=9, pady=(8, 12))
tk.Frame(pie_menu, bg="#E9EEF5", height=1).pack(fill="x", pady=(0, 10))
aviso = tk.Frame(pie_menu, bg="#EEF4FF", highlightbackground="#D9E6FF", highlightthickness=1)
aviso.pack(fill="x")
tk.Label(aviso, text="ⓘ  Nexo Gestión", font=("Segoe UI", 8, "bold"), bg="#EEF4FF", fg="#2563EB").pack(anchor="w", padx=9, pady=(8, 3))
tk.Label(aviso, text="Tu negocio, bajo control.\nAdministrá productos, ventas\ny stock desde un solo lugar.", font=("Segoe UI", 7), bg="#EEF4FF", fg="#64748B", justify="left").pack(anchor="w", padx=9, pady=(0, 9))

mostrar_inicio()
app.mainloop()
