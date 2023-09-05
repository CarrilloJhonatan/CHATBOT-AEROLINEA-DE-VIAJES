import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from GUI_AEROLINEA_MOD_ui import Ui_MainWindow
from crud import obtener_usuarios, crear_usuario, actualizar_usuario, eliminar_usuario, consultar_usuario_por_id
from chatbot import obtener_respuesta_del_chatbot  # Importa la función desde chatbot.py

class Vista(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conectar los botones a las páginas correspondientes
        self.ui.bt_consultar.clicked.connect(self.show_page_base_datos)
        self.ui.bt_registrar.clicked.connect(self.show_page_registrar)
        self.ui.bt_actualizar.clicked.connect(self.show_page_actualizar)
        self.ui.bt_elimanas.clicked.connect(self.show_page_eliminar)
        self.ui.bt_chat.clicked.connect(self.show_page_chat)

        # Conectar el botón de búsqueda y la entrada de texto para buscar
        self.ui.bt_buscar.clicked.connect(self.buscar_usuario_por_id)
        self.ui.linefiltrarcodigo.textChanged.connect(self.buscar_usuario_por_id)

        # Conectar el botón de registro
        self.ui.bt_icono_enviar.clicked.connect(self.registrar_usuario)

        # Conectar el botón de actualización
        self.ui.bt_actualizar_2.clicked.connect(self.actualizar_usuario)

        # Conectar el botón de eliminación
        self.ui.bt_eliminar.clicked.connect(self.eliminar_usuario)

        # Conectar el botón de envío de mensaje en la página de chat
        self.ui.bt_enviarmensaje.clicked.connect(self.enviar_mensaje_al_chatbot)

        # Inicializar la variable para mantener la conversación
        self.conversacion = []

        # Mostrar la página de la base de datos al inicio
        self.show_page_base_datos()

    def show_page_base_datos(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_base_datos)

        # Al hacer clic en el botón, llena la tabla con datos de la base de datos
        self.obtener_y_mostrar_usuarios()

    def obtener_y_mostrar_usuarios(self, id_usuario=None):
        # Llamar a la función obtener_usuarios desde crud.py
        if id_usuario:
            usuarios = [consultar_usuario_por_id(id_usuario)]
        else:
            usuarios = obtener_usuarios()

        # Limpiar la tabla antes de agregar nuevos datos
        self.ui.table_usuarios.setRowCount(0)

        # Configurar las columnas de la tabla
        self.ui.table_usuarios.setColumnCount(5)  # Ajustar el número de columnas según tu tabla
        column_headers = ["CODIGO", "USUARIO", "EMAIL", "CONTRASEÑA", "FECHA"]  # Nombres de las columnas
        self.ui.table_usuarios.setHorizontalHeaderLabels(column_headers)

        # Llenar la tabla con los datos de 'usuarios'
        for row, usuario in enumerate(usuarios):
            self.ui.table_usuarios.insertRow(row)
            for col, dato in enumerate(usuario):
                self.ui.table_usuarios.setItem(row, col, QTableWidgetItem(str(dato)))

    def show_page_registrar(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_registrar)

    def show_page_actualizar(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_actualizar)

    def show_page_eliminar(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_eliminar)

    def show_page_chat(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_chat)

        # Limpiar el contenido actual del QTextBrowser
        self.ui.textChat.clear()

    def buscar_usuario_por_id(self):
        # Obtener el ID de usuario a buscar
        id_usuario = self.ui.linefiltrarcodigo.text()

        # Verificar si el campo de búsqueda está vacío
        if not id_usuario:
            # Si está vacío, mostrar todos los usuarios
            self.obtener_y_mostrar_usuarios()
        else:
            # Si no está vacío, realizar la búsqueda en la base de datos
            usuario = consultar_usuario_por_id(id_usuario)

            if usuario:
                # Si se encontró un usuario, llenar la tabla con los datos
                self.obtener_y_mostrar_usuarios(id_usuario)
            else:
                # Si no se encuentra información, mostrar una alerta
                self.mostrar_mensaje("No se encontró información para el ID especificado.", "Información no encontrada")

    def mostrar_mensaje(self, mensaje, titulo):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.exec()

    def registrar_usuario(self):
        # Obtener los valores de los campos de entrada
        nombre = self.ui.lineEdit_nombre.text()
        contrasena = self.ui.lineEdit_contrasena_2.text()
        correo = self.ui.lineEdit_correo.text()

        # Llamar a la función crear_usuario desde crud.py para registrar al usuario
        if nombre and contrasena and correo:
            # Verificar que los campos no estén vacíos
            crear_usuario(nombre, contrasena, correo)  # Llamar a la función crear_usuario
            self.mostrar_mensaje("Usuario registrado exitosamente.", "Registro Exitoso")

            # Restablecer los valores de los campos de entrada a vacíos
            self.ui.lineEdit_nombre.setText("")
            self.ui.lineEdit_contrasena_2.setText("")
            self.ui.lineEdit_correo.setText("")
        else:
            self.mostrar_mensaje("Por favor, complete todos los campos.", "Campos Incompletos")

    def actualizar_usuario(self):
        # Obtener los valores de los campos de entrada
        codigo_usuario = self.ui.lineEdit_codigousuario.text()
        nombre = self.ui.lineEdit_nombre_2.text()
        contrasena = self.ui.lineEdit_contrasena.text()
        email = self.ui.lineEdit_email.text()

        # Verificar si el campo de código de usuario está vacío
        if not codigo_usuario:
            self.mostrar_mensaje("Por favor, ingrese el ID del usuario a actualizar.", "Campo Vacío")
            return

        # Llamar a la función consultar_usuario_por_id desde crud.py para verificar si el usuario existe
        usuario_existente = consultar_usuario_por_id(codigo_usuario)

        if not usuario_existente:
            self.mostrar_mensaje("El usuario con el ID especificado no existe.", "Usuario No Encontrado")
            return

        # Verificar que los campos de nombre, contraseña y correo no estén vacíos
        if nombre and contrasena and email:
            # Llamar a la función actualizar_usuario desde crud.py para actualizar la información del usuario
            exito = actualizar_usuario(codigo_usuario, nombre, contrasena, email)

            if exito:
                self.mostrar_mensaje("Usuario actualizado exitosamente.", "Actualización Exitosa")

                # Restablecer los valores de los campos de entrada a vacíos
                self.ui.lineEdit_codigousuario.setText("")
                self.ui.lineEdit_nombre_2.setText("")
                self.ui.lineEdit_contrasena.setText("")
                self.ui.lineEdit_email.setText("")
            else:
                self.mostrar_mensaje("Error al actualizar usuario.", "Error")
        else:
            self.mostrar_mensaje("Por favor, complete todos los campos.", "Campos Incompletos")

    def eliminar_usuario(self):
        # Obtener el ID de usuario a eliminar
        id_usuario_a_eliminar = self.ui.lineEdit_eliminarid.text()

        # Verificar si el campo de ID está vacío
        if id_usuario_a_eliminar:
            # Llamar a la función consultar_usuario_por_id para verificar si el usuario existe
            usuario = consultar_usuario_por_id(id_usuario_a_eliminar)

            if usuario:
                # Si el usuario existe, llamar a la función eliminar_usuario desde crud.py
                eliminar_usuario(id_usuario_a_eliminar)
                self.mostrar_mensaje("Usuario eliminado exitosamente.", "Eliminación Exitosa")
                # Limpiar el campo de ID después de la eliminación
                self.ui.lineEdit_eliminarid.setText("")

                # Actualizar la tabla de usuarios después de la eliminación
                self.obtener_y_mostrar_usuarios()
            else:
                self.mostrar_mensaje("El usuario con el ID especificado no existe.", "Usuario No Encontrado")
        else:
            self.mostrar_mensaje("Por favor, ingrese el ID del usuario a eliminar.", "Campo Vacío")

    def enviar_mensaje_al_chatbot(self):
        # Obtener el mensaje del campo de entrada de texto
        mensaje = self.ui.text_mensaje.toPlainText()

        if mensaje:
            # Llamar a la función obtener_respuesta_del_chatbot desde chatbot.py
            respuesta = obtener_respuesta_del_chatbot(mensaje)

            # Agregar el mensaje y la respuesta a la conversación
            self.conversacion.append(f"Tú: {mensaje}")
            self.conversacion.append(f"Chatbot: {respuesta}")

            # Actualizar la ventana de chat
            self.mostrar_conversacion_en_chat()
        else:
            self.mostrar_mensaje("Por favor, ingresa un mensaje.", "Mensaje Vacío")

    def mostrar_conversacion_en_chat(self):
        # Limpiar el contenido actual del QTextBrowser
        self.ui.textChat.clear()

        # Mostrar la conversación en el QTextBrowser
        for mensaje in self.conversacion:
            self.ui.textChat.append(mensaje)

        # Limpiar el campo de entrada de texto después de mostrar la conversación
        self.ui.text_mensaje.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    vista = Vista()
    vista.show()
    sys.exit(app.exec())