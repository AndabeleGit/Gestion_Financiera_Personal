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

        nombre_meta = input("Que meta va a pagar? ").upper()
        cursor.execute("SELECT nombre, cuota_fija, valor_restante FROM metas Where nombre = %s", (nombre_meta,))
        resultado_meta = cursor.fetchone()
        if not resultado_meta:
            raise ValueError("La meta no existe, verifique el nombre")
        
        nombre_meta_db, cuota_fija, valor_restante = resultado_meta

        cuota = input("Va a pagar la cuota fija (f) o una cuota variable (v)? (f/v)").lower()

        if cuota == "f":
            nuevo_valor_restante = valor_restante - cuota_fija
            cursor.execute("UPDATE metas SET valor_restante = %s WHERE nombre = %s", (nuevo_valor_restante, nombre_meta))
            conexion.commit()
            print(f"Pago realizado de cuota fija ({cuota_fija}) a la meta {nombre_meta}, nueva valor restante: {nuevo_valor_restante}")
        elif cuota == "v":
            cuota_variable = int(input("Cuanto dinero va a pagar para la meta? "))
            nuevo_valor_restante = valor_restante - cuota_variable
            cursor.execute("UPDATE metas SET valor_restante = %s WHERE nombre = %s", (nuevo_valor_restante, nombre_meta))
            conexion.commit()
            print(f"Pago realizado de cuota variable ({cuota_variable}) a la meta {nombre_meta}, nueva valor restante: {nuevo_valor_restante}")
        else:
            print("Opcion no valida, seleccione v/f")

except Error as e:
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")