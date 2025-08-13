import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from services.manipular_sql import manipular
from Paneles.productos_view import cargar_productos  # Importa la función para actualizar lista

def agregar_productos(ventana):
    color_fondo = "#ecebf3"  # lavanda clarito
    color_etiqueta = "#b9aee0"  # lavanda medio
    color_boton = "#6a5acd"  # morado medio
    color_boton_texto = "#ffffff"

    fuente_titulo = ("Gill Sans Ultra Bold",19,"bold")
    fuente_label = ("Bauhaus 93",18,"bold")
    fuente_entrada = ("Cascadia Code ExtraLight",14,"bold")
    fuente_boton = ("Broadway",17,"bold")

    panel_izquierdo = tk.Frame(ventana, bg=color_fondo, highlightbackground="#c4c1d7", highlightthickness=1)
    panel_izquierdo.place(relx=0, rely=0, relwidth=0.18, relheight=0.7)

    titulo_izquierdo = tk.Label(panel_izquierdo, text="Fromulario de\n   productos", bg=color_fondo,
                                font=fuente_titulo, fg="#280b6a", anchor="w", justify="left")
    titulo_izquierdo.pack(padx=15, pady=(15, 25), anchor="w")

    categorias = manipular("SELECT id, nombre FROM categorias")
    if not categorias:
        categorias = []
    categorias_dict = {nombre: id for id, nombre in categorias}

    campos = [
        ("Nombra producto:", "producto"),
        ("Coloca el precio:", "precio"),
        ("Cantidad entrante:", "cantidad"),
    ]

    entradas = {}
    errores_entry = {}
    for texto, clave in campos:
        etiqueta = tk.Label(panel_izquierdo, text=texto, font=fuente_label,
                            bg=color_fondo, fg=color_boton, anchor="w")
        etiqueta.pack(padx=15, anchor="w")
        entrada = tk.Entry(panel_izquierdo, font=fuente_entrada, relief="flat", bg="#f7f6fb")
        entrada.pack(padx=15, pady=(0, 6), anchor="w", fill='x')
        error = tk.Label(panel_izquierdo, text="", fg="#d9534f", bg=color_fondo, font=("Arial", 10))
        error.pack(padx=15, anchor="w")
        entradas[clave] = entrada
        errores_entry[clave] = error

    etiqueta_categoria = tk.Label(panel_izquierdo, text="Categoría:", font=fuente_label,
                                  bg=color_fondo, fg=color_boton, anchor="w")
    etiqueta_categoria.pack(padx=15, anchor="w")

    categoria_var = tk.StringVar(panel_izquierdo)
    lista_categorias = ["Seleccionar"] + [nombre for _, nombre in categorias]
    categoria_var.set(lista_categorias[0])

    combo_categoria = ttk.Combobox(panel_izquierdo, textvariable=categoria_var, values=lista_categorias,
                                   state="readonly", font=fuente_entrada)
    combo_categoria.current(0)
    combo_categoria.pack(padx=15, pady=(0, 8), anchor="w", fill='x')

    error_categoria = tk.Label(panel_izquierdo, text="", fg="#d9534f", bg=color_fondo, font=("Arial", 10))
    error_categoria.pack(padx=15, anchor="w")

    def avanzar(event, clave_actual):
        claves = list(entradas.keys()) + ["categoria"]
        idx = claves.index(clave_actual)
        if idx < len(claves) - 1:
            siguiente = claves[idx + 1]
            if siguiente == "categoria":
                combo_categoria.focus_set()
            else:
                entradas[siguiente].focus_set()
        else:
            boton_continuar.invoke()

    for clave in entradas:
        entradas[clave].bind("<Return>", lambda e, c=clave: avanzar(e, c))

    combo_categoria.bind("<Return>", lambda e: boton_continuar.invoke())
    combo_categoria.bind("<Down>", lambda e: combo_categoria.event_generate('<Button-1>'))

    def insertar_producto():
        campos_validos = True

        for clave, entrada in entradas.items():
            if not entrada.get().strip():
                errores_entry[clave].config(text=f"❌ No se escribió nada en {clave}")
                campos_validos = False
            else:
                errores_entry[clave].config(text="")

        categoria_nombre = categoria_var.get()
        if categoria_nombre == "Seleccionar":
            error_categoria.config(text="❌ No se seleccionó una categoría")
            campos_validos = False
        else:
            error_categoria.config(text="")

        if not campos_validos:
            return

        try:
            nombre = entradas["producto"].get()
            precio = float(entradas["precio"].get())
            cantidad = int(entradas["cantidad"].get())
            categoria_id = categorias_dict.get(categoria_nombre)
        except ValueError:
            print("❌ Precio y cantidad deben ser números válidos.")
            return

        sql = """INSERT INTO productos (nombre, precio, cantidad, categoria_id)
                 VALUES (%s, %s, %s, %s)"""
        parametros = (nombre, precio, cantidad, categoria_id)
        filas = manipular(sql, parametros)

        if filas == 1:
            print("✅ Producto insertado correctamente.")
            for entrada in entradas.values():
                entrada.delete(0, tk.END)
            for error in errores_entry.values():
                error.config(text="")
            if categorias:
                categoria_var.set("Selecciona una categoría")
            cargar_productos(ventana)
        else:
            print("❌ Error al insertar producto.")

    boton_continuar = tk.Button(panel_izquierdo, text="Agregar", font=fuente_boton,
                                bg=color_boton, fg=color_boton_texto, activebackground="#836fff",
                                bd=0, cursor="hand2", relief="flat", command=insertar_producto)
    boton_continuar.pack(pady=15, fill='x', padx=15)
