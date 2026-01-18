"""
Diàleg de calibratge per configurar la conversió voltatge-alçada
Disseny horitzontal amb sensors un al costat de l'altre
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QDoubleSpinBox, QGroupBox, 
                               QMessageBox, QGridLayout)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from utils.calibration import CalibrationManager


class CalibrationDialog(QDialog):
    """Diàleg per calibrar els sensors."""
    
    def __init__(self, parent=None, daq=None):
        super().__init__(parent)
        self.setWindowTitle("Calibratge de Sensors")
        self.setMinimumSize(1100, 420)  # Reduït alçada de 480 a 420
        self.setMaximumHeight(520)  # Reduït de 580 a 520
        
        self.daq = daq
        self.calibration_manager = CalibrationManager()
        
        # Valors actuals llegits
        self.current_voltage1 = 0.0
        self.current_voltage2 = 0.0
        
        self.setup_ui()
        self.load_current_calibrations()
        
        # Timer per actualitzar voltatges contínuament
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_current_voltages)
        self.update_timer.start(500)  # Actualitzar cada 500ms
    
    def setup_ui(self):
        """Configura la interfície del diàleg."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)  # Reduït de 15 a 10
        
        # Títol
        title = QLabel("Calibratge de Sensors")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Instruccions en dues columnes
        instructions_container = QHBoxLayout()
        instructions_container.setSpacing(10)
        
        # Columna 1: Calibratge Software
        software_box = QGroupBox("📋 CALIBRATGE DEL PROGRAMA (Software)")
        software_box.setStyleSheet(
            "QGroupBox { "
            "font-weight: bold; "
            "font-size: 11px; "
            "color: #2c5282; "
            "border: 2px solid #2c5282; "
            "border-radius: 5px; "
            "margin-top: 10px; "
            "padding-top: 10px; "
            "background-color: #f0f7ff; "
            "} "
            "QGroupBox::title { "
            "subcontrol-origin: margin; "
            "subcontrol-position: top left; "
            "padding: 5px 10px; "
            "}"
        )
        software_layout = QVBoxLayout()
        software_layout.setSpacing(5)  # Reduït de 8 a 5
        
        software_label = QLabel(
            "Per calibrar la conversió <b>voltatge → alçada</b>:<br>"
            "<b>1.</b> Col·loca el sensor a una alçada coneguda (ex: 0 cm)<br>"
            "<b>2.</b> Prem <b>'Llegir'</b> per capturar el voltatge actual<br>"
            "<b>3.</b> Introdueix l'alçada al camp 'Alçada (cm)'<br>"
            "<b>4.</b> Repeteix per un segon punt a <b>diferent alçada</b> (ex: 20 cm)<br>"
            "<b>5.</b> Prem <b>'Desa i Tanca'</b> quan hagis calibrat ambdós punts"
        )
        software_label.setWordWrap(True)
        software_label.setStyleSheet("QLabel { font-size: 10px; color: #333; line-height: 1.4; }")  # Reduït de 1.8 a 1.4
        software_layout.addWidget(software_label)
        software_box.setLayout(software_layout)
        
        # Columna 2: Configuració Hardware
        hardware_box = QGroupBox("⚙️ CONFIGURACIÓ DEL SENSOR AWP-24-3 (Hardware)")
        hardware_box.setStyleSheet(
            "QGroupBox { "
            "font-weight: bold; "
            "font-size: 11px; "
            "color: #c05621; "
            "border: 2px solid #c05621; "
            "border-radius: 5px; "
            "margin-top: 10px; "
            "padding-top: 10px; "
            "background-color: #fffaf0; "
            "} "
            "QGroupBox::title { "
            "subcontrol-origin: margin; "
            "subcontrol-position: top left; "
            "padding: 5px 10px; "
            "}"
        )
        hardware_layout = QVBoxLayout()
        hardware_layout.setSpacing(5)  # Reduït de 8 a 5
        
        hardware_label = QLabel(
            "<i>Només cal fer-ho UNA VEGADA o si canvies el rang:</i><br>"
            "<b>1.</b> Treu la tapa del sensor que vols configurar (4 cargols estrella)<br>"
            "<b>2.</b> Verifica que el LED <span style='color: green;'>verd</span> (PWR) està encès<br>"
            "<b>3.</b> Si LED <span style='color: red;'>vermell</span> no està ON continu: manté <b>SET/CLEAR</b> premut 3 segons<br>"
            "<b>4.</b> Submergeix la sonda a la <b>profunditat MÀXIMA</b><br>"
            "<b>5.</b> Prem <b>SET/CLEAR</b> una vegada → LED parpelleja (1s ON, 1s OFF)<br>"
            "<b>6.</b> <b>NO moguis</b> la sonda fins que LED canviï a: 1s ON, 9s OFF ✅ Configurat!"
        )
        hardware_label.setWordWrap(True)
        hardware_label.setStyleSheet("QLabel { font-size: 10px; color: #333; line-height: 1.4; }")
        hardware_layout.addWidget(hardware_label)
        hardware_box.setLayout(hardware_layout)
        
        instructions_container.addWidget(software_box)
        instructions_container.addWidget(hardware_box)
        
        layout.addLayout(instructions_container)
        
        # Sensors en horitzontal
        sensors_layout = QHBoxLayout()
        
        # Sensor 1
        self.sensor1_group = self.create_sensor_group(0, "Sensor #1")
        sensors_layout.addWidget(self.sensor1_group)
        
        # Sensor 2
        self.sensor2_group = self.create_sensor_group(1, "Sensor #2")
        sensors_layout.addWidget(self.sensor2_group)
        
        layout.addLayout(sensors_layout)
        
        # Botons
        button_layout = QHBoxLayout()
        
        self.btn_reset = QPushButton("Reseteja Calibratge")
        self.btn_reset.clicked.connect(self.reset_calibration)
        button_layout.addWidget(self.btn_reset)
        
        button_layout.addStretch()
        
        self.btn_cancel = QPushButton("Cancel·la")
        self.btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.btn_cancel)
        
        self.btn_save = QPushButton("Desa i Tanca")
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.btn_save.clicked.connect(self.save_and_close)
        button_layout.addWidget(self.btn_save)
        
        layout.addLayout(button_layout)
    
    def create_sensor_group(self, sensor_id: int, title: str):
        """Crea un grup de controls per un sensor."""
        group = QGroupBox(title)
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # Voltatge actual
        row = 0
        layout.addWidget(QLabel("Voltatge actual:"), row, 0)
        voltage_label = QLabel("--- V")
        
        # Color segons sensor
        if sensor_id == 0:
            voltage_label.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; color: #4A90E2; }")
        else:
            voltage_label.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; color: #E24A4A; }")
        
        layout.addWidget(voltage_label, row, 1, 1, 2)
        
        # Punt 1
        row += 1
        layout.addWidget(QLabel("<b>Punt 1:</b>"), row, 0, 1, 3)
        
        row += 1
        layout.addWidget(QLabel("Voltatge (V):"), row, 0)
        v1_spin = QDoubleSpinBox()
        v1_spin.setRange(-10, 10)
        v1_spin.setDecimals(4)
        v1_spin.setReadOnly(True)
        v1_spin.setStyleSheet("QDoubleSpinBox { background-color: #f0f0f0; }")
        layout.addWidget(v1_spin, row, 1)
        
        btn_read1 = QPushButton("Llegir")
        btn_read1.setMaximumWidth(80)
        btn_read1.clicked.connect(lambda: self.read_current_voltage(sensor_id, 1))
        layout.addWidget(btn_read1, row, 2)
        
        row += 1
        layout.addWidget(QLabel("Alçada (cm):"), row, 0)
        h1_spin = QDoubleSpinBox()
        h1_spin.setRange(0, 1000)
        h1_spin.setDecimals(2)
        layout.addWidget(h1_spin, row, 1, 1, 2)
        
        # Punt 2
        row += 1
        layout.addWidget(QLabel("<b>Punt 2:</b>"), row, 0, 1, 3)
        
        row += 1
        layout.addWidget(QLabel("Voltatge (V):"), row, 0)
        v2_spin = QDoubleSpinBox()
        v2_spin.setRange(-10, 10)
        v2_spin.setDecimals(4)
        v2_spin.setReadOnly(True)
        v2_spin.setStyleSheet("QDoubleSpinBox { background-color: #f0f0f0; }")
        layout.addWidget(v2_spin, row, 1)
        
        btn_read2 = QPushButton("Llegir")
        btn_read2.setMaximumWidth(80)
        btn_read2.clicked.connect(lambda: self.read_current_voltage(sensor_id, 2))
        layout.addWidget(btn_read2, row, 2)
        
        row += 1
        layout.addWidget(QLabel("Alçada (cm):"), row, 0)
        h2_spin = QDoubleSpinBox()
        h2_spin.setRange(0, 1000)
        h2_spin.setDecimals(2)
        layout.addWidget(h2_spin, row, 1, 1, 2)
        
        # Estat calibratge
        row += 1
        status_label = QLabel("No calibrat")
        status_label.setStyleSheet("QLabel { color: #f44336; font-weight: bold; }")
        layout.addWidget(status_label, row, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        
        group.setLayout(layout)
        
        # Guardar referències als widgets
        if sensor_id == 0:
            self.voltage1_label = voltage_label
            self.s1_v1_spin = v1_spin
            self.s1_h1_spin = h1_spin
            self.s1_v2_spin = v2_spin
            self.s1_h2_spin = h2_spin
            self.s1_status = status_label
        else:
            self.voltage2_label = voltage_label
            self.s2_v1_spin = v1_spin
            self.s2_h1_spin = h1_spin
            self.s2_v2_spin = v2_spin
            self.s2_h2_spin = h2_spin
            self.s2_status = status_label
        
        return group
    
    def read_current_voltage(self, sensor_id: int, point: int):
        """Llegeix el voltatge actual del sensor."""
        if self.daq is None:
            QMessageBox.warning(self, "Error", "Sistema d'adquisició no disponible")
            return
        
        try:
            success, msg, values = self.daq.read_current_values()
            if success and values is not None:
                # values és una tupla (voltage1, voltage2)
                voltage = float(values[sensor_id])
                
                # Actualitzar el spin corresponent
                if sensor_id == 0:
                    self.current_voltage1 = voltage
                    self.voltage1_label.setText(f"{voltage:.4f} V")
                    if point == 1:
                        self.s1_v1_spin.setValue(voltage)
                    else:
                        self.s1_v2_spin.setValue(voltage)
                else:
                    self.current_voltage2 = voltage
                    self.voltage2_label.setText(f"{voltage:.4f} V")
                    if point == 1:
                        self.s2_v1_spin.setValue(voltage)
                    else:
                        self.s2_v2_spin.setValue(voltage)
            else:
                QMessageBox.warning(self, "Error", f"No s'ha pogut llegir el sensor: {msg}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error llegint sensor: {str(e)}")
    
    def load_current_calibrations(self):
        """Carrega les calibracions actuals."""
        # Sensor 1
        cal1 = self.calibration_manager.get_calibration(0)
        if cal1.is_calibrated():
            self.s1_v1_spin.setValue(cal1.point1[0])
            self.s1_h1_spin.setValue(cal1.point1[1])
            self.s1_v2_spin.setValue(cal1.point2[0])
            self.s1_h2_spin.setValue(cal1.point2[1])
            self.s1_status.setText("✓ Calibrat")
            self.s1_status.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; }")
        
        # Sensor 2
        cal2 = self.calibration_manager.get_calibration(1)
        if cal2.is_calibrated():
            self.s2_v1_spin.setValue(cal2.point1[0])
            self.s2_h1_spin.setValue(cal2.point1[1])
            self.s2_v2_spin.setValue(cal2.point2[0])
            self.s2_h2_spin.setValue(cal2.point2[1])
            self.s2_status.setText("✓ Calibrat")
            self.s2_status.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; }")
    
    def save_and_close(self):
        """Valida i desa les calibracions."""
        # Validar Sensor 1
        v1_1 = self.s1_v1_spin.value()
        h1_1 = self.s1_h1_spin.value()
        v1_2 = self.s1_v2_spin.value()
        h1_2 = self.s1_h2_spin.value()
        
        if abs(v1_2 - v1_1) < 0.001:
            QMessageBox.warning(
                self,
                "Error de validació",
                "Sensor #1: Els dos voltatges han de ser diferents (mínim 0.001V de diferència)"
            )
            return
        
        # Validar Sensor 2
        v2_1 = self.s2_v1_spin.value()
        h2_1 = self.s2_h1_spin.value()
        v2_2 = self.s2_v2_spin.value()
        h2_2 = self.s2_h2_spin.value()
        
        if abs(v2_2 - v2_1) < 0.001:
            QMessageBox.warning(
                self,
                "Error de validació",
                "Sensor #2: Els dos voltatges han de ser diferents (mínim 0.001V de diferència)"
            )
            return
        
        # Desar calibracions
        self.calibration_manager.set_calibration(0, v1_1, h1_1, v1_2, h1_2)
        self.calibration_manager.set_calibration(1, v2_1, h2_1, v2_2, h2_2)
        
        QMessageBox.information(
            self,
            "Calibratge desat",
            "Les calibracions s'han desat correctament"
        )
        
        self.accept()
    
    def reset_calibration(self):
        """Reseteja totes les calibracions."""
        reply = QMessageBox.question(
            self,
            "Reseteja calibratge",
            "Vols esborrar totes les calibracions?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.calibration_manager.reset()
            
            # Netejar tots els camps
            for spin in [self.s1_v1_spin, self.s1_v2_spin, self.s2_v1_spin, self.s2_v2_spin]:
                spin.setValue(0)
            for spin in [self.s1_h1_spin, self.s1_h2_spin, self.s2_h1_spin, self.s2_h2_spin]:
                spin.setValue(0)
            
            self.s1_status.setText("No calibrat")
            self.s1_status.setStyleSheet("QLabel { color: #f44336; font-weight: bold; }")
            self.s2_status.setText("No calibrat")
            self.s2_status.setStyleSheet("QLabel { color: #f44336; font-weight: bold; }")
            
            QMessageBox.information(self, "Resetejat", "Calibracions esborrades")
    
    def update_current_voltages(self):
        """Actualitza els voltatges actuals contínuament."""
        if self.daq is None:
            return
        
        try:
            success, msg, values = self.daq.read_current_values()
            if success and values is not None:
                v1 = float(values[0])
                v2 = float(values[1])
                
                self.current_voltage1 = v1
                self.current_voltage2 = v2
                
                # Actualitzar labels
                self.voltage1_label.setText(f"{v1:.4f} V")
                self.voltage2_label.setText(f"{v2:.4f} V")
        except Exception:
            pass  # Ignorar errors silenciosament
    
    def closeEvent(self, event):
        """Aturar timer en tancar."""
        self.update_timer.stop()
        event.accept()
