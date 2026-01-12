"""
Gestor de fitxers Excel per emmagatzemar i carregar dades
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
        df = pd.DataFrame(columns=['time_seconds', 'voltage_sensor1', 'voltage_sensor2'])
        df.to_excel(self.filepath, index=False, engine='openpyxl')
        
    def append_data(self, time: float, voltage1: float, voltage2: float):
        """
        Afegeix una nova fila de dades al buffer.
        
        Args:
            time: Temps en segons
            voltage1: Voltatge del sensor 1
            voltage2: Voltatge del sensor 2
        """
        self.data_buffer.append({
            'time_seconds': time,
            'voltage_sensor1': voltage1,
            'voltage_sensor2': voltage2
        })
        
    def flush_to_file(self):
        """Escriu el buffer de dades al fitxer Excel."""
        if not self.data_buffer:
            return
            
        # Llegir fitxer existent
        try:
            df_existing = pd.read_excel(self.filepath, engine='openpyxl')
        except FileNotFoundError:
            df_existing = pd.DataFrame(columns=['time_seconds', 'voltage_sensor1', 'voltage_sensor2'])
        
        # Afegir noves dades
        df_new = pd.DataFrame(self.data_buffer)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        
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
            
            # Validar columnes
            required_columns = ['time_seconds', 'voltage_sensor1', 'voltage_sensor2']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"El fitxer ha de contenir les columnes: {required_columns}")
            
            return df
            
        except Exception as e:
            print(f"Error carregant fitxer: {e}")
            return None
