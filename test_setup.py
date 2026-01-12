"""
Script de test per verificar la configuració del hardware
Universitat de Girona - Departament de Física
"""
import sys


def test_imports():
    """Comprova que totes les llibreries necessàries estan instal·lades."""
    print("=" * 60)
    print("TEST 1: Comprovant imports...")
    print("=" * 60)
    
    modules = {
        'nidaqmx': 'Driver NI-DAQmx',
        'PyQt5': 'Framework GUI',
        'pyqtgraph': 'Gràfiques en temps real',
        'pandas': 'Processament de dades',
        'numpy': 'Càlculs numèrics',
        'openpyxl': 'Gestió de fitxers Excel'
    }
    
    all_ok = True
    for module_name, description in modules.items():
        try:
            __import__(module_name)
            print(f"✓ {module_name:15} - {description}")
        except ImportError:
            print(f"✗ {module_name:15} - {description} [NO INSTAL·LAT]")
            all_ok = False
    
    print()
    return all_ok


def test_daqmx():
    """Comprova la disponibilitat del hardware DAQmx."""
    print("=" * 60)
    print("TEST 2: Comprovant hardware DAQmx...")
    print("=" * 60)
    
    try:
        import nidaqmx.system
        
        system = nidaqmx.system.System.local()
        devices = list(system.devices)
        
        if not devices:
            print("✗ No s'han trobat dispositius DAQmx")
            print("  Verifiqueu:")
            print("  - Que el cDAQ està connectat i encès")
            print("  - Que NI-DAQmx Runtime està instal·lat")
            print("  - Que els dispositius són visibles a NI MAX")
            return False
        
        print(f"✓ Trobats {len(devices)} dispositiu(s) DAQmx:")
        for device in devices:
            print(f"  - {device.name}: {device.product_type}")
            
        print()
        return True
        
    except ImportError:
        print("✗ nidaqmx no està instal·lat")
        print("  Instal·leu NI-DAQmx Runtime i executeu:")
        print("  pip install nidaqmx")
        return False
    except Exception as e:
        print(f"✗ Error comprovant DAQmx: {e}")
        return False


def test_config():
    """Comprova la configuració del sistema."""
    print("=" * 60)
    print("TEST 3: Comprovant configuració...")
    print("=" * 60)
    
    try:
        from utils import config
        
        print(f"✓ Dispositiu: {config.DEVICE_NAME}")
        print(f"✓ Mòdul AI: {config.AI_MODULE}")
        print(f"✓ Mòdul DO: {config.DO_MODULE}")
        print(f"✓ Canals AI: {config.AI_CHANNELS}")
        print(f"✓ Canals DO: {config.DO_CHANNELS}")
        print(f"✓ Taxa de mostreig: {config.SAMPLE_RATE} Hz")
        print()
        return True
        
    except Exception as e:
        print(f"✗ Error carregant configuració: {e}")
        return False


def test_device_match():
    """Comprova que el dispositiu configurat existeix."""
    print("=" * 60)
    print("TEST 4: Verificant dispositiu configurat...")
    print("=" * 60)
    
    try:
        import nidaqmx.system
        from utils import config
        
        system = nidaqmx.system.System.local()
        device_names = [dev.name for dev in system.devices]
        
        if config.DEVICE_NAME in device_names:
            print(f"✓ Dispositiu '{config.DEVICE_NAME}' trobat i configurat correctament")
            print()
            return True
        else:
            print(f"✗ Dispositiu '{config.DEVICE_NAME}' NO trobat")
            print(f"  Dispositius disponibles: {device_names}")
            print(f"  Editeu utils/config.py i canvieu DEVICE_NAME")
            print()
            return False
            
    except Exception as e:
        print(f"✗ Error verificant dispositiu: {e}")
        print()
        return False


def main():
    """Executa tots els tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  SISTEMA D'ADQUISICIÓ DE NIVELL D'AIGUA - TEST".center(58) + "║")
    print("║" + "  Universitat de Girona - Departament de Física".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: DAQmx hardware
    results.append(("Hardware DAQmx", test_daqmx()))
    
    # Test 3: Configuració
    results.append(("Configuració", test_config()))
    
    # Test 4: Dispositiu configurat
    results.append(("Dispositiu configurat", test_device_match()))
    
    # Resum
    print("=" * 60)
    print("RESUM DELS TESTS")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:25} {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("✓ TOTS ELS TESTS HAN PASSAT!")
        print("  El sistema està preparat per executar l'aplicació.")
        print("  Executeu: python main.py")
    else:
        print("✗ ALGUNS TESTS HAN FALLAT")
        print("  Reviseu els errors anteriors abans d'executar l'aplicació.")
    
    print()
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
