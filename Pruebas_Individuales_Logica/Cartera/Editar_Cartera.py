import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_config import obtener_conexion
from mysql.connector import Error

try:
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        cursor.execute("SELECT id, nombre, valor FROM carteras")
        carteras = cursor.fetchall()

        if carteras:
            print("Carteras disponibles:")
            for cartera in carteras:
                print(f"ID: {cartera[0]}, Nombre: {cartera[1]}, Valor: {cartera[2]}")
            
            cartera_id = input("Ingrese el ID de la cartera que desea editar: ")

            cursor.execute("SELECT nombre, valor FROM carteras WHERE id = %s", (cartera_id,))
            cartera_seleccionada = cursor.fetchone()

            if cartera_seleccionada:
                print(f"Has seleccionado la cartera: {cartera_seleccionada[0]} con un valor de {cartera_seleccionada[1]}")
                
                campo_a_editar = input("¿Qué desea editar, el nombre (n) o el valor (v)? ").lower()

                if campo_a_editar == 'n':
                    nuevo_nombre = input("Ingrese el nuevo nombre de la cartera: ").upper()
                    cursor.execute("UPDATE carteras SET nombre = %s WHERE id = %s", (nuevo_nombre, cartera_id))
                    conexion.commit()
                    print(f"El nombre de la cartera ha sido actualizado a {nuevo_nombre}")

                elif campo_a_editar == 'v':
                    nuevo_valor = float(input("Ingrese el nuevo valor de la cartera: "))
                    cursor.execute("UPDATE carteras SET valor = %s WHERE id = %s", (nuevo_valor, cartera_id))
                    conexion.commit()
                    print(f"El valor de la cartera ha sido actualizado a {nuevo_valor}")
                else:
                    print("Opción no válida.")
            else:
                print("No existe una cartera con ese ID.")
        else:
            print("No hay carteras disponibles para editar.")

except Error as e:
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
