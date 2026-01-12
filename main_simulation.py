"""
Sistema d'Adquisició de Nivell d'Aigua - MODE SIMULACIÓ
Universitat de Girona - Departament de Física

Aquesta versió executa el programa amb dades sintètiques,
sense necessitat de hardware real.

Útil per:
- Testejar la GUI
- Verificar funcionalitat
- Desenvolupament sense hardware
- Demostració

Author: JCM Technologies, SAU
Date: 2026
"""
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

# IMPORTANT: Activar mode simulació ABANS d'importar altres mòduls
from simulation import enable_simulation
enable_simulation()

# Ara podem importar la finestra principal
# (que internament usarà el mock de DAQmx)
from gui.main_window import MainWindow


def show_simulation_notice():
    """Mostra un avís que el programa està en mode simulació."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Mode Simulació")
    msg.setText("🎭 Mode Simulació Activat")
    msg.setInformativeText(
        "Aquest programa s'executa amb dades sintètiques.\n\n"
        "Característiques:\n"
        "• No es necessita hardware real (cDAQ, sensors)\n"
        "• Les dades són generades artificialment\n"
        "• Permet testejar tota la funcionalitat\n"
        "• Els fitxers guardats són vàlids\n\n"
        "Per executar amb hardware real, usa: python main.py"
    )
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def main():
    """Punt d'entrada de l'aplicació en mode simulació."""
    print("=" * 60)
    print("🎭 SISTEMA D'ADQUISICIÓ - MODE SIMULACIÓ")
    print("=" * 60)
    print()
    print("✓ Mode simulació activat")
    print("✓ No es necessita hardware real")
    print("✓ Les dades són sintètiques i realistes")
    print()
    print("Característiques de la simulació:")
    print("  - Dos sensors virtuals (ai0, ai1)")
    print("  - Voltatges base: ~2.5V i ~3.5V")
    print("  - Oscil·lacions simulant variacions del nivell")
    print("  - Soroll gaussià realista")
    print("  - Deriva lenta en el temps")
    print()
    print("=" * 60)
    print()
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Mostrar avís de mode simulació
    show_simulation_notice()
    
    # Crear i mostrar finestra principal
    window = MainWindow()
    
    # Afegir indicador visual al títol
    window.setWindowTitle(window.windowTitle() + " [SIMULACIÓ]")
    
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
