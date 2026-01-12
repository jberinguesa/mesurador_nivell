"""
Finestra principal de l'aplicació
Universitat de Girona - Departament de Física
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QDoubleSpinBox,
                             QFileDialog, QMessageBox, QFrame)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from datetime import datetime
import os

from daq.acquisition import DAQAcquisition
from daq.sensor import SensorManager
from data.file_handler import FileHandler
from utils.config import (
    WINDOW_TITLE, INSTITUTION_FOOTER, DEFAULT_SAMPLING_PERIOD,
    MIN_SAMPLING_PERIOD, MAX_SAMPLING_PERIOD, DEFAULT_FILENAME_PATTERN,
    PLOT_COLORS, AI_CHANNEL_NAMES, DEVICE_NAME
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
        
        # Estat de l'aplicació
        self.is_acquiring = False
        self.start_time = None
        self.acquisition_timer = QTimer()
        self.acquisition_timer.timeout.connect(self.on_acquisition_tick)
        
        # Dades per a la gràfica
        self.time_data = []
        self.voltage1_data = []
        self.voltage2_data = []
        
        # Crear interfície
        self.setup_ui()
        
        # Comprovar disponibilitat del hardware
        self.check_hardware()
    
    def setup_ui(self):
        """Configura la interfície gràfica."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Part esquerra: Gràfica (2/3)
        left_layout = QVBoxLayout()
        self.setup_plot()
        left_layout.addWidget(self.plot_widget)
        
        # Part dreta: Controls (1/3)
        right_layout = QVBoxLayout()
        self.setup_controls(right_layout)
        
        # Afegir layouts al principal
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 1)
        
        # Footer institucional
        self.setup_footer()
    
    def setup_plot(self):
        """Configura la gràfica temporal."""
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'Voltatge', units='V')
        self.plot_widget.setLabel('bottom', 'Temps', units='s')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.addLegend()
        
        # Crear línies per cada sensor
        self.plot_line1 = self.plot_widget.plot(
            [], [], pen=pg.mkPen(color=PLOT_COLORS[0], width=2),
            name=AI_CHANNEL_NAMES[0]
        )
        self.plot_line2 = self.plot_widget.plot(
            [], [], pen=pg.mkPen(color=PLOT_COLORS[1], width=2),
            name=AI_CHANNEL_NAMES[1]
        )
    
    def setup_controls(self, layout):
        """Configura els controls de la interfície."""
        # Botó Start
        self.btn_start = QPushButton('Start')
        self.btn_start.setMinimumHeight(40)
        self.btn_start.clicked.connect(self.on_start_clicked)
        layout.addWidget(self.btn_start)
        
        # Botó Stop
        self.btn_stop = QPushButton('Stop')
        self.btn_stop.setMinimumHeight(40)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.on_stop_clicked)
        layout.addWidget(self.btn_stop)
        
        # Botó Carregar mesura
        self.btn_load = QPushButton('Carregar mesura')
        self.btn_load.setMinimumHeight(40)
        self.btn_load.clicked.connect(self.on_load_clicked)
        layout.addWidget(self.btn_load)
        
        # Botó Neteja gràfica
        self.btn_clear = QPushButton('Neteja gràfica')
        self.btn_clear.setMinimumHeight(40)
        self.btn_clear.clicked.connect(self.on_clear_clicked)
        layout.addWidget(self.btn_clear)
        
        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Període de mostreig
        period_label = QLabel('Període de mostreig (s):')
        layout.addWidget(period_label)
        
        self.spin_period = QDoubleSpinBox()
        self.spin_period.setRange(MIN_SAMPLING_PERIOD, MAX_SAMPLING_PERIOD)
        self.spin_period.setValue(DEFAULT_SAMPLING_PERIOD)
        self.spin_period.setDecimals(3)
        self.spin_period.setSingleStep(0.01)
        layout.addWidget(self.spin_period)
        
        # Nom del fitxer
        filename_label = QLabel('Nom del fitxer:')
        layout.addWidget(filename_label)
        
        self.edit_filename = QLineEdit()
        default_filename = datetime.now().strftime(DEFAULT_FILENAME_PATTERN)
        self.edit_filename.setText(default_filename)
        self.edit_filename.setPlaceholderText('mesura1.xlsx')
        layout.addWidget(self.edit_filename)
        
        # Etiqueta d'estat
        layout.addWidget(QLabel('Estat:'))
        self.label_status = QLabel('Esperant...')
        self.label_status.setStyleSheet('QLabel { font-weight: bold; color: #666; }')
        layout.addWidget(self.label_status)
        
        # Espai flexible
        layout.addStretch()
    
    def setup_footer(self):
        """Configura el footer institucional."""
        footer = QLabel(INSTITUTION_FOOTER)
        footer.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        footer_font = QFont()
        footer_font.setPointSize(8)
        footer.setFont(footer_font)
        footer.setStyleSheet('QLabel { color: #888; margin: 5px; }')
        
        # Afegir al layout principal
        self.centralWidget().layout().addWidget(footer, 0, Qt.AlignRight | Qt.AlignBottom)
    
    def check_hardware(self):
        """Comprova si el hardware està disponible."""
        available, msg = DAQAcquisition.check_device_available(DEVICE_NAME)
        if not available:
            QMessageBox.warning(
                self,
                'Hardware no disponible',
                f'{msg}\n\nVerifiqueu la connexió i la configuració a NI MAX.'
            )
    
    def on_start_clicked(self):
        """Gestiona el clic al botó Start."""
        # Validar inputs
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
        
        # Comprovar si el fitxer existeix
        if check_file_exists(filename):
            reply = QMessageBox.question(
                self,
                'Fitxer existent',
                f'El fitxer "{filename}" ja existeix. Voleu sobreescriure\'l?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        # Netejar gràfica
        self.clear_plot()
        
        # Configurar tasques DAQmx
        success, msg = self.daq.setup_tasks()
        if not success:
            QMessageBox.critical(self, 'Error DAQmx', msg)
            return
        
        # Activar sensors
        success, msg = self.daq.activate_sensors()
        if not success:
            QMessageBox.critical(self, 'Error activant sensors', msg)
            self.daq.cleanup()
            return
        
        # Crear fitxer
        try:
            self.file_handler = FileHandler(filename)
            self.file_handler.create_file()
        except Exception as e:
            QMessageBox.critical(self, 'Error creant fitxer', str(e))
            self.daq.cleanup()
            return
        
        # Iniciar adquisició
        success, msg = self.daq.start_acquisition()
        if not success:
            QMessageBox.critical(self, 'Error iniciant adquisició', msg)
            self.daq.cleanup()
            return
        
        # Configurar estat
        self.is_acquiring = True
        self.start_time = datetime.now()
        
        # Configurar timer (convertir període a ms)
        timer_interval = int(period * 1000)
        self.acquisition_timer.start(timer_interval)
        
        # Actualitzar UI
        self.update_ui_for_acquisition(True)
        self.label_status.setText('Adquirint dades...')
        self.label_status.setStyleSheet('QLabel { font-weight: bold; color: green; }')
    
    def on_stop_clicked(self):
        """Gestiona el clic al botó Stop."""
        self.stop_acquisition()
    
    def on_load_clicked(self):
        """Gestiona el clic al botó Carregar mesura."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            'Carregar mesura',
            '',
            'Fitxers Excel (*.xlsx)'
        )
        
        if not filename:
            return
        
        # Carregar dades
        df = FileHandler.load_file(filename)
        if df is None:
            QMessageBox.critical(
                self,
                'Error carregant fitxer',
                'No s\'ha pogut carregar el fitxer o el format no és vàlid.'
            )
            return
        
        # Netejar gràfica
        self.clear_plot()
        
        # Dibuixar dades
        try:
            self.time_data = df['time_seconds'].tolist()
            self.voltage1_data = df['voltage_sensor1'].tolist()
            self.voltage2_data = df['voltage_sensor2'].tolist()
            
            self.update_plot()
            
            self.label_status.setText(f'Carregat: {os.path.basename(filename)}')
            self.label_status.setStyleSheet('QLabel { font-weight: bold; color: blue; }')
            
        except Exception as e:
            QMessageBox.critical(self, 'Error visualitzant dades', str(e))
    
    def on_clear_clicked(self):
        """Gestiona el clic al botó Neteja gràfica."""
        self.clear_plot()
        self.label_status.setText('Gràfica netejada')
        self.label_status.setStyleSheet('QLabel { font-weight: bold; color: #666; }')
    
    def on_acquisition_tick(self):
        """Executa cada cicle d'adquisició."""
        # Calcular nombre de mostres a llegir
        period = self.spin_period.value()
        from utils.config import SAMPLE_RATE
        num_samples = int(SAMPLE_RATE * period)
        
        # Llegir mostres
        success, msg, data = self.daq.read_samples(num_samples)
        if not success:
            QMessageBox.critical(self, 'Error d\'adquisició', msg)
            self.stop_acquisition()
            return
        
        # Processar dades
        try:
            voltage1, voltage2 = self.sensor_manager.process_multi_channel_data(data)
            
            # Calcular temps
            elapsed = (datetime.now() - self.start_time).total_seconds()
            
            # Afegir a les llistes
            self.time_data.append(elapsed)
            self.voltage1_data.append(voltage1)
            self.voltage2_data.append(voltage2)
            
            # Guardar al fitxer
            self.file_handler.append_data(elapsed, voltage1, voltage2)
            
            # Fer flush cada 10 punts
            if len(self.time_data) % 10 == 0:
                self.file_handler.flush_to_file()
            
            # Actualitzar gràfica
            self.update_plot()
            
        except Exception as e:
            QMessageBox.critical(self, 'Error processant dades', str(e))
            self.stop_acquisition()
    
    def stop_acquisition(self):
        """Atura l'adquisició de dades."""
        # Aturar timer
        self.acquisition_timer.stop()
        
        # Aturar tasques DAQmx
        self.daq.stop_acquisition()
        
        # Tancar fitxer
        if self.file_handler:
            self.file_handler.close()
            self.file_handler = None
        
        # Neteja DAQmx
        self.daq.cleanup()
        
        # Actualitzar estat
        self.is_acquiring = False
        
        # Actualitzar UI
        self.update_ui_for_acquisition(False)
        self.label_status.setText('Aturat')
        self.label_status.setStyleSheet('QLabel { font-weight: bold; color: #666; }')
    
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
    
    def update_plot(self):
        """Actualitza la gràfica amb les dades actuals."""
        self.plot_line1.setData(self.time_data, self.voltage1_data)
        self.plot_line2.setData(self.time_data, self.voltage2_data)
    
    def closeEvent(self, event):
        """Gestiona el tancament de la finestra."""
        if self.is_acquiring:
            reply = QMessageBox.question(
                self,
                'Adquisició activa',
                'Hi ha una adquisició en curs. Voleu aturar-la i tancar?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.stop_acquisition()
                event.accept()
            else:
                event.ignore()
        else:
            # Assegurar neteja
            self.daq.cleanup()
            event.accept()
