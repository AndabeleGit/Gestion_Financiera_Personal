import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_config import obtener_conexion
from mysql.connector import Error

try:
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        nueva_cartera = input("Nombre de su nueva cartera: ").upper()
        dinero_en_cartera = int(input("Cuánto dinero tiene en su cartera? "))

        cursor.execute("SELECT nombre FROM carteras WHERE nombre = %s", (nueva_cartera,))
        resultado = cursor.fetchone()

        if resultado:
            raise ValueError("Cartera ya existente. Por favor, elige un nombre diferente.")
        else:
            cursor.execute("INSERT INTO carteras (nombre, valor) VALUES(%s, %s)", (nueva_cartera, dinero_en_cartera))
            conexion.commit()
            print("Cartera agregada correctamente.")
            
except Error as e:
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
