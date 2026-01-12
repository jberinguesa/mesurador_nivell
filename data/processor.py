"""
Processador de dades per càlculs i transformacions
"""
import numpy as np
from typing import List


class DataProcessor:
    """Processa les dades adquirides dels sensors."""
    
    @staticmethod
    def calculate_mean(samples: np.ndarray) -> float:
        """
        Calcula la mitjana d'un conjunt de mostres.
        
        Args:
            samples: Array de mostres
            
        Returns:
            Mitjana de les mostres
        """
        if len(samples) == 0:
            return 0.0
        return float(np.mean(samples))
    
    @staticmethod
    def calculate_statistics(data: List[float]) -> dict:
        """
        Calcula estadístiques bàsiques d'un conjunt de dades.
        
        Args:
            data: Llista de valors
            
        Returns:
            Diccionari amb estadístiques (mean, min, max, std)
        """
        if not data:
            return {'mean': 0.0, 'min': 0.0, 'max': 0.0, 'std': 0.0}
        
        data_array = np.array(data)
        return {
            'mean': float(np.mean(data_array)),
            'min': float(np.min(data_array)),
            'max': float(np.max(data_array)),
            'std': float(np.std(data_array))
        }
