import tkinter as tk
from tkinter import ttk
from services.my_sql import conectar
from services.manipular_sql import manipular
from tkinter import messagebox
from tkinter import font as tkfont


def abrir_editor(ventana, producto_id, nombre, precio, cantidad):
    editor = tk.Toplevel(ventana)
    editor.title(f"Editar: {nombre}")
    editor.geometry("320x320")
    editor.config(bg="#f0f0f5")

    tk.Label(editor, text=f"Producto: {nombre}", bg="#f0f0f5", fg="#4b3f72",
             font=("Calibri", 14, "bold")).pack(pady=7)
    tk.Label(editor, text="Precio (Q):", bg="#f0f0f5", fg="#3b3a5a", font=("Calibri", 11)).pack()
    entry_precio = tk.Entry(editor, font=("Calibri", 12), justify="center", bd=2, relief="groove")
    entry_precio.insert(0, str(precio))
    entry_precio.pack(pady=4, ipadx=4, ipady=2)

    tk.Label(editor, text="Cantidad:", bg="#f0f0f5", fg="#3b3a5a", font=("Calibri", 11)).pack()
    entry_cantidad = tk.Entry(editor, font=("Calibri", 12), justify="center", bd=2, relief="groove")
    entry_cantidad.insert(0, str(cantidad))
    entry_cantidad.pack(pady=4, ipadx=4, ipady=2)

    def guardar_cambios():
        try:
            nuevo_precio = float(entry_precio.get())
            nueva_cantidad = int(entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Precio y cantidad deben ser números válidos.")
            return
        sql = "UPDATE productos SET precio=%s, cantidad=%s WHERE id=%s"
        filas_afectadas = manipular(sql, (nuevo_precio, nueva_cantidad, producto_id))
        if filas_afectadas:
            editor.destroy()
            cargar_productos(ventana)

    def eliminar_producto():
        sql = "DELETE FROM productos WHERE id=%s"
        confirmado = messagebox.askyesno("Eliminar", f"¿Estás seguro de eliminar '{nombre}'?")
        if confirmado:
            manipular(sql, (producto_id,))
            editor.destroy()
            cargar_productos(ventana)

    btn_guardar = tk.Button(editor, text="Guardar", bg="#6a5acd", fg="white",
                           font=("Calibri", 12, "bold"), command=guardar_cambios, bd=0,
                           activebackground="#836fff", cursor="hand2")
    btn_guardar.pack(pady=(10, 5), ipadx=10, ipady=3)

    btn_eliminar = tk.Button(editor, text="Eliminar", bg="#d9534f", fg="white",
                             font=("Calibri", 12, "bold"), command=eliminar_producto, bd=0,
                             activebackground="#e06b68", cursor="hand2")
    btn_eliminar.pack(ipadx=10, ipady=3)


def cargar_productos(ventana, campo_filtro=None, texto_filtro=None):
    color_fondo = "#f5f3f7"  # fondo claro neutro
    color_tarjeta = "#ffffff"
    color_borde = "#c9c9d1"
    color_titulo = "#4b3f72"  # morado oscuro
    color_encabezado = "#280b6a"  # lilac claro
    color_texto = "#3b3a5a"  # azul grisáceo

    ventana.update_idletasks()

    for widget in ventana.place_slaves():
        if isinstance(widget, tk.Frame) and widget.place_info().get("relx") == '0.2':
            widget.destroy()

    productos_panel = tk.Frame(ventana, bg=color_fondo, highlightbackground=color_borde, highlightthickness=1)
    productos_panel.place(relx=0.18, rely=0, relwidth=0.82, relheight=1)

    titulo = tk.Label(productos_panel, text="Productos Disponibles",
                      fg=color_titulo, bg=color_fondo, font=("Bauhaus 93", 40, "bold"), anchor="center")
    titulo.place(relx=0.02, y=15, relwidth=0.95)

    boton_actualizar = tk.Button(productos_panel,
                                text="""Cargar De
Nuevo""",       
                                bg="#6a5acd", fg="white",
                                borderwidth=1.5,
                                font=("Lucida Bright", 12, "bold"), padx=15, pady=6, bd=0,
                                activebackground="#280b6a",
                                relief="flat",
                                cursor="hand2",
                                command=lambda: cargar_productos(ventana, campo_filtro, texto_filtro))
    boton_actualizar.place(relx=0.05, y=8)

    canvas = tk.Canvas(productos_panel, bg=color_fondo, bd=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(productos_panel, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.place(relx=0.025, rely=0.1, relwidth=0.94, relheight=0.85)
    scrollbar.place(relx=0.965, rely=0.1, relheight=0.85)

    frame_interno = tk.Frame(canvas, bg=color_fondo)
    canvas_window = canvas.create_window((0, 0), window=frame_interno, anchor="nw", tags="frame_interno")

    def ajustar_ancho(event):
        canvas.itemconfig("frame_interno", width=event.width)
    canvas.bind("<Configure>", ajustar_ancho)

    frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    encabezados = ["No.", "Nombres", "Precios", "Cantidad", "Categorías"]

    # Títulos centrados y con bordes planos
    for col, texto in enumerate(encabezados):
        label = tk.Label(frame_interno, text=texto, bg=color_encabezado, fg=color_tarjeta,
                         font=("Gill Sans Ultra Bold", 13, "bold"), borderwidth=2, relief="solid",
                         padx=5, pady=8)
        label.grid(row=0, column=col, sticky="nsew")

    consulta_sql = """
        SELECT p.id, p.nombre, p.precio, p.cantidad, c.nombre 
        FROM productos p 
        LEFT JOIN categorias c ON p.categoria_id = c.id
    """

    parametros = ()
    if campo_filtro and texto_filtro and texto_filtro.strip() != "":
        campo_bd_map = {
            "Nombre": "p.nombre",
            "Precio": "p.precio",
            "Cantidad": "p.cantidad",
            "Categoría": "c.nombre"
        }
        columna = campo_bd_map.get(campo_filtro)
        if columna:
            if campo_filtro in ["Precio", "Cantidad"]:
                consulta_sql += f" WHERE {columna} = %s "
                try:
                    if campo_filtro == "Precio":
                        val = float(texto_filtro)
                    else:
                        val = int(texto_filtro)
                    parametros = (val,)
                except ValueError:
                    parametros = ("-1",)
            else:
                consulta_sql += f" WHERE {columna} LIKE %s "
                parametros = (f"%{texto_filtro}%",)
    consulta_sql += " ORDER BY p.id"

    productos_consulta = conectar(consulta_sql, parametros)

    for index, producto in enumerate(productos_consulta, start=1):
        producto_id = producto[0]
        nombre = producto[1]
        precio = producto[2]
        cantidad = producto[3]
        categoria = producto[4] if producto[4] else "Sin categoría"

        datos = [
            str(index),
            nombre,
            f"Q {precio:.2f}",
            str(cantidad),
            categoria
        ]

        for col, texto in enumerate(datos):
            # Solo borde inferior para simular tabla pegada sin separación extra
            border_style = "solid"
            bd = 1
            relief_style = "flat"

            celda = tk.Label(frame_interno, text=texto, bg=color_tarjeta, fg=color_texto,
                             font=("Calibri", 11), borderwidth=bd, relief=relief_style,
                             padx=8, pady=6)
            celda.grid(row=index, column=col, sticky="nsew")

            # Alternar color filas para mejor lectura
            if index % 2 == 0:
                celda.configure(bg="#faf9fc")

            # Bind corregido, pasa ventana para abrir editor
            celda.bind("<Button-1>", lambda e, pid=producto_id, nom=nombre, pre=precio, cant=cantidad: abrir_editor(ventana, pid, nom, pre, cant))

    for col in range(5):
        frame_interno.grid_columnconfigure(col, weight=1)

    return productos_panel


def crear_panel_buscador(ventana, actualizar_productos_func):
    color_fondo = "#ecebf3"  # fondo lavanda muy claro
    color_etiqueta = "#b9aee0"  # lavanda medio
    color_boton = "#6a5acd"  # morado medio
    color_boton_texto = "#ffffff"
    fuente_label = ("Bauhaus 93",18,"bold")
    fuente_entrada = ("Cascadia Code ExtraLight",15,"bold")
    fuente_boton = ("Broadway",17,"bold")

    panel_buscador = tk.Frame(ventana, bg=color_fondo, highlightbackground="#c4c1d7", highlightthickness=2, bd=0)
    panel_buscador.place(relx=0, rely=0.7, relwidth=0.18, relheight=0.3)

    encabezados_busqueda = ["Nombre", "Precio", "Cantidad", "Categoría"]

    etiqueta_campo = tk.Label(panel_buscador, text="Campo a buscar:", font=fuente_label,
                             bg=color_fondo, fg=color_boton, anchor="w")
    etiqueta_campo.pack(padx=15, pady=(15, 5), anchor="w")

    campo_var = tk.StringVar(panel_buscador)
    campo_var.set(encabezados_busqueda[0])

    combo_campo = ttk.Combobox(panel_buscador, textvariable=campo_var, values=encabezados_busqueda,
                              state="readonly", font=fuente_entrada, height=5)
    combo_campo.pack(padx=15, pady=(0, 15), anchor="w", fill='x')

    etiqueta_texto = tk.Label(panel_buscador, text="Dato del Campo: ", font=fuente_label,
                             bg=color_fondo, fg=color_boton, anchor="w")
    etiqueta_texto.pack(padx=15, pady=(0, 5), anchor="w")

    texto_var = tk.StringVar()
    entry_texto = tk.Entry(panel_buscador, textvariable=texto_var, font=fuente_entrada, relief="flat", bg="#f7f6fb")
    entry_texto.pack(padx=15, pady=(0, 15), anchor="w", fill='x')

    def on_enter(event):
        boton_buscar.invoke()

    combo_campo.bind("<Return>", on_enter)
    combo_campo.bind("<Down>", lambda e: combo_campo.event_generate('<Button-1>'))
    entry_texto.bind("<Return>", on_enter)

    boton_buscar = tk.Button(panel_buscador, text="Buscar", font=fuente_boton,
                             bg=color_boton, fg=color_boton_texto, activebackground="#836fff",
                             bd=0, cursor="hand2", relief="flat",
                             command=lambda: actualizar_productos_func(campo_var.get(), texto_var.get()))
    boton_buscar.pack(padx=15, pady=10, fill='x')

    return panel_buscador
