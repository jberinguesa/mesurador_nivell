"""
Mòdul d'adquisició de dades amb NI-DAQmx
"""
# Intentar importar nidaqmx real, si falla o està en mode simulació, usar mock
try:
    from simulation.mock_daq import is_simulation_enabled
    if is_simulation_enabled():
        raise ImportError("Simulation mode enabled")
    import nidaqmx
    from nidaqmx.constants import TerminalConfiguration
    USING_MOCK = False
except (ImportError, OSError):
    from simulation.mock_daq import get_mock_nidaqmx
    nidaqmx = get_mock_nidaqmx()
    TerminalConfiguration = nidaqmx.constants.TerminalConfiguration
    USING_MOCK = True
    print("⚠️  Utilitzant simulador DAQmx (hardware no disponible)")

import numpy as np
import time
from typing import Optional, Tuple
from utils.config import (
    AI_CHANNELS, DO_CHANNELS, VOLTAGE_RANGE_MIN, VOLTAGE_RANGE_MAX,
    SAMPLE_RATE, BUFFER_SIZE, SENSOR_STABILIZATION_TIME
)


class DAQAcquisition:
    """Gestiona l'adquisició de dades amb NI-DAQmx."""
    
    def __init__(self):
        """Inicialitza el sistema d'adquisició."""
        self.ai_task: Optional[nidaqmx.Task] = None
        self.do_task: Optional[nidaqmx.Task] = None
        self.is_running = False
        self.using_simulation = USING_MOCK
        
    def setup_tasks(self):
        """Configura les tasques DAQmx per entrada analògica i sortida digital."""
        try:
            # Crear tasca d'entrada analògica
            self.ai_task = nidaqmx.Task()
            self.ai_task.ai_channels.add_ai_voltage_chan(
                AI_CHANNELS,
                terminal_config=TerminalConfiguration.RSE,
                min_val=VOLTAGE_RANGE_MIN,
                max_val=VOLTAGE_RANGE_MAX
            )
            self.ai_task.timing.cfg_samp_clk_timing(
                rate=SAMPLE_RATE,
                sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                samps_per_chan=BUFFER_SIZE
            )
            
            # Crear tasca de sortida digital
            self.do_task = nidaqmx.Task()
            for channel in DO_CHANNELS:
                self.do_task.do_channels.add_do_chan(channel)
            
            mode = "SIMULACIÓ" if self.using_simulation else "REAL"
            return True, f"Tasques configurades (Mode: {mode})"
            
        except Exception as e:
            return False, f"Error configurant tasques DAQmx: {str(e)}"
    
    def activate_sensors(self):
        """Activa les sortides digitals per alimentar els sensors."""
        try:
            if self.do_task is None:
                return False, "Tasca de sortida digital no inicialitzada"
            
            # Activar tots els canals (DO0 i DO1)
            num_channels = len(DO_CHANNELS)
            self.do_task.write([True] * num_channels)
            
            # Esperar estabilització
            time.sleep(SENSOR_STABILIZATION_TIME)
            
            return True, ""
            
        except Exception as e:
            return False, f"Error activant sensors: {str(e)}"
    
    def deactivate_sensors(self):
        """Desactiva les sortides digitals."""
        try:
            if self.do_task is not None:
                num_channels = len(DO_CHANNELS)
                self.do_task.write([False] * num_channels)
            return True, ""
        except Exception as e:
            return False, f"Error desactivant sensors: {str(e)}"
    
    def start_acquisition(self):
        """Inicia l'adquisició de dades."""
        try:
            if self.ai_task is None:
                return False, "Tasca d'entrada analògica no inicialitzada"
            
            self.ai_task.start()
            self.is_running = True
            return True, ""
            
        except Exception as e:
            return False, f"Error iniciant adquisició: {str(e)}"
    
    def read_samples(self, num_samples: int) -> Tuple[bool, str, Optional[np.ndarray]]:
        """
        Llegeix mostres dels canals analògics.
        
        Args:
            num_samples: Nombre de mostres a llegir per canal
            
        Returns:
            Tupla (success, error_message, data)
            data és un array de forma (num_channels, num_samples)
        """
        try:
            if self.ai_task is None or not self.is_running:
                return False, "Adquisició no iniciada", None
            
            # Llegir dades (retorna array de forma [num_channels, num_samples])
            data = self.ai_task.read(
                number_of_samples_per_channel=num_samples,
                timeout=nidaqmx.constants.WAIT_INFINITELY
            )
            
            # Convertir a numpy array
            data_array = np.array(data)
            
            return True, "", data_array
            
        except Exception as e:
            return False, f"Error llegint mostres: {str(e)}", None
    
    def stop_acquisition(self):
        """Atura l'adquisició de dades."""
        try:
            if self.ai_task is not None and self.is_running:
                self.ai_task.stop()
                self.is_running = False
            return True, ""
        except Exception as e:
            return False, f"Error aturant adquisició: {str(e)}"
    
    def cleanup(self):
        """Neteja i tanca totes les tasques DAQmx."""
        try:
            # Aturar i tancar tasca d'entrada
            if self.ai_task is not None:
                if self.is_running:
                    self.ai_task.stop()
                self.ai_task.close()
                self.ai_task = None
            
            # Desactivar sensors i tancar tasca de sortida
            self.deactivate_sensors()
            if self.do_task is not None:
                self.do_task.close()
                self.do_task = None
            
            self.is_running = False
            return True, ""
            
        except Exception as e:
            return False, f"Error netejant tasques: {str(e)}"
    
    def read_current_values(self) -> Tuple[bool, str, Optional[Tuple[float, float]]]:
        """
        Llegeix valors puntuals dels sensors sense necessitat d'adquisició contínua.
        Utilitza les tasques existents si estan disponibles, sinó crea tasques temporals.
        
        Returns:
            Tupla (success, error_message, (voltage1, voltage2))
        """
        temp_do_task = None
        temp_ai_task = None
        try:
            # Si les tasques ja estan configurades, utilitzar-les
            if self.ai_task is not None and self.do_task is not None:
                # Assegurar que els sensors estan activats
                num_channels = len(DO_CHANNELS)
                self.do_task.write([True] * num_channels)
                
                # Crear una tasca temporal només per llegir (més ràpid que reconfigurar)
                temp_ai_task = nidaqmx.Task()
                temp_ai_task.ai_channels.add_ai_voltage_chan(
                    AI_CHANNELS,
                    terminal_config=TerminalConfiguration.RSE,
                    min_val=VOLTAGE_RANGE_MIN,
                    max_val=VOLTAGE_RANGE_MAX
                )
                values = temp_ai_task.read(number_of_samples_per_channel=1)
                temp_ai_task.close()
            else:
                # Activar sensors temporalment si no estan activats
                temp_do_task = nidaqmx.Task()
                for channel in DO_CHANNELS:
                    temp_do_task.do_channels.add_do_chan(channel)
                num_channels = len(DO_CHANNELS)
                temp_do_task.write([True] * num_channels)
                time.sleep(SENSOR_STABILIZATION_TIME)
                
                # Crear tasca temporal per llegir valors puntuals
                temp_ai_task = nidaqmx.Task()
                temp_ai_task.ai_channels.add_ai_voltage_chan(
                    AI_CHANNELS,
                    terminal_config=TerminalConfiguration.RSE,
                    min_val=VOLTAGE_RANGE_MIN,
                    max_val=VOLTAGE_RANGE_MAX
                )
                
                # Llegir una mostra de cada canal
                values = temp_ai_task.read(number_of_samples_per_channel=1)
                temp_ai_task.close()
                
                # Desactivar sensors si els hem activat temporalment
                num_channels = len(DO_CHANNELS)
                temp_do_task.write([False] * num_channels)
                temp_do_task.close()
                temp_do_task = None
            
            # Convertir a tupla (voltage1, voltage2)
            if isinstance(values, (list, tuple)) and len(values) >= 2:
                voltage1 = float(values[0])
                voltage2 = float(values[1])
            elif isinstance(values, np.ndarray):
                voltage1 = float(values[0]) if len(values) > 0 else 0.0
                voltage2 = float(values[1]) if len(values) > 1 else 0.0
            else:
                return False, "Format de dades inesperat", None
            
            return True, "", (voltage1, voltage2)
            
        except Exception as e:
            # Assegurar neteja en cas d'error
            if temp_do_task is not None:
                try:
                    num_channels = len(DO_CHANNELS)
                    temp_do_task.write([False] * num_channels)
                    temp_do_task.close()
                except:
                    pass
            if temp_ai_task is not None:
                try:
                    temp_ai_task.close()
                except:
                    pass
            return False, f"Error llegint valors actuals: {str(e)}", None
    
    @staticmethod
    def check_device_available(device_name: str) -> Tuple[bool, str]:
        """
        Comprova si un dispositiu DAQmx està disponible.
        
        Args:
            device_name: Nom del dispositiu (ex: 'cDAQ1')
            
        Returns:
            Tupla (is_available, error_message)
        """
        try:
            system = nidaqmx.system.System.local()
            devices = [dev.name for dev in system.devices]
            
            if device_name in devices:
                mode = "SIMULAT" if USING_MOCK else "REAL"
                return True, f"Dispositiu '{device_name}' disponible (Mode: {mode})"
            else:
                return False, f"Dispositiu '{device_name}' no trobat. Disponibles: {devices}"
                
        except Exception as e:
            return False, f"Error comprovant dispositius: {str(e)}"
