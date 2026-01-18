"""
Validadors per inputs de l'usuari
"""
import os
from utils.config import MIN_SAMPLING_PERIOD, MAX_SAMPLING_PERIOD, FILE_EXTENSION


def validate_sampling_period(period: float) -> tuple[bool, str]:
    """
    Valida el període de mostreig introduït per l'usuari.
    
    Args:
        period: Període de mostreig en segons
        
    Returns:
        Tupla (is_valid, error_message)
    """
    if period < MIN_SAMPLING_PERIOD:
        return False, f"El període de mostreig ha de ser >= {MIN_SAMPLING_PERIOD} s"
    
    if period > MAX_SAMPLING_PERIOD:
        return False, f"El període de mostreig ha de ser <= {MAX_SAMPLING_PERIOD} s"
    
    return True, ""


def validate_filename(filename: str) -> tuple[bool, str]:
    """
    Valida el nom del fitxer introduït per l'usuari.
    
    Args:
        filename: Nom del fitxer
        
    Returns:
        Tupla (is_valid, error_message)
    """
    if not filename:
        return False, "El nom del fitxer no pot estar buit"
    
    if not filename.endswith(FILE_EXTENSION):
        return False, f"El fitxer ha de tenir extensió {FILE_EXTENSION}"
    
    # Comprovar caràcters invàlids per a noms de fitxer
    invalid_chars = '<>:"|?*'
    for char in invalid_chars:
        if char in filename:
            return False, f"El nom del fitxer conté caràcters invàlids: {char}"
    
    return True, ""


def check_file_exists(filepath: str) -> bool:
    """
    Comprova si un fitxer ja existeix.
    
    Args:
        filepath: Camí complet del fitxer
        
    Returns:
        True si el fitxer existeix, False altrament
    """
    return os.path.exists(filepath)
