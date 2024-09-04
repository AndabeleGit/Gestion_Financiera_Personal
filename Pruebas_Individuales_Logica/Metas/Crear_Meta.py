from db_config import obtener_conexion
from mysql.connector import Error
from datetime import datetime

try:
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        nombre_meta = input("Escriba el nombre de la meta ").upper()
        cursor.execute("SELECT nombre FROM metas WHERE nombre = %s", (nombre_meta,))
        resultado_nombre_meta = cursor.fetchone()
        if resultado_nombre_meta:
            raise ValueError("Meta ya existente")
        
        descripcion_meta = input("Añada una descripcion a la meta (opcional) ")

        valor_meta = int(input("Cuanto cuesta su meta? "))

        cuota_fija = int(input("Cual es su cuota fija para su meta? "))

        fecha_de_creacion = datetime.now()
        fecha_de_creacion_modificada = fecha_de_creacion.date()
        
        cursor.execute("INSERT INTO metas (nombre, descripcion, valor_meta, cuota_fija, fecha_de_creacion) VALUES(%s, %s, %s, %s, %s)", 
                       (nombre_meta, descripcion_meta, valor_meta, cuota_fija, fecha_de_creacion_modificada))
        
        conexion.commit()

        print("meta agregada correctamente.")
            
except Error as e:
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
