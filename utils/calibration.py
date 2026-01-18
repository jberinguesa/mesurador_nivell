"""
Mòdul de calibratge per convertir voltatge a alçada d'aigua
"""
import json
import os
from typing import Optional, Tuple


class SensorCalibration:
    """Gestiona la calibració d'un sensor (voltatge → alçada)."""
    
    def __init__(self, sensor_id: int):
        """
        Inicialitza la calibració del sensor.
        
        Args:
            sensor_id: Identificador del sensor (0 o 1)
        """
        self.sensor_id = sensor_id
        # Punts de calibratge (voltatge, alçada)
        self.point1 = None  # (voltage, height)
        self.point2 = None  # (voltage, height)
        
    def set_calibration_points(self, v1: float, h1: float, v2: float, h2: float):
        """
        Estableix els punts de calibratge.
        
        Args:
            v1: Voltatge del punt 1
            h1: Alçada del punt 1 (cm)
            v2: Voltatge del punt 2
            h2: Alçada del punt 2 (cm)
        """
        self.point1 = (v1, h1)
        self.point2 = (v2, h2)
    
    def is_calibrated(self) -> bool:
        """Retorna True si el sensor està calibrat."""
        return self.point1 is not None and self.point2 is not None
    
    def voltage_to_height(self, voltage: float) -> Optional[float]:
        """
        Converteix voltatge a alçada usant interpolació lineal.
        
        Args:
            voltage: Voltatge llegit del sensor
            
        Returns:
            Alçada en cm, o None si no està calibrat
        """
        if not self.is_calibrated():
            return None
        
        v1, h1 = self.point1
        v2, h2 = self.point2
        
        # Interpolació lineal: h = h1 + (h2 - h1) * (v - v1) / (v2 - v1)
        if abs(v2 - v1) < 0.001:  # Evitar divisió per zero
            return h1
        
        height = h1 + (h2 - h1) * (voltage - v1) / (v2 - v1)
        return height
    
    def to_dict(self) -> dict:
        """Exporta la calibració a diccionari."""
        return {
            'sensor_id': self.sensor_id,
            'point1': self.point1,
            'point2': self.point2
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'SensorCalibration':
        """Crea una calibració des d'un diccionari."""
        calib = SensorCalibration(data['sensor_id'])
        calib.point1 = tuple(data['point1']) if data['point1'] else None
        calib.point2 = tuple(data['point2']) if data['point2'] else None
        return calib


class CalibrationManager:
    """Gestiona les calibracions de tots els sensors."""
    
    CALIBRATION_FILE = "sensor_calibration.json"
    
    # Valors per defecte: -2V = 0cm, +2V = 5cm
    DEFAULT_V1 = -2.0
    DEFAULT_H1 = 0.0
    DEFAULT_V2 = 2.0
    DEFAULT_H2 = 5.0
    
    def __init__(self):
        """Inicialitza el gestor de calibracions."""
        self.calibrations = {
            0: SensorCalibration(0),
            1: SensorCalibration(1)
        }
        self.load()
        
        # Si no hi ha calibracions carregades, aplicar valors per defecte
        if not self.calibrations[0].is_calibrated():
            self.set_calibration(0, self.DEFAULT_V1, self.DEFAULT_H1, 
                               self.DEFAULT_V2, self.DEFAULT_H2)
        if not self.calibrations[1].is_calibrated():
            self.set_calibration(1, self.DEFAULT_V1, self.DEFAULT_H1, 
                               self.DEFAULT_V2, self.DEFAULT_H2)
    
    def get_calibration(self, sensor_id: int) -> SensorCalibration:
        """Obté la calibració d'un sensor."""
        return self.calibrations[sensor_id]
    
    def set_calibration(self, sensor_id: int, v1: float, h1: float, v2: float, h2: float):
        """Estableix la calibració d'un sensor."""
        self.calibrations[sensor_id].set_calibration_points(v1, h1, v2, h2)
        self.save()
    
    def is_sensor_calibrated(self, sensor_id: int) -> bool:
        """Comprova si un sensor està calibrat."""
        return self.calibrations[sensor_id].is_calibrated()
    
    def are_all_calibrated(self) -> bool:
        """Comprova si tots els sensors estan calibrats."""
        return all(cal.is_calibrated() for cal in self.calibrations.values())
    
    def voltage_to_height(self, sensor_id: int, voltage: float) -> Optional[float]:
        """Converteix voltatge a alçada per un sensor."""
        return self.calibrations[sensor_id].voltage_to_height(voltage)
    
    def save(self):
        """Guarda les calibracions a fitxer JSON."""
        try:
            data = {
                'calibrations': [cal.to_dict() for cal in self.calibrations.values()]
            }
            with open(self.CALIBRATION_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error guardant calibracions: {e}")
    
    def load(self):
        """Carrega les calibracions des de fitxer JSON."""
        try:
            if os.path.exists(self.CALIBRATION_FILE):
                with open(self.CALIBRATION_FILE, 'r') as f:
                    data = json.load(f)
                for cal_data in data['calibrations']:
                    cal = SensorCalibration.from_dict(cal_data)
                    self.calibrations[cal.sensor_id] = cal
        except Exception as e:
            print(f"Error carregant calibracions: {e}")
    
    def reset(self):
        """Reseteja totes les calibracions."""
        self.calibrations = {
            0: SensorCalibration(0),
            1: SensorCalibration(1)
        }
        if os.path.exists(self.CALIBRATION_FILE):
            os.remove(self.CALIBRATION_FILE)
