import tkinter as tk 
def cargar_productos(ventana):
    productos_panel = tk.Frame(
        ventana,
        bg="green", 
        padx=0, 
        pady=0,
        width=1000,
        height=540)
    productos_panel.pack()
    print("panel productos cargado")