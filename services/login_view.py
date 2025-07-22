import tkinter as tk
from services.my_sql import conectar

def cargar_login(ventana):
    login_panel = tk.Frame(
        ventana,
        bg = "grey",
        padx = 0,
        pady = 0,
        width = 1000,
        height = 540,
        )
    
# Formulario
    titulo = tk.Label(login_panel, text="Login")
    titulo.pack() 

# Correo
    correo = tk.Label(login_panel, text="Correo")
    correo.pack()

# Entrada correo# Correo
    entrada_correo = tk.Entry(login_panel)
    entrada_correo.pack()

#Contraseña
    contraseña = tk.Label(login_panel, text="Contraseña")
    contraseña.pack()

# Entrada contraseña
    entrada_contraseña = tk.Entry(login_panel)
    entrada_contraseña.pack()

# Botón ingresar

    def funcion_boton():
        correo = entrada_correo.get()
        datocontraseña = entrada_contraseña.get()
        consultar_usuario = conectar(f"SELECT * FROM usuario WHERE correo = '{correo}' AND contrasena = '{datocontraseña}'")

        if len(consultar_usuario) != 0:
            print("Usuario activo")
        else:
            print("Datos incorrectos") 
    


    boton = tk.Button(login_panel, text="Continuar", command=funcion_boton)
    boton.pack()


    login_panel.pack()
    print("panel login cargado")
    return login_panel

