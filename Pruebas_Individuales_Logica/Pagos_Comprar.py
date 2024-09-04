from db_config import obtener_conexion
from mysql.connector import Error

try:
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()

        info = input("¿Qué va a comprar? ")
        costo = int(input("¿Cuánto costó? "))
        banco = input("¿De dónde saldrá el dinero? ")

        cursor.execute("SELECT nombre, valor FROM carteras WHERE nombre = %s", (banco))
        registro = cursor.fetchone()

        if registro:
            print(f"Registro obtenido: {registro}")

            nombre, valor_actual = registro

            valor_actual = float(valor_actual)
            print(f"Valor actual en la base de datos: {valor_actual}")

            nuevo_costo = valor_actual - costo
            print(f"Nuevo valor calculado: {nuevo_costo}")

            cursor.execute("""
                UPDATE carteras
                SET valor = %s
                WHERE nombre = %s
            """, (nuevo_costo, banco))

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
