"""
Tests automàtics per verificar el funcionament del sistema
en mode simulació.

Executa: python test_simulation.py
"""
import sys
import os
import time
import numpy as np
from datetime import datetime

# Activar mode simulació
from simulation import enable_simulation
enable_simulation()

# Importar components del sistema
from daq.acquisition import DAQAcquisition
from daq.sensor import SensorManager
from data.file_handler import FileHandler
from data.processor import DataProcessor
from utils.validators import validate_sampling_period, validate_filename
from utils.config import DEVICE_NAME


class TestResults:
    """Gestor de resultats dels tests."""
    
    def __init__(self):
        self.tests = []
        self.passed = 0
        self.failed = 0
    
    def add_test(self, name, passed, message=""):
        """Afegeix un resultat de test."""
        self.tests.append({
            'name': name,
            'passed': passed,
            'message': message
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        """Imprimeix el resum dels tests."""
        print("\n" + "=" * 70)
        print("RESUM DELS TESTS")
        print("=" * 70)
        
        for test in self.tests:
            status = "✓ PASS" if test['passed'] else "✗ FAIL"
            print(f"{test['name']:45} {status}")
            if test['message'] and not test['passed']:
                print(f"  → {test['message']}")
        
        print("=" * 70)
        print(f"Total: {len(self.tests)} tests")
        print(f"✓ Passats: {self.passed}")
        print(f"✗ Fallats: {self.failed}")
        print("=" * 70)
        
        if self.failed == 0:
            print("🎉 TOTS ELS TESTS HAN PASSAT!")
        else:
            print(f"⚠️  {self.failed} test(s) han fallat")
        
        return self.failed == 0


def test_validators():
    """Test dels validadors."""
    results = TestResults()
    
    print("\n📝 TEST 1: Validadors")
    print("-" * 70)
    
    # Test període de mostreig vàlid
    valid, msg = validate_sampling_period(0.1)
    results.add_test("Validador: període vàlid (0.1 s)", valid)
    
    # Test període massa petit
    valid, msg = validate_sampling_period(0.0001)
    results.add_test("Validador: període massa petit", not valid)
    
    # Test període massa gran
    valid, msg = validate_sampling_period(20.0)
    results.add_test("Validador: període massa gran", not valid)
    
    # Test nom de fitxer vàlid
    valid, msg = validate_filename("test.xlsx")
    results.add_test("Validador: nom de fitxer vàlid", valid)
    
    # Test nom de fitxer sense extensió
    valid, msg = validate_filename("test.txt")
    results.add_test("Validador: extensió incorrecta", not valid)
    
    # Test nom de fitxer buit
    valid, msg = validate_filename("")
    results.add_test("Validador: nom buit", not valid)
    
    return results


def test_data_processor():
    """Test del processador de dades."""
    results = TestResults()
    
    print("\n🔢 TEST 2: Processador de Dades")
    print("-" * 70)
    
    processor = DataProcessor()
    
    # Test càlcul de mitjana
    samples = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    mean = processor.calculate_mean(samples)
    expected = 3.0
    results.add_test(
        "Processador: càlcul mitjana",
        abs(mean - expected) < 0.001,
        f"Esperat {expected}, obtingut {mean}"
    )
    
    # Test estadístiques
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    stats = processor.calculate_statistics(data)
    results.add_test(
        "Processador: estadístiques (mean)",
        abs(stats['mean'] - 3.0) < 0.001
    )
    results.add_test(
        "Processador: estadístiques (min)",
        stats['min'] == 1.0
    )
    results.add_test(
        "Processador: estadístiques (max)",
        stats['max'] == 5.0
    )
    
    return results


def test_daq_simulation():
    """Test del sistema DAQmx simulat."""
    results = TestResults()
    
    print("\n🔌 TEST 3: Sistema DAQmx Simulat")
    print("-" * 70)
    
    daq = DAQAcquisition()
    
    # Test que està en mode simulació
    results.add_test(
        "DAQ: mode simulació activat",
        daq.using_simulation,
        "S'esperava mode simulació"
    )
    
    # Test configuració de tasques
    success, msg = daq.setup_tasks()
    results.add_test("DAQ: configurar tasques", success, msg)
    
    # Test activació de sensors
    success, msg = daq.activate_sensors()
    results.add_test("DAQ: activar sensors", success, msg)
    
    # Test iniciar adquisició
    success, msg = daq.start_acquisition()
    results.add_test("DAQ: iniciar adquisició", success, msg)
    
    # Test lectura de mostres
    success, msg, data = daq.read_samples(100)
    results.add_test("DAQ: llegir mostres", success and data is not None, msg)
    
    if data is not None:
        # Verificar forma de les dades
        expected_shape = (2, 100)  # 2 canals, 100 mostres
        results.add_test(
            "DAQ: forma de dades correcta",
            data.shape == expected_shape,
            f"Esperat {expected_shape}, obtingut {data.shape}"
        )
        
        # Verificar que els valors estan dins del rang
        in_range = np.all((data >= -10) & (data <= 10))
        results.add_test("DAQ: valors dins del rang ±10V", in_range)
    
    # Test aturar adquisició
    success, msg = daq.stop_acquisition()
    results.add_test("DAQ: aturar adquisició", success, msg)
    
    # Test neteja
    success, msg = daq.cleanup()
    results.add_test("DAQ: neteja de tasques", success, msg)
    
    return results


def test_sensor_manager():
    """Test del gestor de sensors."""
    results = TestResults()
    
    print("\n📡 TEST 4: Gestor de Sensors")
    print("-" * 70)
    
    manager = SensorManager()
    
    # Test processament de dades multicanal
    # Crear dades simulades (2 canals, 50 mostres cada un)
    data = np.random.randn(2, 50) * 0.1 + np.array([[2.5], [3.5]])
    
    try:
        voltage1, voltage2 = manager.process_multi_channel_data(data)
        results.add_test("Sensors: processar dades multicanal", True)
        
        # Verificar que els voltatges són raonables
        v1_ok = 2.0 < voltage1 < 3.0
        v2_ok = 3.0 < voltage2 < 4.0
        results.add_test(
            "Sensors: voltatges dins del rang esperat",
            v1_ok and v2_ok,
            f"V1={voltage1:.3f}, V2={voltage2:.3f}"
        )
        
        # Test validació de lectures
        valid, msg = manager.validate_readings(voltage1, voltage2)
        results.add_test("Sensors: validar lectures", valid, msg)
        
    except Exception as e:
        results.add_test("Sensors: processar dades", False, str(e))
    
    return results


def test_file_handler():
    """Test del gestor de fitxers."""
    results = TestResults()
    
    print("\n💾 TEST 5: Gestor de Fitxers")
    print("-" * 70)
    
    # Nom de fitxer temporal
    test_filename = "test_simulation_data.xlsx"
    
    try:
        # Test crear fitxer
        handler = FileHandler(test_filename)
        handler.create_file()
        results.add_test("Fitxer: crear fitxer Excel", os.path.exists(test_filename))
        
        # Test afegir dades
        for i in range(10):
            handler.append_data(i * 0.1, 2.5 + i * 0.01, 3.5 + i * 0.01)
        results.add_test("Fitxer: afegir dades al buffer", len(handler.data_buffer) == 10)
        
        # Test guardar dades
        handler.flush_to_file()
        results.add_test("Fitxer: guardar dades", len(handler.data_buffer) == 0)
        
        # Test tancar fitxer
        handler.close()
        results.add_test("Fitxer: tancar correctament", True)
        
        # Test carregar fitxer
        df = FileHandler.load_file(test_filename)
        results.add_test("Fitxer: carregar dades", df is not None)
        
        if df is not None:
            # Verificar columnes
            expected_cols = ['time_seconds', 'voltage_sensor1', 'voltage_sensor2']
            has_cols = all(col in df.columns for col in expected_cols)
            results.add_test("Fitxer: columnes correctes", has_cols)
            
            # Verificar nombre de files
            results.add_test("Fitxer: nombre de files", len(df) == 10)
        
        # Netejar fitxer de test
        if os.path.exists(test_filename):
            os.remove(test_filename)
            results.add_test("Fitxer: neteja correcta", True)
        
    except Exception as e:
        results.add_test("Fitxer: error general", False, str(e))
    
    return results


def test_full_acquisition_cycle():
    """Test d'un cicle complet d'adquisició."""
    results = TestResults()
    
    print("\n🔄 TEST 6: Cicle Complet d'Adquisició")
    print("-" * 70)
    
    test_filename = "test_full_cycle.xlsx"
    
    try:
        # Inicialitzar components
        daq = DAQAcquisition()
        manager = SensorManager()
        handler = FileHandler(test_filename)
        
        # Configurar
        success, msg = daq.setup_tasks()
        results.add_test("Cicle: configurar DAQ", success, msg)
        
        success, msg = daq.activate_sensors()
        results.add_test("Cicle: activar sensors", success, msg)
        
        handler.create_file()
        results.add_test("Cicle: crear fitxer", True)
        
        # Iniciar adquisició
        success, msg = daq.start_acquisition()
        results.add_test("Cicle: iniciar", success, msg)
        
        # Simular 5 cicles d'adquisició
        for i in range(5):
            # Llegir mostres
            success, msg, data = daq.read_samples(100)
            if not success or data is None:
                results.add_test(f"Cicle: lectura {i+1}", False, msg)
                break
            
            # Processar
            voltage1, voltage2 = manager.process_multi_channel_data(data)
            
            # Guardar
            handler.append_data(i * 0.1, voltage1, voltage2)
            
            time.sleep(0.01)  # Petit delay
        
        results.add_test("Cicle: 5 lectures completes", i == 4)
        
        # Tancar
        handler.flush_to_file()
        handler.close()
        daq.stop_acquisition()
        daq.cleanup()
        
        results.add_test("Cicle: tancar correctament", True)
        
        # Verificar fitxer final
        df = FileHandler.load_file(test_filename)
        results.add_test("Cicle: fitxer final vàlid", df is not None and len(df) == 5)
        
        # Netejar
        if os.path.exists(test_filename):
            os.remove(test_filename)
        
    except Exception as e:
        results.add_test("Cicle: error", False, str(e))
    
    return results


def main():
    """Executa tots els tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  TESTS AUTOMÀTICS - MODE SIMULACIÓ".center(68) + "║")
    print("║" + "  Universitat de Girona - Departament de Física".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Executar tots els tests
    all_results = []
    
    all_results.append(test_validators())
    all_results.append(test_data_processor())
    all_results.append(test_daq_simulation())
    all_results.append(test_sensor_manager())
    all_results.append(test_file_handler())
    all_results.append(test_full_acquisition_cycle())
    
    # Combinar resultats
    final_results = TestResults()
    for result_set in all_results:
        final_results.passed += result_set.passed
        final_results.failed += result_set.failed
        final_results.tests.extend(result_set.tests)
    
    # Mostrar resum final
    all_passed = final_results.print_summary()
    
    print()
    if all_passed:
        print("✅ El sistema està llest per usar!")
        print("   Pots executar: python main_simulation.py")
    else:
        print("❌ Alguns tests han fallat. Revisa els errors anteriors.")
    print()
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
