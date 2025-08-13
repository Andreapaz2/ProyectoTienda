import mysql.connector

def conectar(consulta_sql, parametros=None):
    # Credenciales para la conexión
    config = {
        'user': 'unw0a3mplphyntvt',
        'password': 'gg29e8tWark4pZdtWAky',
        'host': 'bzkjatoeuklsc30l3wda-mysql.services.clever-cloud.com',
        'database': 'bzkjatoeuklsc30l3wda',
        'raise_on_warnings': True
    }

    try:
        conexion = mysql.connector.connect(**config)
        print("✅ Conexión exitosa a la base de datos.")

        consulta = conexion.cursor()
        if parametros:
            consulta.execute(consulta_sql, parametros)
        else:
            consulta.execute(consulta_sql)
        resultado = consulta.fetchall()

        conexion.close()
        return resultado

    except mysql.connector.Error as err:
        print(f"❌ Error al conectar a la base de datos: {err}")
        return []  # Retorna lista vacía para evitar errores
