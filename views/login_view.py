import tkinter as tk 
from services.my_sql import conectar

def cargar_login(ventana):
    login_panel = tk.Frame(
        ventana,
        bg="green",
        padx=0,
        pady=0,
        width=1000,
        height=600
        )
    
    titulo = tk.Label(login_panel, text="Login")
    titulo.pack()
    
    txt_correo = tk.Label(login_panel, text="Correo")
    txt_correo.pack()

    entrada_correo = tk.Entry(login_panel)
    entrada_correo.pack()

    txt_correo = tk.Label(login_panel, text="Contraseña")
    txt_correo.pack()

    entrada_contrasenha = tk.Entry(login_panel)
    entrada_contrasenha.pack()


    def funcion_boton():
        usuario_login = entrada_correo.get()
        contrasenha_login = entrada_contrasenha.get()
        print("Usuario: ",usuario_login)
        print("Contraseña: ", contrasenha_login)
        print(conectar("SHOW TABLES"))


    boton = tk.Button(login_panel, text = "Continuar",command=funcion_boton)
    boton.pack()


    login_panel.pack()
    print("Panel login cargado") 
