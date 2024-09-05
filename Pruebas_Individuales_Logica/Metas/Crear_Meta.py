import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mysql.connector import Error
from datetime import datetime
from db_config import obtener_conexion

try:
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        nombre_meta = input("Escriba el nombre de la meta: ").upper()
        cursor.execute("SELECT nombre FROM metas WHERE nombre = %s", (nombre_meta,))
        resultado_nombre_meta = cursor.fetchone()

        if resultado_nombre_meta:
            raise ValueError("Meta ya existente")
        
        descripcion_meta = input("Añada una descripción a la meta (opcional): ")
        valor_meta = int(input("¿Cuánto cuesta su meta? "))
        cuota_fija = int(input("¿Cuál es su cuota fija para la meta? "))

        valor_restante = input("¿Cuánto le falta para completar su meta? (Deje en blanco si es igual al valor total): ")
        
        if valor_restante.strip() == "":  
            valor_restante = valor_meta
        else:
            valor_restante = int(valor_restante)

        fecha_de_creacion = datetime.now().date()

        cursor.execute("""
            INSERT INTO metas (nombre, descripcion, valor_meta, cuota_fija, fecha_de_creacion, valor_restante) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre_meta, descripcion_meta, valor_meta, cuota_fija, fecha_de_creacion, valor_restante))

        conexion.commit()
        print("Meta agregada correctamente.")
    
except Error as e:
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
