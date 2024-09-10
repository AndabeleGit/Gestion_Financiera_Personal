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

        sale_banco = input("¿De qué banco saldrá el dinero? ").upper()
        llega_banco = input("¿A qué banco llegará el dinero? ").upper()
        dinero_a_mover = int(input("¿Cuánto dinero va a mover? "))

        cursor.execute("SELECT nombre, valor FROM carteras WHERE nombre = %s", (sale_banco,))
        registro_1 = cursor.fetchone()

        cursor.execute("SELECT nombre, valor FROM carteras WHERE nombre = %s", (llega_banco,))
        registro_2 = cursor.fetchone()

        if not registro_1:
            raise ValueError(f"El banco '{sale_banco}' no existe. Por favor, verifica el nombre.")
        
        if not registro_2:
            raise ValueError(f"El banco '{llega_banco}' no existe. Por favor, verifica el nombre.")

        valor_sale_banco = registro_1[1]
        valor_llega_banco = registro_2[1]

        if dinero_a_mover > valor_sale_banco:
            raise ValueError(f"El banco '{sale_banco}' no tiene suficiente dinero para mover {dinero_a_mover}.")

        nuevo_valor_sale_banco = valor_sale_banco - dinero_a_mover
        nuevo_valor_llega_banco = valor_llega_banco + dinero_a_mover

        cursor.execute("UPDATE carteras SET valor = %s WHERE nombre = %s", (nuevo_valor_sale_banco, sale_banco))
        cursor.execute("UPDATE carteras SET valor = %s WHERE nombre = %s", (nuevo_valor_llega_banco, llega_banco))
        
        conexion.commit()

        fecha_de_creacion = datetime.now().date()

        cursor.execute("INSERT INTO Extractos (nombre, descripcion, salida_dinero, entrada_dinero, valor_movido, fecha_de_creacion) "
                       "VALUES ('MOVIMIENTO ENTRE CUENTAS', 'moviento entre cuentas', %s, %s, %s, %s)", (sale_banco, llega_banco, dinero_a_mover, fecha_de_creacion))
        
        conexion.commit()

        print(f"Transferencia realizada: {dinero_a_mover} ha sido movido de '{sale_banco}' a '{llega_banco}'.")
        print(f"Nuevo saldo de '{sale_banco}': {nuevo_valor_sale_banco}")
        print(f"Nuevo saldo de '{llega_banco}': {nuevo_valor_llega_banco}")
        
except Error as e:
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
