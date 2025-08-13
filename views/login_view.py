import tkinter as tk
from services.my_sql import conectar
from views.dashboard import ventana_productos


def cargar_login(ventana):
    # Fondo degradado simulado
    ventana.config(bg="#4b3f72",)

    # Panel principal centrado con bordes redondeados
    login_panel = tk.Frame(
        ventana,
        bg="white",
        bd=2,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#d1d9e6"
    )
    login_panel.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)

    # Título
    titulo = tk.Label(
        login_panel,
        text="🔐 Inicio de Sesión",
        font=("Bauhaus 93", 25, "bold"),
        bg="white",
        fg="#4b3f72"
    )
    titulo.pack(pady=(20, 15))

    # Etiqueta y entrada correo
    tk.Label(login_panel, text="Correo electrónico:", font=("Gill Sans Ultra Bold", 14),fg="#4b3f72", bg="white", anchor="w").pack(fill="x", padx=40)
    entrada_correo = tk.Entry(login_panel, font=("Cascadia Code ExtraLight", 12), width=30, bd=1, relief="solid")
    entrada_correo.pack(pady=(0, 15))

    # Etiqueta y entrada contraseña
    entrada_correo.bind("<Return>", lambda event: entrada_contrasenha.focus_set())
    tk.Label(login_panel, text="Contraseña:", font=("Gill Sans Ultra Bold", 14),fg="#4b3f72", bg="white", anchor="w").pack(fill="x", padx=40)
    entrada_contrasenha = tk.Entry(login_panel, font=("Cascadia Code ExtraLight", 12), width=30, show="*", bd=1, relief="solid")
    entrada_contrasenha.pack(pady=(0, 20))

    # Función botón
    def funcion_boton():
        usuario_login = entrada_correo.get()
        contrasenha_login = entrada_contrasenha.get()
        consultar_usuario = conectar(
            f"SELECT * FROM usuarios WHERE correo = '{usuario_login}' AND contrasenna = '{contrasenha_login}'"
        )
        if len(consultar_usuario) != 0:
            print("Usuario Activo")
            ventana.destroy()
            ventana_productos(consultar_usuario)
        else:
            tk.Label(login_panel, text="❌ Datos incorrectos", fg="red", bg="white", font=("Arial", 10, "bold")).pack()

    # Botón iniciar sesión
    boton = tk.Button(
        login_panel,
        text="Iniciar Sesión",
        command=funcion_boton,
        font=("Broadway", 14, "bold"),
        bg="#4b3f72",
        fg="white",
        activebackground="#280b6a",
        activeforeground="white",
        relief="flat",
        width=20,
        height=2,
        cursor="hand2"
    )
    boton.pack()

    entrada_contrasenha.bind("<Return>", lambda event: funcion_boton())

    print("Panel login cargado")
