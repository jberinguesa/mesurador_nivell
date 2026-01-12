"""
Classe específica per gestionar els sensors AWP-24-3
"""
from typing import Tuple
import numpy as np
from data.processor import DataProcessor


class AWP24Sensor:
    """Representa un sensor de nivell d'aigua AWP-24-3."""
    
    def __init__(self, sensor_id: int, name: str):
        """
        Inicialitza el sensor.
        
        Args:
            sensor_id: Identificador del sensor (0 o 1)
            name: Nom del sensor (ex: "Sensor #1")
        """
        self.sensor_id = sensor_id
        self.name = name
        self.data_processor = DataProcessor()
        
    def process_samples(self, samples: np.ndarray) -> float:
        """
        Processa les mostres del sensor i retorna la mitjana.
        
        Args:
            samples: Array de mostres de voltatge
            
        Returns:
            Voltatge mitjà en V
        """
        return self.data_processor.calculate_mean(samples)
    
    def validate_voltage(self, voltage: float, min_voltage: float = -10.0, 
                        max_voltage: float = 10.0) -> Tuple[bool, str]:
        """
        Valida que el voltatge estigui dins del rang esperat.
        
        Args:
            voltage: Voltatge a validar
            min_voltage: Voltatge mínim acceptable
            max_voltage: Voltatge màxim acceptable
            
        Returns:
            Tupla (is_valid, warning_message)
        """
        if voltage < min_voltage or voltage > max_voltage:
            return False, f"{self.name}: Voltatge fora de rang ({voltage:.3f} V)"
        
        return True, ""


class SensorManager:
    """Gestiona els dos sensors AWP-24-3."""
    
    def __init__(self):
        """Inicialitza el gestor de sensors."""
        self.sensors = [
            AWP24Sensor(0, "Sensor #1"),
            AWP24Sensor(1, "Sensor #2")
        ]
    
    def process_multi_channel_data(self, data: np.ndarray) -> Tuple[float, float]:
        """
        Processa les dades de tots els canals.
        
        Args:
            data: Array de forma (num_channels, num_samples)
            
        Returns:
            Tupla (voltage_sensor1, voltage_sensor2)
        """
        if data.shape[0] != 2:
            raise ValueError(f"S'esperaven 2 canals, rebuts {data.shape[0]}")
        
        voltage1 = self.sensors[0].process_samples(data[0])
        voltage2 = self.sensors[1].process_samples(data[1])
        
        return voltage1, voltage2
    
    def validate_readings(self, voltage1: float, voltage2: float) -> Tuple[bool, str]:
        """
        Valida les lectures de tots els sensors.
        
        Args:
            voltage1: Voltatge del sensor 1
            voltage2: Voltatge del sensor 2
            
        Returns:
            Tupla (all_valid, combined_warnings)
        """
        warnings = []
        all_valid = True
        
        valid1, msg1 = self.sensors[0].validate_voltage(voltage1)
        if not valid1:
            warnings.append(msg1)
            all_valid = False
        
        valid2, msg2 = self.sensors[1].validate_voltage(voltage2)
        if not valid2:
            warnings.append(msg2)
            all_valid = False
        
        return all_valid, "; ".join(warnings)
