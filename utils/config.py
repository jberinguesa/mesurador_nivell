"""
Configuració del sistema d'adquisició de nivell d'aigua
Universitat de Girona - Departament de Física
"""

# Noms de dispositius DAQmx (verificar amb NI MAX)
DEVICE_NAME = "cDAQ1"
AI_MODULE = "cDAQ1Mod2"  # NI-9201 (Analog Input) al Slot 2
DO_MODULE = "cDAQ1Mod1"  # NI-9472 (Digital Output) al Slot 1

# Canals d'entrada analògica
AI_CHANNELS = "cDAQ1Mod2/ai0:1"  # Llegir ai0 i ai1 del Mod2
AI_CHANNEL_NAMES = ["Sensor #1", "Sensor #2"]

# Canals de sortida digital
DO_CHANNELS = ["cDAQ1Mod1/port0/line0", "cDAQ1Mod1/port0/line1"]  # DO0, DO1 del Mod1

# Configuració d'adquisició
VOLTAGE_RANGE_MIN = -10.0  # V
VOLTAGE_RANGE_MAX = 10.0   # V
SAMPLE_RATE = 1000         # Hz (taxa de mostreig hardware)
BUFFER_SIZE = 100000       # samples per buffer (augmentat per evitar overflow)

# Configuració de la interfície
DEFAULT_SAMPLING_PERIOD = 0.1  # segons
MIN_SAMPLING_PERIOD = 0.001    # segons
MAX_SAMPLING_PERIOD = 10.0     # segons
PLOT_UPDATE_INTERVAL = 10      # Actualitzar gràfica cada N mostres (més alt = menys càrrega)

# Configuració de colors per a la gràfica
PLOT_COLORS = ['#4A90E2', '#E24A4A']  # Blau, Vermell

# Temps d'estabilització del sensor
SENSOR_STABILIZATION_TIME = 0.1  # segons

# Configuració de fitxers
DEFAULT_FILENAME_PATTERN = "mesura_%Y%m%d_%H%M%S.xlsx"
FILE_EXTENSION = ".xlsx"

# Títols i etiquetes
WINDOW_TITLE = "Sistema d'Adquisició de Nivell d'Aigua - UdG"
INSTITUTION_FOOTER = "Departament de Física · Universitat de Girona"
