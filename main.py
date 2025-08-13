import tkinter as tk 
from Paneles.header_view import cargar_header
from Paneles.productos_view import cargar_productos
from views.login_view import *
from views.login_view import cargar_login
from views.dashboard import *

ventana = tk.Tk()
ventana.title("Mi tienda")
ventana.geometry("500x500")

cargar_login(ventana)


ventana. mainloop()
#USUARIO para puruebas :  carlos.martinez@email.com | clave123  

