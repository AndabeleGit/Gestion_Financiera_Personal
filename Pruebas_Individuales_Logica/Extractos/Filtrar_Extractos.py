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

        opcion = input("Desea hacer algún tipo de filtro? Estas son las opciones:\n"
                       "Filtrar por Nombre (n)\n"
                       "Filtrar por Descripción (d)\n"
                       "Filtrar por Banco (b)\n"
                       "Filtrar por Fecha de Creación (f)\n").strip().lower()
        
        if opcion == "n":
            nombre_a_buscar = input("¿Qué nombre busca? ").strip().upper()
            cursor.execute("SELECT * FROM Extractos WHERE nombre = %s", (nombre_a_buscar,))
        
        elif opcion == "d":
            descripcion_a_buscar = input("¿Qué descripción busca? ").strip().upper()
            cursor.execute("SELECT * FROM Extractos WHERE descripcion = %s", (descripcion_a_buscar,))
        
        elif opcion == "b":
            banco_a_buscar = input("¿Qué banco busca? ").strip().upper()
            cursor.execute("SELECT * FROM Extractos WHERE salida_dinero = %s", (banco_a_buscar,))
        
        elif opcion == "f":
            fecha_a_buscar = input("¿Qué fecha busca? (formato YYYY-MM-DD) ").strip()
            try:
                datetime.strptime(fecha_a_buscar, '%Y-%m-%d')
                cursor.execute("SELECT * FROM Extractos WHERE fecha_de_creacion = %s", (fecha_a_buscar,))
            except ValueError:
                print("Formato de fecha inválido. Use el formato YYYY-MM-DD.")
                sys.exit(1)

        else:
            print("Opción de filtro no válida")
            sys.exit(1)

        resultados = cursor.fetchall()
        if resultados:
            for fila in resultados:
                print(fila)
        else:
            print("No se encontraron resultados.")

except Error as e:
    print(f"Error en la conexión: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
