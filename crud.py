import mysql.connector

# Configuración de la conexión a la base de datos
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'chatbot_db',  # Nombre de la base de datos
    'raise_on_warnings': True
}

# Conectar a la base de datos
conn = mysql.connector.connect(**config)

# Crear un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Función para crear un nuevo usuario
def crear_usuario(nombre, email, contraseña):
    try:
        sql = "INSERT INTO usuarios (nombre, email, contraseña) VALUES (%s, %s, %s)"
        val = (nombre, email, contraseña)
        cursor.execute(sql, val)
        conn.commit()
        print("Usuario creado exitosamente.")
    except Exception as e:
        print(f"Error al crear el usuario: {str(e)}")
        conn.rollback()

# Función para obtener todos los usuarios
def obtener_usuarios():
    try:
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios: {str(e)}")

# Función para consultar un usuario por su ID
def consultar_usuario_por_id(usuario_id):
    try:
        sql = "SELECT * FROM usuarios WHERE id = %s"
        val = (usuario_id,)
        cursor.execute(sql, val)
        usuario = cursor.fetchone()
        return usuario
    except Exception as e:
        print(f"Error al consultar el usuario por ID: {str(e)}")


# Función para actualizar la contraseña, nombre y correo electrónico de un usuario
def actualizar_usuario(usuario_id, nuevo_nombre, nueva_contraseña, nuevo_correo):
    try:
        sql = "UPDATE usuarios SET nombre = %s, contraseña = %s, email = %s WHERE id = %s"
        val = (nuevo_nombre, nueva_contraseña, nuevo_correo, usuario_id)
        cursor.execute(sql, val)
        conn.commit()
        print("Información de usuario actualizada exitosamente.")
        return True
    except Exception as e:
        print(f"Error al actualizar la información del usuario: {str(e)}")
        conn.rollback()
        return False

# Función para eliminar un usuario por ID
def eliminar_usuario(usuario_id):
    try:
        sql = "DELETE FROM usuarios WHERE id = %s"
        val = (usuario_id,)
        cursor.execute(sql, val)
        conn.commit()
        print("Usuario eliminado exitosamente.")
    except Exception as e:
        print(f"Error al eliminar el usuario: {str(e)}")
        conn.rollback()
        
# # Función para guardar una conversación en la tabla historial_chat
# def guardar_conversacion(usuario_id, mensaje, respuesta_chatbot):
#     try:
#         # Crear la sentencia SQL para la inserción
#         sql = "INSERT INTO historial_chat (usuario_id, mensaje, respuesta_chatbot) VALUES (%s, %s, %s)"
#         val = (usuario_id, mensaje, respuesta_chatbot)

#         # Ejecutar la sentencia SQL
#         cursor.execute(sql, val)

#         # Confirmar la transacción
#         conn.commit()

#         print("Conversación guardada exitosamente en el historial_chat.")
#     except Exception as e:
#         print(f"Error al guardar la conversación: {str(e)}")
#         conn.rollback()