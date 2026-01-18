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
except ImportError as e:
    if "Simulation mode enabled" in str(e):
        from simulation.mock_daq import get_mock_nidaqmx
        nidaqmx = get_mock_nidaqmx()
        TerminalConfiguration = nidaqmx.constants.TerminalConfiguration
        USING_MOCK = True
        print("🎭 Mode simulació activat")
    else:
        print("❌ ERROR: nidaqmx no està instal·lat o NI-DAQmx Runtime no està disponible")
        print("   Instal·leu:")
        print("   1. NI-DAQmx Runtime des de ni.com")
        print("   2. pip install nidaqmx")
        print()
        print("   Per provar sense hardware, executeu: python main_simulation.py")
        raise
except OSError as e:
    print(f"❌ ERROR d'accés al hardware DAQmx: {e}")
    print("   Verifiqueu:")
    print("   - Que el cDAQ està connectat i encès")
    print("   - Que el dispositiu és visible a NI MAX")
    print()
    print("   Per provar sense hardware, executeu: python main_simulation.py")
    raise

import numpy as np
import time
from typing import Optional, Tuple
from utils.config import (
    AI_CHANNELS, DO_CHANNELS, VOLTAGE_RANGE_MIN, VOLTAGE_RANGE_MAX,
    SAMPLE_RATE, BUFFER_SIZE, SENSOR_STABILIZATION_TIME
)


class DAQAcquisition:
    """Gestiona l'adquisició de dades amb NI-DAQmx amb gestió segura de recursos."""
    
    def __init__(self):
        """Inicialitza el sistema d'adquisició."""
        self.ai_task: Optional[nidaqmx.Task] = None
        self.do_task: Optional[nidaqmx.Task] = None
        self.monitor_ai_task: Optional[nidaqmx.Task] = None  # Tasca separada per monitorització
        self.is_running = False
        self.using_simulation = USING_MOCK
        
    def setup_tasks(self):
        """Configura les tasques DAQmx per entrada analògica i sortida digital."""
        try:
            # Netejar tasques existents primer
            self.cleanup()
            
            # Crear tasca d'entrada analògica per adquisició
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
            
            # Crear tasca separada per monitorització (lectura puntual)
            self.monitor_ai_task = nidaqmx.Task()
            self.monitor_ai_task.ai_channels.add_ai_voltage_chan(
                AI_CHANNELS,
                terminal_config=TerminalConfiguration.RSE,
                min_val=VOLTAGE_RANGE_MIN,
                max_val=VOLTAGE_RANGE_MAX
            )
            
            mode = "SIMULACIÓ" if self.using_simulation else "REAL"
            return True, f"Tasques configurades (Mode: {mode})"
            
        except Exception as e:
            self.cleanup()
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
        Llegeix mostres dels canals analògics durant adquisició.
        
        Args:
            num_samples: Nombre de mostres a llegir per canal
            
        Returns:
            Tupla (success, error_message, data)
        """
        try:
            if self.ai_task is None or not self.is_running:
                return False, "Adquisició no iniciada", None
            
            data = self.ai_task.read(
                number_of_samples_per_channel=num_samples,
                timeout=nidaqmx.constants.WAIT_INFINITELY
            )
            
            data_array = np.array(data)
            return True, "", data_array
            
        except Exception as e:
            return False, f"Error llegint mostres: {str(e)}", None
    
    def read_current_values(self) -> Tuple[bool, str, Optional[Tuple[float, float]]]:
        """
        Llegeix valors puntuals dels sensors per monitorització.
        Utilitza una tasca separada que no interfereix amb l'adquisició.
        
        Returns:
            Tupla (success, error_message, (voltage1, voltage2))
        """
        try:
            # Si estem en mode adquisició, no interferir
            if self.is_running:
                return False, "No es pot monitoritzar durant adquisició", None
            
            # Utilitzar la tasca de monitorització
            if self.monitor_ai_task is None:
                return False, "Tasca de monitorització no inicialitzada", None
            
            # Assegurar que els sensors estan activats
            if self.do_task is not None:
                num_channels = len(DO_CHANNELS)
                self.do_task.write([True] * num_channels)
            
            # Llegir una mostra de cada canal
            values = self.monitor_ai_task.read(number_of_samples_per_channel=1)
            
            # Convertir a tupla (voltage1, voltage2)
            # values pot ser [[v1], [v2]] o [v1, v2] segons el nombre de canals
            if isinstance(values, (list, tuple)):
                if len(values) >= 2:
                    # Si és llista de llistes, agafar primer element de cada
                    if isinstance(values[0], (list, tuple)):
                        voltage1 = float(values[0][0])
                        voltage2 = float(values[1][0])
                    else:
                        voltage1 = float(values[0])
                        voltage2 = float(values[1])
                else:
                    return False, "Format de dades inesperat (menys de 2 canals)", None
            elif isinstance(values, np.ndarray):
                if values.ndim == 2:
                    voltage1 = float(values[0][0])
                    voltage2 = float(values[1][0])
                else:
                    voltage1 = float(values[0]) if len(values) > 0 else 0.0
                    voltage2 = float(values[1]) if len(values) > 1 else 0.0
            else:
                return False, "Format de dades inesperat", None
            
            return True, "", (voltage1, voltage2)
            
        except Exception as e:
            return False, f"Error llegint valors actuals: {str(e)}", None
    
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
        """Neteja i tanca totes les tasques DAQmx de forma segura."""
        errors = []
        
        try:
            # Aturar adquisició si està corrent
            if self.is_running and self.ai_task is not None:
                try:
                    self.ai_task.stop()
                except:
                    pass
                self.is_running = False
            
            # Tancar tasca d'adquisició
            if self.ai_task is not None:
                try:
                    self.ai_task.close()
                except Exception as e:
                    errors.append(f"Error tancant ai_task: {e}")
                self.ai_task = None
            
            # Tancar tasca de monitorització
            if self.monitor_ai_task is not None:
                try:
                    self.monitor_ai_task.close()
                except Exception as e:
                    errors.append(f"Error tancant monitor_ai_task: {e}")
                self.monitor_ai_task = None
            
            # Desactivar sensors
            try:
                self.deactivate_sensors()
            except:
                pass
            
            # Tancar tasca de sortida digital
            if self.do_task is not None:
                try:
                    self.do_task.close()
                except Exception as e:
                    errors.append(f"Error tancant do_task: {e}")
                self.do_task = None
            
            if errors:
                return False, "; ".join(errors)
            return True, ""
            
        except Exception as e:
            return False, f"Error general en cleanup: {str(e)}"
    
    def __del__(self):
        """Destructor: assegurar que tot es tanca en eliminar l'objecte."""
        try:
            self.cleanup()
        except:
            pass
    
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
