import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_config import obtener_conexion
from mysql.connector import Error

try:
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        meta_a_borrar = input("Que meta va a eliminar? ")

        cursor.execute("SELECT nombre FROM metas WHERE nombre = %s", (meta_a_borrar,))
        resultado = cursor.fetchone()

        if not resultado:
            raise ValueError("Meta no existente. Por favor, verifica el nombre.")

        confirmacion = input("¿Seguro quieres borrar la meta? (y/n): ")

        if confirmacion.lower() == "y":
            cursor.execute("DELETE FROM metas WHERE nombre = %s", (meta_a_borrar,))
            conexion.commit()
            print("Meta borrada correctamente.")
        else: 
            print("No se modificó la tabla.")
            
except Error as e:
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
