import tkinter as tk
from Paneles.productos_view import cargar_productos, crear_panel_buscador
from Paneles.agregar_prod import agregar_productos

def ventana_productos(datos):
    venta_usuario = tk.Tk()
    venta_usuario.title("Ventana Usuario")
    venta_usuario.state('zoomed')  # Maximiza ventana (Windows)

    # Panel superior con botón de actualización general
    panel_superior = tk.Frame(venta_usuario, bg="#e0e0e0")
    panel_superior.place(relx=0, rely=0, relwidth=1, relheight=0.05)

    def actualizar_ventana():
        # Eliminar todos los paneles menos panel_superior
        for widget in venta_usuario.winfo_children():
            if widget != panel_superior:
                widget.destroy()
        # Crear buscador y pasar función para filtrar productos
        crear_panel_buscador(venta_usuario, lambda campo, texto: cargar_productos(venta_usuario, campo, texto))
        # Cargar lista productos sin filtro
        cargar_productos(venta_usuario)
        # Cargar formulario agregar productos
        agregar_productos(venta_usuario)

    boton_actualizar = tk.Button(
        panel_superior,
        text="Actualizar ventana",
        command=actualizar_ventana,
        bg="#2196F3",
        fg="white",
        font=("Segoe UI", 10, "bold")
    )
    boton_actualizar.pack(padx=10, pady=5, side="left")

    # Crear buscador al iniciar la ventana
    crear_panel_buscador(venta_usuario, lambda campo, texto: cargar_productos(venta_usuario, campo, texto))

    # Cargar productos (lista) sin filtro al inicio
    cargar_productos(venta_usuario)

    # Cargar panel de agregar productos (abajo del buscador)
    agregar_productos(venta_usuario)

    venta_usuario.mainloop()
