"""
Gestor de fitxers Excel per emmagatzemar i carregar dades
Amb suport per columnes d'alçada
"""
import pandas as pd
from typing import Optional


class FileHandler:
    """Gestiona l'escriptura i lectura de fitxers Excel amb dades d'adquisició."""
    
    def __init__(self, filepath: str):
        """
        Inicialitza el gestor de fitxers.
        
        Args:
            filepath: Camí complet del fitxer Excel
        """
        self.filepath = filepath
        self.data_buffer = []
        
    def create_file(self):
        """Crea un nou fitxer Excel amb les capçaleres adequades."""
        df = pd.DataFrame(columns=[
            'time_seconds', 
            'voltage_sensor1', 
            'voltage_sensor2',
            'height_sensor1',
            'height_sensor2'
        ])
        # Especificar dtypes per evitar warnings
        df = df.astype({
            'time_seconds': 'float64',
            'voltage_sensor1': 'float64',
            'voltage_sensor2': 'float64',
            'height_sensor1': 'float64',
            'height_sensor2': 'float64'
        })
        df.to_excel(self.filepath, index=False, engine='openpyxl')
        
    def append_data(self, time: float, voltage1: float, voltage2: float, 
                    height1: Optional[float] = None, height2: Optional[float] = None):
        """
        Afegeix una nova fila de dades al buffer.
        
        Args:
            time: Temps en segons
            voltage1: Voltatge del sensor 1
            voltage2: Voltatge del sensor 2
            height1: Alçada del sensor 1 (cm) - opcional
            height2: Alçada del sensor 2 (cm) - opcional
        """
        self.data_buffer.append({
            'time_seconds': time,
            'voltage_sensor1': voltage1,
            'voltage_sensor2': voltage2,
            'height_sensor1': height1 if height1 is not None else float('nan'),
            'height_sensor2': height2 if height2 is not None else float('nan')
        })
        
    def flush_to_file(self):
        """Escriu el buffer de dades al fitxer Excel."""
        if not self.data_buffer:
            return
        
        # Crear DataFrame amb noves dades
        df_new = pd.DataFrame(self.data_buffer)
        
        # Llegir fitxer existent
        try:
            df_existing = pd.read_excel(self.filepath, engine='openpyxl')
            
            # Si el fitxer existent està buit, usar només les noves dades
            if df_existing.empty:
                df_combined = df_new
            else:
                # Concatenar amb copy=False per millor rendiment
                df_combined = pd.concat([df_existing, df_new], ignore_index=True, copy=False)
                
        except FileNotFoundError:
            # Si el fitxer no existeix, usar només les noves dades
            df_combined = df_new
        
        # Assegurar que els tipus de dades són correctes
        df_combined = df_combined.astype({
            'time_seconds': 'float64',
            'voltage_sensor1': 'float64',
            'voltage_sensor2': 'float64',
            'height_sensor1': 'float64',
            'height_sensor2': 'float64'
        })
        
        # Guardar
        df_combined.to_excel(self.filepath, index=False, engine='openpyxl')
        
        # Netejar buffer
        self.data_buffer.clear()
        
    def close(self):
        """Tanca el fitxer i assegura que totes les dades estan guardades."""
        self.flush_to_file()
        
    @staticmethod
    def load_file(filepath: str) -> Optional[pd.DataFrame]:
        """
        Carrega dades d'un fitxer Excel existent.
        
        Args:
            filepath: Camí complet del fitxer Excel
            
        Returns:
            DataFrame amb les dades o None si hi ha error
        """
        try:
            df = pd.read_excel(filepath, engine='openpyxl')
            
            # Validar columnes obligatòries
            required_columns = ['time_seconds', 'voltage_sensor1', 'voltage_sensor2']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"El fitxer ha de contenir les columnes: {required_columns}")
            
            # Les columnes d'alçada són opcionals (compatibilitat amb fitxers antics)
            if 'height_sensor1' not in df.columns:
                df['height_sensor1'] = float('nan')
            if 'height_sensor2' not in df.columns:
                df['height_sensor2'] = float('nan')
            
            return df
            
        except Exception as e:
            print(f"Error carregant fitxer: {e}")
            return None
