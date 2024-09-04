
from db_config import obtener_conexion
from mysql.connector import Error

try:
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        cartera_a_borrar = input("Que cartera va a eliminar? ")

        cursor.execute("SELECT nombre FROM carteras WHERE nombre = %s", (cartera_a_borrar,))
        resultado = cursor.fetchone()

        if not resultado:
            raise ValueError("Cartera no existe. Por favor, verifica el nombre.")

        confirmacion = input("¿Seguro quieres borrar la cartera? (y/n): ")

        if confirmacion.lower() == "y":
            cursor.execute("DELETE FROM carteras WHERE nombre = %s", (cartera_a_borrar,))
            conexion.commit()
            print("Cartera borrada correctamente.")
        else: 
            print("No se modificó la tabla.")
            
except Error as e:
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Advertencia: {ve}")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")
