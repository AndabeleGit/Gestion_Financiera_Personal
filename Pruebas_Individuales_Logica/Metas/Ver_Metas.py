import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from db_config import obtener_conexion
from mysql.connector import Error

try:
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM metas")
        resultado_visualizacion_metas = cursor.fetchall()  

        for meta in resultado_visualizacion_metas:
            meta_formateada = []
            for dato in meta:
                if isinstance(dato, datetime):
                    dato = dato.strftime("%d-%m-%Y")
                else:
                    dato = str(dato)
                meta_formateada.append(dato)
            
            print(" | ".join(meta_formateada))  

except Error as e:
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
