"""
Sistema d'Adquisició de Nivell d'Aigua
Universitat de Girona - Departament de Física

Aplicació per adquirir dades de dos sensors AWP-24-3
connectats a un sistema NI cDAQ amb mòduls NI-9201 i NI-9472.

Author: JCM Technologies, SAU
Date: 2026
"""
import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """Punt d'entrada de l'aplicació."""
    app = QApplication(sys.argv)
    
    # Configurar estil de l'aplicació
    app.setStyle('Fusion')
    
    # Crear i mostrar finestra principal
    window = MainWindow()
    window.show()
    
    # Executar aplicació
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
