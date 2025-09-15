import sys
import json
import os
from datetime import datetime, time, date
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QTimeEdit, QPushButton, QListWidget, QMessageBox,
                             QGroupBox, QListWidgetItem, QTableWidget, 
                             QTableWidgetItem, QTabWidget, QHeaderView, QDateEdit,
                             QCalendarWidget, QTextEdit, QCheckBox, QFrame,
                             QListWidget, QDialog, QDialogButtonBox, QFormLayout,
                             QLineEdit, QListWidget, QInputDialog, QColorDialog,
                             QToolButton, QMenu, QAction, QDialog, QVBoxLayout,
                             QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt, QTime, QDate
from PyQt5.QtGui import QFont, QColor, QBrush, QTextCharFormat, QIcon, QPixmap

class EditarClaseDialog(QDialog):
    def __init__(self, clase_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Clase" if clase_data else "Agregar Clase")
        self.setGeometry(300, 300, 400, 500)
        
        self.clase_data = clase_data
        self.color = clase_data["color"] if clase_data and "color" in clase_data else "#C8E6FF"
        
        layout = QVBoxLayout()
        
        # Formulario
        form_layout = QFormLayout()
        
        self.nombre_input = QLineEdit()
        if clase_data:
            self.nombre_input.setText(clase_data["nombre"])
        form_layout.addRow("Nombre de la clase:", self.nombre_input)
        
        self.nrc_input = QLineEdit()
        if clase_data and "nrc" in clase_data:
            self.nrc_input.setText(clase_data["nrc"])
        form_layout.addRow("NRC:", self.nrc_input)
        
        self.profesor_input = QLineEdit()
        if clase_data and "profesor" in clase_data:
            self.profesor_input.setText(clase_data["profesor"])
        form_layout.addRow("Profesor:", self.profesor_input)
        
        self.aula_input = QLineEdit()
        if clase_data and "aula" in clase_data:
            self.aula_input.setText(clase_data["aula"])
        form_layout.addRow("Aula:", self.aula_input)
        
        # Día de la semana
        self.dia_combo = QComboBox()
        self.dia_combo.addItems(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
        if clase_data:
            self.dia_combo.setCurrentText(clase_data["dia"])
        form_layout.addRow("Día:", self.dia_combo)
        
        # Hora de inicio
        self.hora_inicio = QTimeEdit()
        self.hora_inicio.setDisplayFormat("HH:mm")
        if clase_data:
            hora, minuto = map(int, clase_data["hora_inicio"].split(":"))
            self.hora_inicio.setTime(QTime(hora, minuto))
        else:
            self.hora_inicio.setTime(QTime(8, 0))
        form_layout.addRow("Hora inicio:", self.hora_inicio)
        
        # Hora de fin
        self.hora_fin = QTimeEdit()
        self.hora_fin.setDisplayFormat("HH:mm")
        if clase_data:
            hora, minuto = map(int, clase_data["hora_fin"].split(":"))
            self.hora_fin.setTime(QTime(hora, minuto))
        else:
            self.hora_fin.setTime(QTime(9, 0))
        form_layout.addRow("Hora fin:", self.hora_fin)
        
        # Selector de color
        color_layout = QHBoxLayout()
        self.color_btn = QPushButton()
        self.color_btn.setFixedSize(30, 30)
        self.color_btn.setStyleSheet(f"background-color: {self.color}; border: 1px solid gray;")
        self.color_btn.clicked.connect(self.seleccionar_color)
        color_layout.addWidget(self.color_btn)
        color_layout.addWidget(QLabel("Color del curso"))
        form_layout.addRow("Color:", color_layout)
        
        layout.addLayout(form_layout)
        
        # Botones
        btn_layout = QHBoxLayout()
        guardar_btn = QPushButton("Guardar")
        guardar_btn.clicked.connect(self.accept)
        btn_layout.addWidget(guardar_btn)
        
        cancelar_btn = QPushButton("Cancelar")
        cancelar_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancelar_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def seleccionar_color(self):
        color = QColorDialog.getColor(QColor(self.color), self, "Seleccionar color")
        if color.isValid():
            self.color = color.name()
            self.color_btn.setStyleSheet(f"background-color: {self.color}; border: 1px solid gray;")
    
    def get_data(self):
        return {
            "nombre": self.nombre_input.text().strip(),
            "nrc": self.nrc_input.text().strip(),
            "profesor": self.profesor_input.text().strip(),
            "aula": self.aula_input.text().strip(),
            "dia": self.dia_combo.currentText(),
            "hora_inicio": self.hora_inicio.time().toString("HH:mm"),
            "hora_fin": self.hora_fin.time().toString("HH:mm"),
            "color": self.color
        }

class DetalleClaseDialog(QDialog):
    def __init__(self, clase_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detalles de la Clase")
        self.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout()
        
        # Mostrar detalles de la clase
        detalles = QTextEdit()
        detalles.setReadOnly(True)
        detalles.setHtml(f"""
        <h3>{clase_data['nombre']}</h3>
        <p><b>NRC:</b> {clase_data.get('nrc', 'No especificado')}</p>
        <p><b>Horario:</b> {clase_data['hora_inicio']} - {clase_data['hora_fin']}</p>
        <p><b>Aula:</b> {clase_data.get('aula', 'No especificado')}</p>
        <p><b>Profesor:</b> {clase_data.get('profesor', 'No especificado')}</p>
        <p><b>Día:</b> {clase_data['dia']}</p>
        """)
        
        layout.addWidget(detalles)
        
        # Botón para cerrar
        cerrar_btn = QPushButton("Cerrar")
        cerrar_btn.clicked.connect(self.accept)
        layout.addWidget(cerrar_btn)
        
        self.setLayout(layout)

class LoginDialog(QDialog):
    def __init__(self, usuarios, parent=None):
        super().__init__(parent)
        self.usuarios = usuarios
        self.setWindowTitle("Seleccionar Usuario")
        self.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()
        
        # Lista de usuarios
        self.lista_usuarios = QListWidget()
        for usuario in usuarios:
            self.lista_usuarios.addItem(usuario)
        layout.addWidget(QLabel("Selecciona an usuario:"))
        layout.addWidget(self.lista_usuarios)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        self.btn_seleccionar = QPushButton("Seleccionar")
        self.btn_seleccionar.clicked.connect(self.accept)
        btn_layout.addWidget(self.btn_seleccionar)
        
        self.btn_nuevo = QPushButton("Nuevo Usuario")
        self.btn_nuevo.clicked.connect(self.crear_nuevo_usuario)
        btn_layout.addWidget(self.btn_nuevo)
        
        self.btn_eliminar = QPushButton("Eliminar Usuario")
        self.btn_eliminar.clicked.connect(self.eliminar_usuario)
        btn_layout.addWidget(self.btn_eliminar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def crear_nuevo_usuario(self):
        nombre, ok = QInputDialog.getText(self, "Nuevo Usuario", "Nombre del nuevo usuario:")
        if ok and nombre:
            if nombre not in self.usuarios:
                self.usuarios.append(nombre)
                self.lista_usuarios.addItem(nombre)
                QMessageBox.information(self, "Éxito", f"Usuario '{nombre}' creado.")
            else:
                QMessageBox.warning(self, "Error", "El usuario ya existe.")
    
    def eliminar_usuario(self):
        current_item = self.lista_usuarios.currentItem()
        if current_item:
            usuario = current_item.text()
            if usuario != "default":
                respuesta = QMessageBox.question(self, "Eliminar Usuario", 
                                               f"¿Estás seguro de eliminar al usuario '{usuario}'?")
                if respuesta == QMessageBox.Yes:
                    self.usuarios.remove(usuario)
                    self.lista_usuarios.takeItem(self.lista_usuarios.row(current_item))
                    
                    # Eliminar archivos del usuario
                    if os.path.exists(f'data/{usuario}_tareas.json'):
                        os.remove(f'data/{usuario}_tareas.json')
                    if os.path.exists(f'data/{usuario}_clases.json'):
                        os.remove(f'data/{usuario}_clases.json')
            else:
                QMessageBox.warning(self, "Error", "No puedes eliminar el usuario default.")
        else:
            QMessageBox.warning(self, "Error", "Selecciona an usuario para eliminar.")
    
    def get_selected_user(self):
        current_item = self.lista_usuarios.currentItem()
        return current_item.text() if current_item else None

class TareaManager(QMainWindow):
    def __init__(self, usuario="default"):
        super().__init__()
        self.usuario = usuario
        self.tareas = []
        self.clases = []  # Lista de clases en lugar de horario por horas
        self.initUI()
        self.cargar_datos()
        
    def initUI(self):
        self.setWindowTitle(f'ClassTask Manager - {self.usuario}')
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central con pestañas
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)
        
        # Pestaña 1: Gestión de tareas
        tareas_tab = QWidget()
        self.setup_tareas_tab(tareas_tab)
        tab_widget.addTab(tareas_tab, "Gestión de Tareas")
        
        # Pestaña 2: Horario de clases (MEJORADA)
        horario_tab = QWidget()
        self.setup_horario_tab(horario_tab)
        tab_widget.addTab(horario_tab, "Horario de Clases")
        
        # Pestaña 3: Calendario unificado
        calendario_tab = QWidget()
        self.setup_calendario_tab(calendario_tab)
        tab_widget.addTab(calendario_tab, "Calendario Unificado")
        
        # Mostrar ventana
        self.show()
    
    def setup_tareas_tab(self, tab):
        layout = QHBoxLayout(tab)
        
        # Panel izquierdo para agregar tareas
        left_panel = QGroupBox("Agregar Nueva Tarea")
        left_layout = QVBoxLayout()
        
        # Nombre de la tarea
        left_layout.addWidget(QLabel("Nombre de la tarea:"))
        self.nombre_input = QLineEdit()
        left_layout.addWidget(self.nombre_input)
        
        # Nivel de importancia
        left_layout.addWidget(QLabel("Nivel de importancia:"))
        self.importancia_combo = QComboBox()
        self.importancia_combo.addItems(["Baja", "Media", "Alta"])
        left_layout.addWidget(self.importancia_combo)
        
        # Fecha de entrega
        left_layout.addWidget(QLabel("Fecha de entrega:"))
        self.fecha_entrega = QDateEdit()
        self.fecha_entrega.setDate(QDate.currentDate())
        self.fecha_entrega.setCalendarPopup(True)
        left_layout.addWidget(self.fecha_entrega)
        
        # Hora de entrega
        left_layout.addWidget(QLabel("Hora de entrega:"))
        self.entrega_time = QTimeEdit()
        self.entrega_time.setDisplayFormat("HH:mm")
        self.entrega_time.setTime(QTime.currentTime())
        left_layout.addWidget(self.entrega_time)
        
        # Botón para agregar tarea
        agregar_btn = QPushButton("Agregar Tarea")
        agregar_btn.clicked.connect(self.agregar_tarea)
        left_layout.addWidget(agregar_btn)
        
        left_panel.setLayout(left_layout)
        left_panel.setFixedWidth(300)
        
        # Panel derecho para mostrar tareas
        right_panel = QGroupBox("Tareas")
        right_layout = QVBoxLayout()
        
        # Filtros
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar por:"))
        
        self.filtro_fecha = QCheckBox("Hoy")
        self.filtro_fecha.stateChanged.connect(self.aplicar_filtros)
        filter_layout.addWidget(self.filtro_fecha)
        
        self.filtro_prioridad = QCheckBox("Alta prioridad")
        self.filtro_prioridad.stateChanged.connect(self.aplicar_filtros)
        filter_layout.addWidget(self.filtro_prioridad)
        
        self.filtro_completadas = QCheckBox("Mostrar completadas")
        self.filtro_completadas.stateChanged.connect(self.aplicar_filtros)
        filter_layout.addWidget(self.filtro_completadas)
        
        right_layout.addLayout(filter_layout)
        
        # Lista de tareas
        self.tareas_list = QListWidget()
        right_layout.addWidget(self.tareas_list)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        
        ordenar_btn = QPushButton("Ordenar por Prioridad")
        ordenar_btn.clicked.connect(self.mostrar_tareas)
        btn_layout.addWidget(ordenar_btn)
        
        eliminar_btn = QPushButton("Eliminar Tarea Seleccionada")
        eliminar_btn.clicked.connect(self.eliminar_tarea)
        btn_layout.addWidget(eliminar_btn)
        
        right_layout.addLayout(btn_layout)
        
        right_panel.setLayout(right_layout)
        
        # Añadir paneles al layout
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)
    
    def setup_horario_tab(self, tab):
        layout = QVBoxLayout(tab)
        
        # Panel superior para gestionar clases
        top_panel = QGroupBox("Gestión de Clases")
        top_layout = QHBoxLayout()
        
        # Botón para agregar clase
        agregar_btn = QPushButton("➕ Agregar Clase")
        agregar_btn.clicked.connect(self.agregar_clase)
        top_layout.addWidget(agregar_btn)
        
        # Botón para editar clase
        editar_btn = QPushButton("✏️ Editar Clase")
        editar_btn.clicked.connect(self.editar_clase)
        top_layout.addWidget(editar_btn)
        
        # Botón para eliminar clase
        eliminar_btn = QPushButton("🗑️ Eliminar Clase")
        eliminar_btn.clicked.connect(self.eliminar_clase)
        top_layout.addWidget(eliminar_btn)
        
        top_panel.setLayout(top_layout)
        layout.addWidget(top_panel)
        
        # Área de visualización del horario
        horario_frame = QGroupBox("Horario Semanal")
        horario_layout = QVBoxLayout()
        
        # Crear tabla de horario
        self.horario_table = QTableWidget()
        self.horario_table.setRowCount(14)  # 7:00 a 20:00 (14 horas)
        self.horario_table.setColumnCount(7)  # Lunes a Domingo
        
        # Encabezados de columnas (días)
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.horario_table.setHorizontalHeaderLabels(dias)
        
        # Encabezados de filas (horas)
        horas = [f"{h}:00" for h in range(7, 21)]
        self.horario_table.setVerticalHeaderLabels(horas)
        
        # Ajustar tamaño de las celdas
        self.horario_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horario_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Conectar doble clic para ver detalles
        self.horario_table.cellDoubleClicked.connect(self.mostrar_detalles_clase)
        
        horario_layout.addWidget(self.horario_table)
        horario_frame.setLayout(horario_layout)
        layout.addWidget(horario_frame)
        
        # Lista de todas las clases
        clases_frame = QGroupBox("Todas las Clases")
        clases_layout = QVBoxLayout()
        
        self.clases_list = QListWidget()
        self.clases_list.itemDoubleClicked.connect(self.mostrar_detalles_clase_lista)
        clases_layout.addWidget(self.clases_list)
        
        clases_frame.setLayout(clases_layout)
        layout.addWidget(clases_frame)
        
        # Actualizar la visualización
        self.actualizar_horario()
    
    def setup_calendario_tab(self, tab):
        layout = QVBoxLayout(tab)
        
        # Calendario para navegar por fechas
        self.calendario = QCalendarWidget()
        self.calendario.setGridVisible(True)
        self.calendario.clicked.connect(self.mostrar_eventos_fecha)
        layout.addWidget(self.calendario)
        
        # Área para mostrar eventos de la fecha seleccionada
        self.eventos_fecha_label = QLabel("Eventos para la fecha seleccionada:")
        layout.addWidget(self.eventos_fecha_label)
        
        self.eventos_fecha_text = QTextEdit()
        self.eventos_fecha_text.setReadOnly(True)
        layout.addWidget(self.eventos_fecha_text)
        
        # Mostrar eventos de hoy inicialmente
        self.mostrar_eventos_fecha(QDate.currentDate())
    
    def aplicar_filtros(self):
        tareas_filtradas = self.tareas.copy()
        
        # Filtrar por completadas
        if not self.filtro_completadas.isChecked():
            tareas_filtradas = [t for t in tareas_filtradas if not t["completada"]]
        
        # Filtrar por fecha (hoy)
        if self.filtro_fecha.isChecked():
            hoy = date.today()
            tareas_filtradas = [t for t in tareas_filtradas if t["fecha_entrega"] == hoy]
        
        # Filtrar por prioridad (alta)
        if self.filtro_prioridad.isChecked():
            tareas_filtradas = [t for t in tareas_filtradas if t["importancia"] == 3]
        
        # Mostrar tareas filtradas
        self.mostrar_tareas_lista(tareas_filtradas)
    
    def mostrar_tareas(self):
        self.mostrar_tareas_lista(self.tareas)
    
    def mostrar_tareas_lista(self, tareas_list):
        self.tareas_list.clear()
        
        if not tareas_list:
            item = QListWidgetItem("No hay tareas que mostrar.")
            item.setTextAlignment(Qt.AlignCenter)
            self.tareas_list.addItem(item)
            return
        
        # Ordenar tareas: importancia (desc), hora de entrega (asc)
        tareas_ordenadas = sorted(
            tareas_list,
            key=lambda t: (-t["importancia"], t["hora_entrega"])
        )
        
        for tarea in tareas_ordenadas:
            # Determinar color según importancia
            color = QColor(0, 0, 0)  # Negro por defecto
            if tarea["importancia"] == 3:  # Alta
                color = QColor(200, 0, 0)  # Rojo
            elif tarea["importancia"] == 2:  # Media
                color = QColor(0, 0, 200)  # Azul
            
            # Tachar texto si está completada
            texto = f"{tarea['nombre']} | Importancia: {tarea['importancia']} | " \
                    f"Entrega: {tarea['fecha_entrega'].strftime('%d/%m/%Y')} {tarea['hora_entrega'].strftime('%H:%M')}"
            
            if tarea["completada"]:
                texto = f"✓ {texto}"
            
            item = QListWidgetItem(texto)
            item.setForeground(color)
            item.setData(Qt.UserRole, tarea)  # Almacenar datos de la tarea
            
            # Checkbox para marcar como completada
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if tarea["completada"] else Qt.Unchecked)
            
            self.tareas_list.addItem(item)
        
        # Conectar señal de cambio de checkbox
        self.tareas_list.itemChanged.connect(self.tarea_completada)
    
    def tarea_completada(self, item):
        tarea = item.data(Qt.UserRole)
        if tarea in self.tareas:
            index = self.tareas.index(tarea)
            self.tareas[index]["completada"] = (item.checkState() == Qt.Checked)
            self.guardar_datos()
    
    def agregar_clase(self):
        dialog = EditarClaseDialog()
        if dialog.exec_() == QDialog.Accepted:
            nueva_clase = dialog.get_data()
            
            # Verificar que todos los campos obligatorios estén completos
            if not nueva_clase["nombre"]:
                QMessageBox.warning(self, "Error", "El nombre de la clase es obligatorio.")
                return
            
            # Verificar conflictos de horario
            conflictos = self.verificar_conflictos_clases(nueva_clase)
            if conflictos:
                respuesta = QMessageBox.question(self, "Conflicto de horario", 
                                  f"Esta clase se cruza con:\n{conflictos}\n¿Deseas agregarla de todos modos?",
                                  QMessageBox.Yes | QMessageBox.No)
                if respuesta == QMessageBox.No:
                    return
            
            self.clases.append(nueva_clase)
            self.actualizar_horario()
            self.guardar_datos()
            QMessageBox.information(self, "Éxito", "Clase agregada correctamente.")
    
    def editar_clase(self):
        if not self.clases:
            QMessageBox.warning(self, "Error", "No hay clases para editar.")
            return
        
        # Diálogo para seleccionar clase a editar
        clases_names = [f"{clase['nombre']} ({clase['dia']} {clase['hora_inicio']}-{clase['hora_fin']})" for clase in self.clases]
        clase_seleccionada, ok = QInputDialog.getItem(self, "Editar Clase", "Selecciona la clase a editar:", clases_names, 0, False)
        
        if ok and clase_seleccionada:
            index = clases_names.index(clase_seleccionada)
            dialog = EditarClaseDialog(self.clases[index])
            if dialog.exec_() == QDialog.Accepted:
                self.clases[index] = dialog.get_data()
                self.actualizar_horario()
                self.guardar_datos()
                QMessageBox.information(self, "Éxito", "Clase editada correctamente.")
    
    def eliminar_clase(self):
        if not self.clases:
            QMessageBox.warning(self, "Error", "No hay clases para eliminar.")
            return
        
        # Diálogo para seleccionar clase a eliminar
        clases_names = [f"{clase['nombre']} ({clase['dia']} {clase['hora_inicio']}-{clase['hora_fin']})" for clase in self.clases]
        clase_seleccionada, ok = QInputDialog.getItem(self, "Eliminar Clase", "Selecciona la clase a eliminar:", clases_names, 0, False)
        
        if ok and clase_seleccionada:
            index = clases_names.index(clase_seleccionada)
            respuesta = QMessageBox.question(self, "Confirmar eliminación", 
                                           f"¿Estás seguro de eliminar la clase '{clase_seleccionada}'?",
                                           QMessageBox.Yes | QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                self.clases.pop(index)
                self.actualizar_horario()
                self.guardar_datos()
                QMessageBox.information(self, "Éxito", "Clase eliminada correctamente.")
    
    def mostrar_detalles_clase(self, row, col):
        dia = self.horario_table.horizontalHeaderItem(col).text()
        hora = 7 + row  # Las filas empiezan desde las 7:00
        
        # Buscar la clase en esta celda
        for clase in self.clases:
            if clase["dia"] == dia:
                hora_inicio = int(clase["hora_inicio"].split(":")[0])
                hora_fin = int(clase["hora_fin"].split(":")[0])
                if hora_inicio <= hora < hora_fin:
                    self.mostrar_detalles(clase)
                    break
    
    def mostrar_detalles_clase_lista(self, item):
        index = self.clases_list.row(item)
        if 0 <= index < len(self.clases):
            self.mostrar_detalles(self.clases[index])
    
    def mostrar_detalles(self, clase):
        dialog = DetalleClaseDialog(clase, self)
        dialog.exec_()
    
    def verificar_conflictos_clases(self, nueva_clase):
        conflictos = []
        dia = nueva_clase["dia"]
        hora_inicio_nueva = int(nueva_clase["hora_inicio"].split(":")[0])
        hora_fin_nueva = int(nueva_clase["hora_fin"].split(":")[0])
        
        for clase_existente in self.clases:
            if clase_existente["dia"] == dia:
                hora_inicio_existente = int(clase_existente["hora_inicio"].split(":")[0])
                hora_fin_existente = int(clase_existente["hora_fin"].split(":")[0])
                
                # Verificar si hay superposición
                if (hora_inicio_nueva < hora_fin_existente and hora_fin_nueva > hora_inicio_existente):
                    conflicto = f"{clase_existente['nombre']} ({clase_existente['hora_inicio']}-{clase_existente['hora_fin']})"
                    conflictos.append(conflicto)
        
        return "\n".join(conflictos) if conflictos else ""
    
    def actualizar_horario(self):
        # Limpiar tabla
        for i in range(self.horario_table.rowCount()):
            for j in range(self.horario_table.columnCount()):
                self.horario_table.setItem(i, j, QTableWidgetItem(""))
        
        # Llenar tabla con las clases
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        for clase in self.clases:
            dia_index = dias.index(clase["dia"])
            hora_inicio = int(clase["hora_inicio"].split(":")[0])
            hora_fin = int(clase["hora_fin"].split(":")[0])
            
            for hora in range(hora_inicio, hora_fin):
                if 7 <= hora < 21:  # Solo entre 7:00 y 20:00
                    row = hora - 7
                    texto = f"{clase['nombre']}\n{clase['hora_inicio']}-{clase['hora_fin']}\nAula: {clase.get('aula', 'N/A')}"
                    
                    item = QTableWidgetItem(texto)
                    item.setBackground(QBrush(QColor(clase.get("color", "#C8E6FF"))))
                    item.setData(Qt.UserRole, clase)  # Guardar datos completos de la clase
                    self.horario_table.setItem(row, dia_index, item)
        
        # Actualizar lista de clases
        self.clases_list.clear()
        for clase in self.clases:
            item = QListWidgetItem(f"{clase['nombre']} - {clase['dia']} {clase['hora_inicio']}-{clase['hora_fin']}")
            item.setData(Qt.UserRole, clase)
            self.clases_list.addItem(item)
    
    def agregar_tarea(self):
        nombre = self.nombre_input.text().strip()
        
        if not nombre:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingresa un nombre para la tarea.")
            return
        
        # Obtener valores de importancia (1-3)
        importancia_map = {"Baja": 1, "Media": 2, "Alta": 3}
        importancia = importancia_map[self.importancia_combo.currentText()]
        
        # Obtener fechas y horas
        fecha_entrega = self.fecha_entrega.date().toPyDate()
        hora_entrega = self.entrega_time.time()
        
        # Crear objetos datetime
        datetime_entrega = datetime.combine(fecha_entrega, time(hora_entrega.hour(), hora_entrega.minute()))
        
        # Verificar conflictos con el horario de clases
        conflictos = self.verificar_conflictos_clases_tarea(fecha_entrega, hora_entrega.hour())
        
        if conflictos:
            QMessageBox.warning(self, "Conflicto de horario", 
                              f"Tienes clases a esta hora:\n{conflictos}\nNo puedes agregar una tarea en este horario.")
            return
        
        tarea = {
            "nombre": nombre,
            "importancia": importancia,
            "fecha_entrega": fecha_entrega,
            "hora_entrega": datetime_entrega,
            "completada": False
        }
        
        self.tareas.append(tarea)
        self.nombre_input.clear()
        
        # Actualizar lista y calendario
        self.mostrar_tareas()
        self.mostrar_eventos_fecha(self.calendario.selectedDate())
        self.guardar_datos()
        
        QMessageBox.information(self, "Éxito", "✅ Tarea agregada con éxito.")
    
    def verificar_conflictos_clases_tarea(self, fecha, hora):
        dia_semana = fecha.strftime("%A")
        
        # Traducir día al español
        dias_traduccion = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
        
        dia_es = dias_traduccion.get(dia_semana, dia_semana)
        
        # Verificar si hay clases a la misma hora
        for clase in self.clases:
            if clase["dia"] == dia_es:
                hora_inicio = int(clase["hora_inicio"].split(":")[0])
                hora_fin = int(clase["hora_fin"].split(":")[0])
                if hora_inicio <= hora < hora_fin:
                    return f"Clase de {clase['nombre']} a las {hora}:00"
        
        return ""
    
    def mostrar_eventos_fecha(self, fecha_qdate):
        fecha = fecha_qdate.toPyDate()
        texto = f"Eventos para {fecha.strftime('%A %d/%m/%Y')}:\n\n"
        
        # Obtener día de la semana en español
        dias_traduccion = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
        dia_semana = dias_traduccion.get(fecha.strftime("%A"), fecha.strftime("%A"))
        
        # Obtener tareas para esta fecha
        tareas_fecha = [t for t in self.tareas if t["fecha_entrega"] == fecha]
        
        # Obtener clases para este día de la semana
        clases_dia = []
        for clase in self.clases:
            if clase["dia"] == dia_semana:
                clases_dia.append(f"{clase['hora_inicio']}-{clase['hora_fin']} - {clase['nombre']} (Aula: {clase.get('aula', 'N/A')})")
        
        if not tareas_fecha and not clases_dia:
            texto += "No hay eventos para esta fecha."
        else:
            if clases_dia:
                texto += "<b>Clases:</b><br>"
                for clase in clases_dia:
                    texto += f"<span style='color:blue;'>{clase}</span><br>"
                texto += "<br>"
            
            if tareas_fecha:
                texto += "<b>Tareas:</b><br>"
                # Ordenar por hora
                tareas_ordenadas = sorted(tareas_fecha, key=lambda t: t["hora_entrega"])
                
                for tarea in tareas_ordenadas:
                    color = "black"
                    if tarea["importancia"] == 3:
                        color = "red"
                    elif tarea["importancia"] == 2:
                        color = "blue"
                    
                    estado = "✓ " if tarea["completada"] else ""
                    texto += f"<span style='color:{color};'><b>{tarea['hora_entrega'].strftime('%H:%M')}</b> - {estado}{tarea['nombre']} (Prioridad: {tarea['importancia']})</span><br>"
        
        self.eventos_fecha_text.setHtml(texto)
        
        # Resaltar fechas con eventos en el calendario
        self.resaltar_fechas_con_eventos()
    
    def resaltar_fechas_con_eventos(self):
        # Obtener todas las fechas con tareas
        fechas_con_tareas = set(t["fecha_entrega"] for t in self.tareas if not t["completada"])
        
        # Aplicar formato a fechas con eventos
        for fecha in fechas_con_tareas:
            qdate = QDate(fecha.year, fecha.month, fecha.day)
            char_format = QTextCharFormat()
            char_format.setFontWeight(QFont.Bold)
            
            # Colorear según la prioridad más alta de las tareas de ese día
            tareas_dia = [t for t in self.tareas if t["fecha_entrega"] == fecha and not t["completada"]]
            if tareas_dia:
                max_prioridad = max(t["importancia"] for t in tareas_dia)
                
                if max_prioridad == 3:
                    char_format.setBackground(QBrush(QColor(255, 200, 200)))  # Rojo claro
                elif max_prioridad == 2:
                    char_format.setBackground(QBrush(QColor(200, 200, 255)))  # Azul claro
                else:
                    char_format.setBackground(QBrush(QColor(200, 255, 200)))  # Verde claro
                    
                self.calendario.setDateTextFormat(qdate, char_format)
    
    def eliminar_tarea(self):
        current_item = self.tareas_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una tarea para eliminar.")
            return
        
        # Obtener la tarea desde los datos del item
        tarea = current_item.data(Qt.UserRole)
        
        if tarea in self.tareas:
            self.tareas.remove(tarea)
            self.mostrar_tareas()
            self.mostrar_eventos_fecha(self.calendario.selectedDate())
            self.guardar_datos()
            QMessageBox.information(self, "Éxito", "Tarea eliminada con éxito.")
    
    def guardar_datos(self):
        # Crear directorio de datos si no existe
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Guardar tareas
        tareas_serializable = []
        for tarea in self.tareas:
            tarea_serializable = tarea.copy()
            tarea_serializable["hora_entrega"] = tarea["hora_entrega"].isoformat()
            tarea_serializable["fecha_entrega"] = tarea["fecha_entrega"].isoformat()
            tareas_serializable.append(tarea_serializable)
        
        with open(f'data/{self.usuario}_tareas.json', 'w') as f:
            json.dump(tareas_serializable, f)
        
        # Guardar clases
        with open(f'data/{self.usuario}_clases.json', 'w') as f:
            json.dump(self.clases, f)
    
    def cargar_datos(self):
        # Cargar tareas
        try:
            with open(f'data/{self.usuario}_tareas.json', 'r') as f:
                tareas_serializable = json.load(f)
                
            for tarea in tareas_serializable:
                tarea["hora_entrega"] = datetime.fromisoformat(tarea["hora_entrega"])
                tarea["fecha_entrega"] = date.fromisoformat(tarea["fecha_entrega"])
                self.tareas.append(tarea)
        except FileNotFoundError:
            pass
        
        # Cargar clases
        try:
            with open(f'data/{self.usuario}_clases.json', 'r') as f:
                self.clases = json.load(f)
        except FileNotFoundError:
            pass
        
        # Actualizar interfaces
        self.mostrar_tareas()
        self.actualizar_horario()
        self.mostrar_eventos_fecha(QDate.currentDate())
    
    def closeEvent(self, event):
        self.guardar_datos()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Mejor aspecto visual
    
    # Establecer fuentes
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Cargar lista de usuarios
    usuarios = ["default"]
    if os.path.exists('data'):
        for file in os.listdir('data'):
            if file.endswith('_tareas.json'):
                usuario = file.replace('_tareas.json', '')
                if usuario not in usuarios:
                    usuarios.append(usuario)
    
    # Mostrar diálogo de selección de usuario
    login_dialog = LoginDialog(usuarios)
    if login_dialog.exec_() == QDialog.Accepted:
        usuario = login_dialog.get_selected_user()
        if usuario:
            window = TareaManager(usuario)
            sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
