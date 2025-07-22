# sql.py
import mysql.connector
def conectar(consulta_sql):

# Credenciales para la conexión

    config = {
        'user': 'u0mpxrljxh9li3i2',
        'password': 'ElcAh83krxavLWk44FL4',
        'host': 'bdtfzwhm8vhxrkdbh4k1-mysql.services.clever-cloud.com',
        'database': 'bdtfzwhm8vhxrkdbh4k1',
        'raise_on_warnings': True
                        }

# Conectar a la base de datos
    try:
        conexion = mysql.connector.connect(**config)
        print("Conexión exitosa a la base de datos.")

        # Objeto para crear consultas
        consulta = conexion.cursor()

        # función para agregar la consulta SQL
        consulta.execute(consulta_sql)
        # Almacenamos el resultado de la consulta SLQ
        resultado = consulta.fetchall()

        return resultado

        # Respuesta si al conectar da error
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")

