from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_config import obtener_conexion
from mysql.connector import Error

try:
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        banco = input("A que banco le va a sumar dinero? ").upper()
        cursor.execute("SELECT nombre, valor FROM carteras WHERE nombre = %s", (banco,))
        resultado_banco = cursor.fetchone()

        if not resultado_banco:
            raise ValueError("El banco no existe")

        sumar_a_cartera = int(input("Cuanto va a sumar a cartera? "))

        nombre_banco, valor_actual = resultado_banco

        nuevo_valor = valor_actual + sumar_a_cartera

        cursor.execute("UPDATE carteras SET valor = %s WHERE nombre = %s", (nuevo_valor, banco))
        conexion.commit()

        print(f"Al valor de la cartera {valor_actual} se le sumo {sumar_a_cartera}")
        print(f"El nuevo valor es {nuevo_valor}")

        fecha_de_creacion = datetime.now().date()

        cursor.execute("INSERT INTO Extractos (nombre, descripcion, banco_salida, banco_entrada, fecha_de_creacion)" 
                       "Values ('ENTRADA DINERO', 'entrada de dinero a alguna cartera', %s, %s, %s)", (banco, sumar_a_cartera, fecha_de_creacion))
        conexion.commit()

except Error as e:  
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")