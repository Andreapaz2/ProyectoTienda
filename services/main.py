# main.py
import tkinter as tk
from login_view import cargar_login

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("1000x540")  # Tamaño de la ventana para que coincida con login_panel
ventana.title("Login App")

# Cargar el panel de login
cargar_login(ventana)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
