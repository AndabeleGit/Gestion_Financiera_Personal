import sys
import os
from mysql.connector import Error

# Asegura que el archivo de configuración de la base de datos esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_config import obtener_conexion

try:
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        cursor.execute("SELECT id, nombre, descripcion, valor_meta, cuota_fija FROM metas")
        metas = cursor.fetchall()

        if metas:
            print("Metas disponibles:")
            for meta in metas:
                print(f"ID: {meta[0]}, Nombre: {meta[1]}, Descripción: {meta[2]}, Valor Meta: {meta[3]}, Cuota Fija: {meta[4]}")
            
            meta_id = input("Ingrese el ID de la meta que desea editar: ")

            cursor.execute("SELECT id, nombre, descripcion, valor_meta, cuota_fija FROM metas WHERE id = %s", (meta_id,))
            meta_seleccionada = cursor.fetchone()

            if meta_seleccionada:
                print(f"Has seleccionado la meta con la siguiente información: \n"
                      f"Id: {meta_seleccionada[0]} \n"
                      f"Nombre: {meta_seleccionada[1]} \n"
                      f"Descripción: {meta_seleccionada[2]} \n"
                      f"Valor de la meta: {meta_seleccionada[3]} \n"
                      f"Cuota Fija: {meta_seleccionada[4]} \n")
                
                campo_a_editar = input("¿Qué desea editar, Nombre (n), Descripción (d), Valor de la meta (v), Cuota fija (c): ").lower()

                if campo_a_editar == 'n':
                    nuevo_nombre = input("Ingrese el nuevo nombre de la meta: ").upper()
                    cursor.execute("UPDATE metas SET nombre = %s WHERE id = %s", (nuevo_nombre, meta_id))
                    conexion.commit()
                    print(f"El nombre de la meta ha sido actualizado a {nuevo_nombre}")

                elif campo_a_editar == 'd':
                    nuevo_valor = input("Ingrese la nueva descripción de la meta: ")
                    cursor.execute("UPDATE metas SET descripcion = %s WHERE id = %s", (nuevo_valor, meta_id))
                    conexion.commit()
                    print(f"La descripción de la meta ha sido actualizada a {nuevo_valor}")

                elif campo_a_editar == 'v':
                    try:
                        nuevo_valor = float(input("Ingrese el nuevo valor de la meta: "))
                        cursor.execute("UPDATE metas SET valor_meta = %s WHERE id = %s", (nuevo_valor, meta_id))
                        conexion.commit()
                        print(f"El valor de la meta ha sido actualizado a {nuevo_valor}")
                    except ValueError:
                        print("Advertencia: El valor ingresado no es un número válido.")

                elif campo_a_editar == 'c':
                    try:
                        nuevo_valor = float(input("Ingrese la nueva cuota fija de la meta: "))
                        cursor.execute("UPDATE metas SET cuota_fija = %s WHERE id = %s", (nuevo_valor, meta_id))
                        conexion.commit()
                        print(f"La cuota fija de la meta ha sido actualizada a {nuevo_valor}")
                    except ValueError:
                        print("Advertencia: El valor ingresado no es un número válido.")
                else:
                    print("Opción no válida.")
            else:
                print("No existe una meta con ese ID.")
        else:
            print("No hay metas disponibles para editar.")

except Error as e:
    print(f"Error en la base de datos: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
