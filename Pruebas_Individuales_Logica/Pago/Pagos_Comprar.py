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

        info = input("¿Qué va a comprar? ").upper()
        costo = float(input("¿Cuánto costó? "))
        banco = input("¿De dónde saldrá el dinero? ").upper()

        cursor.execute("SELECT nombre, valor FROM carteras WHERE nombre = %s", (banco,))
        registro = cursor.fetchone()

        if registro:
            print(f"Registro obtenido: {registro}")

            valor_actual = registro[1]

            valor_actual = float(valor_actual)
            print(f"Valor actual en la base de datos: {valor_actual}")

            if costo > valor_actual:
                print("Error: No hay suficiente saldo en el banco para realizar esta compra.")
            else:
                nuevo_valor = valor_actual - costo
                print(f"Nuevo valor calculado: {nuevo_valor}")

                cursor.execute("UPDATE carteras SET valor = %s WHERE nombre = %s", (nuevo_valor, banco))
                conexion.commit()

                fecha_de_creacion = datetime.now().date()

                cursor.execute(
                    "INSERT INTO Extractos (nombre, descripcion, salida_dinero, valor_movido, fecha_de_creacion) "
                    "VALUES (%s, 'Compra', %s, %s, %s)",(info, banco, costo, fecha_de_creacion))
                conexion.commit()

                print("El valor ha sido actualizado correctamente.")
        else:
            print("No se encontró ningún registro con el banco proporcionado.")
except Error as e:
    print(f"Error: {e}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
