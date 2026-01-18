"""
Simulador de NI-DAQmx per testejar sense hardware real
Genera dades sintètiques realistes
"""
import numpy as np
import time
from typing import Optional, Tuple


class MockTask:
    """Simula una tasca DAQmx."""
    
    def __init__(self, task_type='analog_input'):
        self.task_type = task_type
        self.is_started = False
        self.num_channels = 2
        self.sample_rate = 1000
        self.samples_generated = 0
        
        # Paràmetres per generar dades sintètiques realistes
        self.base_voltage = [2.5, 3.5]  # Voltatges base per cada sensor
        self.noise_amplitude = 0.05     # Amplitud del soroll
        self.drift_rate = 0.001         # Taxa de deriva lenta
        self.wave_frequency = 0.1       # Freqüència d'oscil·lació
        
    def start(self):
        """Inicia la tasca."""
        self.is_started = True
        self.start_time = time.time()
        
    def stop(self):
        """Atura la tasca."""
        self.is_started = False
        
    def close(self):
        """Tanca la tasca."""
        self.is_started = False
        
    def read(self, number_of_samples_per_channel, timeout=None):
        """
        Simula la lectura de mostres del hardware.
        Genera dades sintètiques realistes.
        
        Returns:
            Array de forma (num_channels, num_samples)
        """
        if not self.is_started:
            raise RuntimeError("Task not started")
        
        # Generar temps per les mostres
        current_time = time.time() - self.start_time
        time_array = np.linspace(
            current_time, 
            current_time + number_of_samples_per_channel / self.sample_rate,
            number_of_samples_per_channel
        )
        
        # Generar dades per cada canal
        data = []
        for channel_idx in range(self.num_channels):
            # Component base
            base = self.base_voltage[channel_idx]
            
            # Component de deriva lenta
            drift = self.drift_rate * current_time
            
            # Component d'oscil·lació (simula variacions del nivell d'aigua)
            wave = 0.2 * np.sin(2 * np.pi * self.wave_frequency * time_array + channel_idx)
            
            # Soroll gaussià
            noise = np.random.normal(0, self.noise_amplitude, number_of_samples_per_channel)
            
            # Combinar tots els components
            channel_data = base + drift + wave + noise
            
            # Limitar al rang del hardware (±10V)
            channel_data = np.clip(channel_data, -10, 10)
            
            data.append(channel_data)
        
        self.samples_generated += number_of_samples_per_channel
        
        return data
    
    def write(self, data):
        """Simula escriptura a sortida digital."""
        # No cal fer res en simulació
        pass


class MockAIChannels:
    """Simula els canals d'entrada analògica."""
    
    def add_ai_voltage_chan(self, channels, terminal_config=None, min_val=-10, max_val=10):
        """Simula afegir un canal d'entrada analògica."""
        pass


class MockDOChannels:
    """Simula els canals de sortida digital."""
    
    def add_do_chan(self, lines):
        """Simula afegir un canal de sortida digital."""
        pass


class MockTiming:
    """Simula la configuració de timing."""
    
    def cfg_samp_clk_timing(self, rate, sample_mode=None, samps_per_chan=1000):
        """Simula configuració del rellotge de mostreig."""
        pass


class MockDAQTask:
    """Simula completament una tasca DAQmx."""
    
    def __init__(self):
        self._task = None
        self.ai_channels = MockAIChannels()
        self.do_channels = MockDOChannels()
        self.timing = MockTiming()
        
    def start(self):
        if self._task is None:
            self._task = MockTask()
        self._task.start()
        
    def stop(self):
        if self._task:
            self._task.stop()
            
    def close(self):
        if self._task:
            self._task.close()
            self._task = None
            
    def read(self, number_of_samples_per_channel, timeout=None):
        if self._task is None or not self._task.is_started:
            raise RuntimeError("Task not started")
        return self._task.read(number_of_samples_per_channel, timeout)
    
    def write(self, data):
        if self._task:
            self._task.write(data)


class MockSystem:
    """Simula el sistema DAQmx."""
    
    class Device:
        def __init__(self, name, product_type):
            self.name = name
            self.product_type = product_type
    
    def __init__(self):
        # Simular dispositius disponibles
        self.devices = [
            self.Device("cDAQ1", "cDAQ-9174"),
            self.Device("cDAQ1Mod1", "NI 9201"),
            self.Device("cDAQ1Mod2", "NI 9472"),
        ]
    
    @staticmethod
    def local():
        """Retorna una instància del sistema local."""
        return MockSystem()


# Classes de constants simulades
class MockTerminalConfiguration:
    RSE = 'RSE'


class MockAcquisitionType:
    CONTINUOUS = 'CONTINUOUS'
    FINITE = 'FINITE'


class MockConstants:
    """Simula nidaqmx.constants."""
    TerminalConfiguration = MockTerminalConfiguration
    AcquisitionType = MockAcquisitionType
    WAIT_INFINITELY = -1


# Classe Task que simula nidaqmx.Task
# En nidaqmx real, Task és una classe, no una funció
Task = MockDAQTask


# Mòdul mock de nidaqmx
class MockNIDAQmx:
    """Simula el mòdul nidaqmx complet."""
    
    Task = Task
    constants = MockConstants
    
    class system:
        System = MockSystem


def get_mock_nidaqmx():
    """
    Retorna un mock del mòdul nidaqmx.
    Utilitzar en mode simulació.
    """
    return MockNIDAQmx()


# Variable global per activar/desactivar mode simulació
SIMULATION_MODE = False


def enable_simulation():
    """Activa el mode simulació."""
    global SIMULATION_MODE
    SIMULATION_MODE = True
    print("🎭 MODE SIMULACIÓ ACTIVAT")
    print("   - No es necessita hardware real")
    print("   - Les dades són sintètiques")
    print()


def is_simulation_enabled():
    """Comprova si el mode simulació està activat."""
    return SIMULATION_MODE
