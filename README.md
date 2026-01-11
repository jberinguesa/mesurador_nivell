# Sistema d'Adquisició de Nivell d'Aigua

**Universitat de Girona - Departament de Física**

Aplicació d'escriptori per adquirir dades de dos sensors de nivell d'aigua Akamina AWP-24-3 connectats a un sistema NI cDAQ.

## 📋 Requisits del Sistema

### Hardware
- NI cDAQ-9174 (xassís CompactDAQ)
- NI-9201 (mòdul d'entrada analògica, 8 canals)
- NI-9472 (mòdul de sortida digital, 8 canals)
- 2x Sensor Akamina AWP-24-3

### Programari
- Windows 10/11
- Python 3.8 o superior
- NI-DAQmx Runtime (descarregar de ni.com)
- Driver NI-DAQmx instal·lat

## 🔧 Connexions Hardware

| Sensor      | Pin            | Connexió NI          |
|-------------|----------------|----------------------|
| AWP-24-3 #1 | F (Power High) | NI-9472 DO0         |
| AWP-24-3 #1 | E (Power Low)  | GND                 |
| AWP-24-3 #1 | B (Output High)| NI-9201 ai0         |
| AWP-24-3 #1 | C (Output Low) | GND                 |
| AWP-24-3 #2 | F (Power High) | NI-9472 DO1         |
| AWP-24-3 #2 | E (Power Low)  | GND                 |
| AWP-24-3 #2 | B (Output High)| NI-9201 ai1         |
| AWP-24-3 #2 | C (Output Low) | GND                 |

**Configuració:** Single-ended respecte massa

## 📦 Instal·lació

### 1. Configurar el Hardware amb NI MAX

Abans d'executar l'aplicació, configureu el hardware amb NI Measurement & Automation Explorer (MAX):

1. Obriu NI MAX
2. Localitzeu el dispositiu cDAQ (normalment `cDAQ1`)
3. Verifiqueu que els mòduls estan en els slots correctes:
   - Slot 1: NI-9201
   - Slot 2: NI-9472
4. Feu un Test Panel per verificar la connectivitat

### 2. Instal·lar Dependències Python

Obriu un terminal i navegueu al directori del projecte:

```bash
cd mesurador_nivell
pip install -r requirements.txt
```

Si teniu problemes amb `nidaqmx`, assegureu-vos que el NI-DAQmx Runtime està instal·lat.

### 3. Configurar els Noms de Dispositius

Si els vostres dispositius tenen noms diferents als predeterminats, editeu el fitxer `utils/config.py`:

```python
DEVICE_NAME = "cDAQ1"        # Canvieu si és diferent
AI_MODULE = "cDAQ1Mod1"      # Mòdul NI-9201
DO_MODULE = "cDAQ1Mod2"      # Mòdul NI-9472
```

## 🚀 Ús de l'Aplicació

### Executar el Programa

```bash
python main.py
```

### Interfície d'Usuari

L'aplicació té dues parts principals:

**Esquerra (Gràfica):**
- Mostra els voltatges dels dos sensors en temps real
- Sensor #1: Línia blava
- Sensor #2: Línia vermella
- Grid i llegenda activats

**Dreta (Controls):**
- **Botó Start:** Inicia l'adquisició
- **Botó Stop:** Atura l'adquisició
- **Botó Carregar mesura:** Carrega dades guardades prèviament
- **Període de mostreig:** Temps entre lectures (0.001 - 10.0 s)
- **Nom del fitxer:** Nom del fitxer Excel on es guardaran les dades

### Flux de Treball Típic

1. **Configurar paràmetres:**
   - Introduïu el període de mostreig desitjat (per defecte: 0.1 s)
   - El nom del fitxer s'auto-genera amb timestamp, però podeu canviar-lo

2. **Iniciar adquisició:**
   - Premeu el botó **Start**
   - Els sensors s'alimenten automàticament (DO0 i DO1)
   - Les dades comencen a visualitzar-se a la gràfica
   - Les dades es guarden automàticament al fitxer Excel

3. **Aturar adquisició:**
   - Premeu el botó **Stop**
   - Els sensors es desactiven
   - El fitxer es tanca correctament
   - La gràfica es manté visible

4. **Carregar dades anteriors:**
   - Premeu **Carregar mesura**
   - Seleccioneu un fitxer `.xlsx` prèviament guardat
   - Les dades es visualitzen a la gràfica

## 📊 Format de Dades

Les dades es guarden en format Excel (`.xlsx`) amb la següent estructura:

| time_seconds | voltage_sensor1 | voltage_sensor2 |
|--------------|-----------------|-----------------|
| 0.000        | 2.345          | 3.456          |
| 0.100        | 2.347          | 3.458          |
| 0.200        | 2.350          | 3.460          |
| ...          | ...            | ...            |

- `time_seconds`: Temps des de l'inici de la mesura (float)
- `voltage_sensor1`: Voltatge del sensor #1 en V (float)
- `voltage_sensor2`: Voltatge del sensor #2 en V (float)

## 🏗️ Estructura del Projecte

```
mesurador_nivell/
├── main.py                 # Punt d'entrada de l'aplicació
├── requirements.txt        # Dependències Python
├── README.md              # Aquest fitxer
├── gui/
│   ├── __init__.py
│   └── main_window.py     # Finestra principal PyQt5
├── daq/
│   ├── __init__.py
│   ├── acquisition.py     # Gestió de tasques DAQmx
│   └── sensor.py          # Lògica dels sensors AWP-24-3
├── data/
│   ├── __init__.py
│   ├── file_handler.py    # Lectura/escriptura Excel
│   └── processor.py       # Processament de dades
└── utils/
    ├── __init__.py
    ├── config.py          # Configuració del sistema
    └── validators.py      # Validació d'inputs
```

## ⚠️ Troubleshooting

### Error: "Dispositiu no trobat"
- Verifiqueu que el cDAQ està connectat i encès
- Obriu NI MAX i comproveu que el dispositiu és visible
- Comproveu que els noms a `utils/config.py` coincideixen amb NI MAX

### Error: "No s'han pogut configurar les tasques DAQmx"
- Assegureu-vos que cap altra aplicació està utilitzant el hardware
- Reinicieu el dispositiu cDAQ
- Verifiqueu els noms dels mòduls a `config.py`

### Error en instal·lar `nidaqmx`
- Descarregueu i instal·leu NI-DAQmx Runtime de ni.com
- Reinicieu l'ordinador després de la instal·lació
- Torneu a intentar `pip install nidaqmx`

### La gràfica no s'actualitza
- Comproveu que el període de mostreig no és massa gran
- Verifiqueu que els sensors estan correctament connectats
- Reviseu la consola per possibles errors

### Fitxer Excel no es crea
- Verifiqueu que teniu permisos d'escriptura al directori
- Comproveu que el nom del fitxer és vàlid
- Si el fitxer existeix, confirmeu que voleu sobreescriure'l

## 📝 Notes Tècniques

### Taxa de Mostreig
- **Hardware:** El sistema mostra a 1000 Hz (1 kHz) constantment
- **Període configurable:** Defineix cada quan es guarda la mitjana de les mostres
- Exemple: Període 0.1 s → Llegeix 100 mostres i en guarda la mitjana cada 0.1 s

### Gestió de la GUI
- L'adquisició s'executa amb QTimer per no bloquejar la interfície
- El flush del fitxer es fa cada 10 punts per optimitzar rendiment
- Les dades es guarden de forma segura fins i tot si l'aplicació es tanca inesperadament

### Validacions
- Període de mostreig: 0.001 - 10.0 segons
- Voltatges: ±10 V (fora de rang genera advertència)
- Format de fitxer: Només `.xlsx`

## 👥 Autors i Contacte

**Desenvolupat per:**
- JCM Technologies, SAU
- Departament de R&D

**Per a:**
- Universitat de Girona
- Departament de Física

**Data:** Gener 2026

## 📄 Llicència

Aquest programari ha estat desenvolupat específicament per a la Universitat de Girona.
Tots els drets reservats.
