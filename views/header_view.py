import tkinter as tk

def cargar_header(ventana):
    header_panel = tk.Frame(ventana, 
        bg="red", 
        padx=0, 
        pady=0,
        width=1000,
        height=60)
    header_panel.pack()
    print("panel header cargado")