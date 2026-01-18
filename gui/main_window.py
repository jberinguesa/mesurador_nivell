"""
Finestra principal de l'aplicació
Universitat de Girona - Departament de Física
Amb suport per calibratge voltatge → alçada
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QDoubleSpinBox,
                             QFileDialog, QMessageBox, QFrame, QDialog)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
import pyqtgraph as pg
from datetime import datetime
import os

from daq.acquisition import DAQAcquisition
from daq.sensor import SensorManager
from data.file_handler import FileHandler
from gui.calibration_dialog import CalibrationDialog
from utils.calibration import CalibrationManager
from utils.config import (
    WINDOW_TITLE, INSTITUTION_FOOTER, DEFAULT_SAMPLING_PERIOD,
    MIN_SAMPLING_PERIOD, MAX_SAMPLING_PERIOD, DEFAULT_FILENAME_PATTERN,
    PLOT_COLORS, AI_CHANNEL_NAMES, DEVICE_NAME, PLOT_UPDATE_INTERVAL
)
from utils.validators import validate_sampling_period, validate_filename, check_file_exists


class MainWindow(QMainWindow):
    """Finestra principal de l'aplicació."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(1000, 600)
        self.resize(1200, 700)
        
        # Components del sistema
        self.daq = DAQAcquisition()
        self.sensor_manager = SensorManager()
        self.file_handler = None
        self.calibration_manager = CalibrationManager()
        
        # Afegir [SIMULACIÓ] al títol si està en mode simulació
        if self.daq.using_simulation:
            self.setWindowTitle(f"{WINDOW_TITLE} [SIMULACIÓ]")
        
        # Estat de l'aplicació
        self.is_acquiring = False
        self.start_time = None
        self.sample_count = 0
        self.plot_update_counter = 0  # Comptador per actualitzar gràfica menys sovint
        self.acquisition_timer = QTimer()
        self.acquisition_timer.timeout.connect(self.on_acquisition_tick)
        
        # Timer per llegir valors contínuament quan no s'està gravant
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.on_monitor_tick)
        self.monitor_timer.start(500)
        
        # Dades per a la gràfica
        self.time_data = []
        self.voltage1_data = []
        self.voltage2_data = []
        
        # Crear interfície
        self.setup_ui()
        
        # Comprovar disponibilitat del hardware
        self.check_hardware()
        
        # Activar sensors per llegir valors contínuament
        self.setup_monitoring()
        
        # Fer una primera lectura després d'un petit delay
        QTimer.singleShot(1000, self.on_monitor_tick)
    
    def setup_ui(self):
        """Configura la interfície gràfica."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Part esquerra: Gràfica (5/6 - més espai)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(0)
        self.setup_plot()
        left_layout.addWidget(self.plot_widget)
        
        # Part dreta: Controls (1/6 - més estret)
        right_widget = QWidget()
        right_widget.setStyleSheet('QWidget { background-color: #2b2b2b; }')
        right_widget.setMinimumWidth(280)
        right_widget.setMaximumWidth(280)  # Fixar amplada exacta
        right_layout = QVBoxLayout(right_widget)
        self.setup_controls(right_layout)
        
        # Afegir widgets al principal
        main_layout.addWidget(left_widget, 5)
        main_layout.addWidget(right_widget, 1)
    
    def setup_plot(self):
        """Configura la gràfica temporal."""
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        
        # Etiqueta Y - mostrar què s'està graficant
        if self.calibration_manager.are_all_calibrated():
            self.plot_widget.setLabel('left', 'Alçada (cm)', color='#333', size='11pt')
            # Afegir nota explicativa
            note = pg.TextItem(text='Nota: Valors convertits de voltatge a alçada segons calibratge', 
                              color='#666', anchor=(0, 0))
            note.setPos(0, 0)
        else:
            self.plot_widget.setLabel('left', 'Voltatge (V)', color='#333', size='11pt')
        
        self.plot_widget.setLabel('bottom', 'Temps', units='s')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.addLegend()
        
        # Crear línies per cada sensor amb noms que indiquin la unitat
        sensor1_name = AI_CHANNEL_NAMES[0]
        sensor2_name = AI_CHANNEL_NAMES[1]
        
        if self.calibration_manager.are_all_calibrated():
            sensor1_name += " (cm)"
            sensor2_name += " (cm)"
        else:
            sensor1_name += " (V)"
            sensor2_name += " (V)"
        
        self.plot_line1 = self.plot_widget.plot(
            [], [], pen=pg.mkPen(color=PLOT_COLORS[0], width=2),
            name=sensor1_name
        )
        self.plot_line2 = self.plot_widget.plot(
            [], [], pen=pg.mkPen(color=PLOT_COLORS[1], width=2),
            name=sensor2_name
        )
    
    def setup_controls(self, layout):
        """Configura els controls de la interfície."""
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Estil millorat per text més clar
        label_style = 'QLabel { font-size: 11px; color: #e0e0e0; font-weight: 500; }'
        
        # Botons Start i Stop horitzontal
        start_stop_layout = QHBoxLayout()
        
        self.btn_start = QPushButton('Start')
        self.btn_start.setMinimumHeight(35)
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #999;
            }
        """)
        self.btn_start.clicked.connect(self.on_start_clicked)
        start_stop_layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton('Stop')
        self.btn_stop.setMinimumHeight(35)
        self.btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #999;
            }
        """)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.on_stop_clicked)
        start_stop_layout.addWidget(self.btn_stop)
        
        layout.addLayout(start_stop_layout)
        
        # Botó Carregar mesura
        self.btn_load = QPushButton('Carregar mesura')
        self.btn_load.setMinimumHeight(35)
        self.btn_load.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.btn_load.clicked.connect(self.on_load_clicked)
        layout.addWidget(self.btn_load)
        
        # Botó Neteja gràfica
        self.btn_clear = QPushButton('Neteja gràfica')
        self.btn_clear.setMinimumHeight(35)
        self.btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        self.btn_clear.clicked.connect(self.on_clear_clicked)
        layout.addWidget(self.btn_clear)
        
        # Botó Calibratge
        self.btn_calibration = QPushButton('⚙️ Calibratge')
        self.btn_calibration.setMinimumHeight(35)
        self.btn_calibration.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        self.btn_calibration.clicked.connect(self.on_calibration_clicked)
        layout.addWidget(self.btn_calibration)
        
        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet('QFrame { color: #555; }')
        layout.addWidget(line)
        
        # Footer institucional (a dalt, on era simulació)
        footer_top = QLabel(INSTITUTION_FOOTER)
        footer_top.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_font = QFont()
        footer_font.setPointSize(8)
        footer_top.setFont(footer_font)
        footer_top.setStyleSheet('QLabel { color: #999; margin: 8px; }')
        footer_top.setWordWrap(True)
        layout.addWidget(footer_top)
        
        # Petit separador
        layout.addSpacing(5)
        
        # Període de mostreig
        period_label = QLabel('Període de mostreig (s):')
        period_label.setStyleSheet(label_style)
        layout.addWidget(period_label)
        
        self.spin_period = QDoubleSpinBox()
        self.spin_period.setRange(MIN_SAMPLING_PERIOD, MAX_SAMPLING_PERIOD)
        self.spin_period.setValue(DEFAULT_SAMPLING_PERIOD)
        self.spin_period.setDecimals(3)
        self.spin_period.setSingleStep(0.01)
        self.spin_period.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.spin_period)
        
        # Nom del fitxer
        filename_label = QLabel('Nom del fitxer:')
        filename_label.setStyleSheet(label_style)
        layout.addWidget(filename_label)
        
        self.edit_filename = QLineEdit()
        default_filename = datetime.now().strftime(DEFAULT_FILENAME_PATTERN)
        self.edit_filename.setText(default_filename)
        self.edit_filename.setPlaceholderText('mesura1.xlsx')
        self.edit_filename.setStyleSheet("""
            QLineEdit {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.edit_filename)
        
        # Etiqueta d'estat
        estat_label = QLabel('Estat:')
        estat_label.setStyleSheet(label_style)
        layout.addWidget(estat_label)
        
        self.label_status = QLabel('Esperant...')
        self.label_status.setStyleSheet('QLabel { font-weight: bold; color: #bbb; font-size: 11px; }')
        layout.addWidget(self.label_status)
        
        # Separador
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        line2.setStyleSheet('QFrame { color: #555; }')
        layout.addWidget(line2)
        
        # Displays de voltatge + alçada (horitzontal)
        sensors_layout = QHBoxLayout()
        
        # Sensor 1
        sensor1_container = QVBoxLayout()
        sensor1_label = QLabel(f'{AI_CHANNEL_NAMES[0]}:')
        sensor1_label.setStyleSheet('QLabel { font-size: 11px; color: #e0e0e0; font-weight: 500; }')
        sensor1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sensor1_container.addWidget(sensor1_label)
        
        self.label_voltage1 = QLabel('--- V\n-- cm')
        self.label_voltage1.setMinimumHeight(70)
        self.label_voltage1.setMinimumWidth(120)  # Amplada fixa
        self.label_voltage1.setMaximumWidth(120)
        self.label_voltage1.setStyleSheet(
            'QLabel { '
            'font-size: 18px; '
            'font-weight: bold; '
            'color: #4A90E2; '
            'background-color: #1e1e1e; '
            'border: 2px solid #4A90E2; '
            'border-radius: 5px; '
            'padding: 8px; '
            '}'
        )
        self.label_voltage1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sensor1_container.addWidget(self.label_voltage1)
        
        # Sensor 2
        sensor2_container = QVBoxLayout()
        sensor2_label = QLabel(f'{AI_CHANNEL_NAMES[1]}:')
        sensor2_label.setStyleSheet('QLabel { font-size: 11px; color: #e0e0e0; font-weight: 500; }')
        sensor2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sensor2_container.addWidget(sensor2_label)
        
        self.label_voltage2 = QLabel('--- V\n-- cm')
        self.label_voltage2.setMinimumHeight(70)
        self.label_voltage2.setMinimumWidth(120)  # Amplada fixa
        self.label_voltage2.setMaximumWidth(120)
        self.label_voltage2.setStyleSheet(
            'QLabel { '
            'font-size: 18px; '
            'font-weight: bold; '
            'color: #E24A4A; '
            'background-color: #1e1e1e; '
            'border: 2px solid #E24A4A; '
            'border-radius: 5px; '
            'padding: 8px; '
            '}'
        )
        self.label_voltage2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sensor2_container.addWidget(self.label_voltage2)
        
        sensors_layout.addLayout(sensor1_container)
        sensors_layout.addLayout(sensor2_container)
        layout.addLayout(sensors_layout)
        
        # Footer institucional (final - ja no cal, està a dalt)
        layout.addStretch()
    
    def on_calibration_clicked(self):
        """Obre el diàleg de calibratge."""
        dialog = CalibrationDialog(self, self.daq)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Recarregar calibracions
            self.calibration_manager.load()
            
            # Netejar i recrear gràfica amb noves etiquetes
            self.clear_plot()
            
            # Recrear plot widget amb etiquetes actualitzades
            old_plot = self.plot_widget
            parent = old_plot.parent()
            layout = parent.layout()
            
            # Eliminar plot antic
            layout.removeWidget(old_plot)
            old_plot.deleteLater()
            
            # Crear plot nou
            self.setup_plot()
            layout.addWidget(self.plot_widget)
            
            QMessageBox.information(
                self,
                'Calibratge actualitzat',
                'Les calibracions s\'han aplicat correctament.\n'
                'La gràfica mostra ara alçada en cm.'
            )
    
    def setup_monitoring(self):
        """Configura el sistema per llegir valors contínuament."""
        try:
            success, msg = self.daq.setup_tasks()
            if success:
                self.daq.activate_sensors()
        except Exception:
            pass
    
    def on_monitor_tick(self):
        """Llegeix valors actuals quan no s'està gravant."""
        if not self.is_acquiring:
            try:
                success, msg, values = self.daq.read_current_values()
                if success and values is not None:
                    voltage1, voltage2 = values
                    self.update_voltage_labels(voltage1, voltage2)
                elif not success and "no inicialitzada" not in msg.lower():
                    try:
                        self.daq.setup_tasks()
                        self.daq.activate_sensors()
                    except Exception:
                        pass
            except Exception:
                pass
    
    def check_hardware(self):
        """Comprova si el hardware està disponible."""
        available, msg = DAQAcquisition.check_device_available(DEVICE_NAME)
        if not available and not self.daq.using_simulation:
            QMessageBox.warning(
                self,
                'Hardware no disponible',
                f'{msg}\n\nVerifiqueu la connexió i la configuració a NI MAX.'
            )
    
    def on_start_clicked(self):
        """Gestiona el clic al botó Start."""
        period = self.spin_period.value()
        valid_period, msg_period = validate_sampling_period(period)
        if not valid_period:
            QMessageBox.warning(self, 'Error de validació', msg_period)
            return
        
        filename = self.edit_filename.text()
        valid_filename, msg_filename = validate_filename(filename)
        if not valid_filename:
            QMessageBox.warning(self, 'Error de validació', msg_filename)
            return
        
        # Crear directori Mesures si no existeix
        mesures_dir = "Mesures"
        if not os.path.exists(mesures_dir):
            os.makedirs(mesures_dir)
        
        # Camí complet del fitxer dins del directori Mesures
        full_filepath = os.path.join(mesures_dir, filename)
        
        if check_file_exists(full_filepath):
            reply = QMessageBox.question(
                self,
                'Fitxer existent',
                f'El fitxer "{filename}" ja existeix. Voleu sobreescriure\'l?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        self.clear_plot()
        
        success, msg = self.daq.setup_tasks()
        if not success:
            QMessageBox.critical(self, 'Error DAQmx', msg)
            return
        
        success, msg = self.daq.activate_sensors()
        if not success:
            QMessageBox.critical(self, 'Error activant sensors', msg)
            self.daq.cleanup()
            return
        
        try:
            self.file_handler = FileHandler(full_filepath)
            self.file_handler.create_file()
        except Exception as e:
            QMessageBox.critical(self, 'Error creant fitxer', str(e))
            self.daq.cleanup()
            return
        
        success, msg = self.daq.start_acquisition()
        if not success:
            QMessageBox.critical(self, 'Error iniciant adquisició', msg)
            self.daq.cleanup()
            return
        
        self.is_acquiring = True
        self.start_time = datetime.now()
        self.sample_count = 0
        self.plot_update_counter = 0  # Reiniciar comptador de refresc
        
        timer_interval = int(period * 1000)
        self.acquisition_timer.start(timer_interval)
        
        self.update_ui_for_acquisition(True)
        self.label_status.setText('Adquirint dades...')
        self.label_status.setStyleSheet('QLabel { font-weight: bold; color: #4CAF50; font-size: 11px; }')
    
    def on_stop_clicked(self):
        """Gestiona el clic al botó Stop."""
        self.stop_acquisition()
    
    def on_load_clicked(self):
        """Gestiona el clic al botó Carregar mesura."""
        # Crear directori Mesures si no existeix
        mesures_dir = "Mesures"
        if not os.path.exists(mesures_dir):
            os.makedirs(mesures_dir)
        
        filename, _ = QFileDialog.getOpenFileName(
            self,
            'Carregar mesura',
            mesures_dir,  # Obrir directament al directori Mesures
            'Fitxers Excel (*.xlsx)'
        )
        
        if not filename:
            return
        
        df = FileHandler.load_file(filename)
        if df is None:
            QMessageBox.critical(
                self,
                'Error carregant fitxer',
                'No s\'ha pogut carregar el fitxer o el format no és vàlid.'
            )
            return
        
        self.clear_plot()
        
        try:
            self.time_data = df['time_seconds'].tolist()
            
            # Decidir si mostrar alçada o voltatge segons calibratge
            if self.calibration_manager.are_all_calibrated() and 'height_sensor1' in df.columns:
                # Mostrar alçada si està disponible i calibrat
                self.voltage1_data = df['height_sensor1'].fillna(df['voltage_sensor1']).tolist()
                self.voltage2_data = df['height_sensor2'].fillna(df['voltage_sensor2']).tolist()
            else:
                # Mostrar voltatge
                self.voltage1_data = df['voltage_sensor1'].tolist()
                self.voltage2_data = df['voltage_sensor2'].tolist()
            
            self.update_plot()
            
            if len(self.voltage1_data) > 0 and len(self.voltage2_data) > 0:
                # Mostrar últims valors (sempre en voltatge + alçada als displays)
                v1 = df['voltage_sensor1'].iloc[-1]
                v2 = df['voltage_sensor2'].iloc[-1]
                self.update_voltage_labels(v1, v2)
            
            self.label_status.setText(f'Carregat: {os.path.basename(filename)}')
            self.label_status.setStyleSheet('QLabel { font-weight: bold; color: #2196F3; font-size: 11px; }')
            
        except Exception as e:
            QMessageBox.critical(self, 'Error visualitzant dades', str(e))
    
    def on_clear_clicked(self):
        """Gestiona el clic al botó Neteja gràfica."""
        self.clear_plot()
        self.label_status.setText('Gràfica netejada')
        self.label_status.setStyleSheet('QLabel { font-weight: bold; color: #bbb; font-size: 11px; }')
    
    def on_acquisition_tick(self):
        """Executa cada cicle d'adquisició."""
        period = self.spin_period.value()
        from utils.config import SAMPLE_RATE
        num_samples = int(SAMPLE_RATE * period)
        
        success, msg, data = self.daq.read_samples(num_samples)
        if not success:
            QMessageBox.critical(self, 'Error d\'adquisició', msg)
            self.stop_acquisition()
            return
        
        try:
            voltage1, voltage2 = self.sensor_manager.process_multi_channel_data(data)
            
            # Convertir a alçada
            height1 = self.calibration_manager.voltage_to_height(0, voltage1)
            height2 = self.calibration_manager.voltage_to_height(1, voltage2)
            
            elapsed = self.sample_count * period
            self.sample_count += 1
            
            self.time_data.append(elapsed)
            
            # Graficar alçada si està calibrat, sinó voltatge
            if height1 is not None:
                self.voltage1_data.append(height1)
            else:
                self.voltage1_data.append(voltage1)
            
            if height2 is not None:
                self.voltage2_data.append(height2)
            else:
                self.voltage2_data.append(voltage2)
            
            # Desar voltatge + alçada
            self.file_handler.append_data(elapsed, voltage1, voltage2, height1, height2)
            
            if len(self.time_data) % 10 == 0:
                self.file_handler.flush_to_file()
            
            # Actualitzar gràfica només cada PLOT_UPDATE_INTERVAL mostres
            self.plot_update_counter += 1
            if self.plot_update_counter >= PLOT_UPDATE_INTERVAL:
                self.update_plot()
                self.plot_update_counter = 0
            
            # Actualitzar displays cada mostra (és ràpid)
            self.update_voltage_labels(voltage1, voltage2)
            
        except Exception as e:
            QMessageBox.critical(self, 'Error processant dades', str(e))
            self.stop_acquisition()
    
    def stop_acquisition(self):
        """Atura l'adquisició de dades."""
        self.acquisition_timer.stop()
        self.daq.stop_acquisition()
        
        # Actualitzar gràfica una última vegada per mostrar totes les dades
        self.update_plot()
        
        # Flush final de dades
        if self.file_handler:
            self.file_handler.close()
            self.file_handler = None
        
        self.daq.cleanup()
        self.is_acquiring = False
        
        self.update_ui_for_acquisition(False)
        self.label_status.setText('Aturat')
        self.label_status.setStyleSheet('QLabel { font-weight: bold; color: #bbb; font-size: 11px; }')
        
        self.setup_monitoring()
    
    def update_ui_for_acquisition(self, acquiring: bool):
        """Actualitza l'estat dels controls segons si s'està adquirint."""
        self.btn_start.setEnabled(not acquiring)
        self.btn_stop.setEnabled(acquiring)
        self.spin_period.setEnabled(not acquiring)
        self.edit_filename.setEnabled(not acquiring)
    
    def clear_plot(self):
        """Neteja la gràfica."""
        self.time_data.clear()
        self.voltage1_data.clear()
        self.voltage2_data.clear()
        self.plot_line1.setData([], [])
        self.plot_line2.setData([], [])
        
        self.label_voltage1.setText('--- V\n-- cm')
        self.label_voltage2.setText('--- V\n-- cm')
    
    def update_plot(self):
        """Actualitza la gràfica amb les dades actuals."""
        self.plot_line1.setData(self.time_data, self.voltage1_data)
        self.plot_line2.setData(self.time_data, self.voltage2_data)
    
    def update_voltage_labels(self, voltage1: float, voltage2: float):
        """Actualitza els labels amb voltatge i alçada."""
        # Sensor 1
        h1 = self.calibration_manager.voltage_to_height(0, voltage1)
        if h1 is not None:
            self.label_voltage1.setText(f'{voltage1:.3f} V\n{h1:.1f} cm')
        else:
            self.label_voltage1.setText(f'{voltage1:.3f} V\n-- cm')
        
        # Sensor 2
        h2 = self.calibration_manager.voltage_to_height(1, voltage2)
        if h2 is not None:
            self.label_voltage2.setText(f'{voltage2:.3f} V\n{h2:.1f} cm')
        else:
            self.label_voltage2.setText(f'{voltage2:.3f} V\n-- cm')
    
    def closeEvent(self, event):
        """Gestiona el tancament de la finestra."""
        self.monitor_timer.stop()
        
        if self.is_acquiring:
            reply = QMessageBox.question(
                self,
                'Adquisició activa',
                'Hi ha una adquisició en curs. Voleu aturar-la i tancar?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.stop_acquisition()
                event.accept()
            else:
                event.ignore()
        else:
            self.daq.cleanup()
            event.accept()
