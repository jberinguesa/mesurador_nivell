# Especificacions del Sistema d'Adquisició de Nivell d'Aigua

## 1. Objectiu

Desenvolupar una aplicació d'escriptori que permeti:
- Llegir en temps real el senyal de **dos sensors de nivell d'aigua AWP-24-3** connectats a un NI-9201 (ai0 i ai1).
- Visualitzar els dos senyals de manera contínua en una **mateixa gràfica temporal amb colors diferents**.
- Emmagatzemar les dades dels dos sensors en un fitxer durant l'adquisició.
- Carregar i visualitzar mesures prèviament guardades.
El sistema ha de permetre iniciar i aturar la mesura de manera interactiva.

## 2. Hardware

-   **NI cDAQ-9174**: Xassís CompactDAQ amb 4 slots
-   **NI-9201**: Mòdul d'entrada analògica (8 canals, ±10 V)
-   **NI-9472**: Mòdul de sortida digital (8 canals, 24V sink/source)
-   **Sensor Akamina AWP-24-3 #1**: Sensor de nivell d'aigua (sortida analògica 4-20 mA o 0-10 V)
-   **Sensor Akamina AWP-24-3 #2**: Sensor de nivell d'aigua (sortida analògica 4-20 mA o 0-10 V)

## 3. Connexions

| Sensor            | Pin               | Mòdul NI      | Descripció                    |
|-------------------|-------------------|---------------|-------------------------------|
| AWP-24-3 #1       | F (Power High)    | NI-9472 DO0   | Alimentació positiva (+24V)   |
| AWP-24-3 #1       | E (Power Low)     | GND           | Alimentació negativa (GND)    |
| AWP-24-3 #1       | B (Output High)   | NI-9201 ai0   | Senyal de sortida analògica   |
| AWP-24-3 #1       | C (Output Low)    | GND           | Referència de senyal (GND)    |
| AWP-24-3 #2       | F (Power High)    | NI-9472 DO1   | Alimentació positiva (+24V)   |
| AWP-24-3 #2       | E (Power Low)     | GND           | Alimentació negativa (GND)    |
| AWP-24-3 #2       | B (Output High)   | NI-9201 ai1   | Senyal de sortida analògica   |
| AWP-24-3 #2       | C (Output Low)    | GND           | Referència de senyal (GND)    |

**Configuració de mesura**: Single-ended respecte massa als canals ai0 i ai1 del NI-9201.

## 4. Programari

### 4.1 Tecnologies

- **Llenguatge**: Python 3.8 o superior
- **Driver**: NI-DAQmx (instal·lat al sistema)
- **Sistema operatiu**: Windows 10/11

### 4.2 Llibreries Python requerides

```
nidaqmx>=0.6.5          # Driver Python per NI-DAQmx
PyQt5>=5.15.0           # Framework GUI
pyqtgraph>=0.12.0       # Gràfiques en temps real
openpyxl>=3.0.0         # Escriptura/lectura de fitxers Excel
pandas>=1.3.0           # Gestió de dades
```

**Alternatives acceptables**:
- PySide6 en lloc de PyQt5
- matplotlib en lloc de pyqtgraph (però pyqtgraph és preferible per temps real)

### 4.3 Configuració DAQmx

- **Canals d'entrada analògica**: `cDAQ1Mod1/ai0:1` (llegir ai0 i ai1 simultàniament)
- **Rang de voltatge**: ±10 V (per ambdós canals)
- **Mode d'adquisició**: Continuous sampling
- **Taxa de mostreig hardware**: 1000 Hz (1 kHz) per canal
- **Buffers**: 10000 samples per buffer (per cada canal)
- **Canals de sortida digital**: 
  - `cDAQ1Mod2/port0/line0` (DO0) - Alimentació sensor #1
  - `cDAQ1Mod2/port0/line1` (DO1) - Alimentació sensor #2

**Nota**: El període de mostreig configurable per l'usuari defineix cada quan es guarda una mostra, però el hardware sempre mostra a 1 kHz i fa la mitjana dels valors dins del període per cada canal.

## 5. Interfície gràfica

La finestra principal està dividida en dues parts:

### 5.1 Esquerra (2/3 de l'amplada)

-   **Gràfica temporal** (pyqtgraph PlotWidget)
    -   Eix X: Temps (s) - Des de 0 fins al temps transcorregut
    -   Eix Y: Voltatge (V) - Rang automàtic o fixe ±10V
    -   **Dues línies simultànies**:
        -   **Sensor #1 (ai0)**: Color blau (o lliure elecció)
        -   **Sensor #2 (ai1)**: Color vermell (o lliure elecció diferent)
    -   Mida: Omple tot l'espai disponible
    -   Grid: Activat
    -   Llegenda: Activada amb "Sensor #1 (V)" i "Sensor #2 (V)"

### 5.2 Dreta (1/3 de l'amplada)

Controls apilats verticalment amb espai adequat:

1. **Botó Start** 
   - Estat inicial: Habilitat
   - Després de clicar: Deshabilitat fins que es premi Stop
   
2. **Botó Stop**
   - Estat inicial: Deshabilitat
   - Només habilitat durant l'adquisició
   
3. **Botó Carregar mesura**
   - Sempre habilitat
   - Obre diàleg de selecció de fitxer .xlsx
   
4. **Camp d'entrada: Període de mostreig**
   - Label: "Període de mostreig (s):"
   - Tipus: QDoubleSpinBox o QLineEdit amb validació
   - Valor per defecte: 0.1
   - Rang vàlid: 0.001 a 10.0 segons
   - Només editable quan no hi ha adquisició activa
   
5. **Camp d'entrada: Nom del fitxer**
   - Label: "Nom del fitxer:"
   - Tipus: QLineEdit
   - Placeholder: "mesura1.xlsx"
   - Valor per defecte: "mesura_YYYYMMDD_HHMMSS.xlsx" (amb timestamp)
   - Només editable quan no hi ha adquisició activa
   - Validació: Comprovar que l'extensió sigui .xlsx

6. **Etiqueta d'estat** (opcional però recomanat)
   - Mostra: "Esperant...", "Adquirint dades...", "Aturat", "Error: [descripció]"

7. **Footer institucional** (part inferior dreta)
   - Text: "Departament de Física · Universitat de Girona"
   - Estil: Font petita (8-9pt), color gris clar, discret
   - Posició: Alineat a la dreta a la part inferior de la finestra

### 5.3 Dimensions de finestra

- Mida mínima: 1000x600 píxels
- Mida inicial: 1200x700 píxels
- Redimensionable: Sí
- Títol de finestra: "Sistema d'Adquisició de Nivell d'Aigua - UdG"

## 6. Funcionament

### 6.1 Estat inicial

-   Sense adquisició activa
-   Gràfica buida (eixos visibles però sense dades)
-   Cap fitxer obert
-   Botó Start habilitat, Stop deshabilitat

### 6.2 En prémer Start

Seqüència d'operacions:

0. **Validar inputs**
   - Comprovar que el període de mostreig és vàlid (0.001-10.0 s)
   - Comprovar que el nom del fitxer és vàlid i té extensió .xlsx
   - Si el fitxer ja existeix, preguntar si sobreescriure

1. **Netejar gràfica**
   - Eliminar qualsevol dada anterior de la visualització
   - Resetar els eixos

2. **Activar sortides digitals**
   - Activar NI-9472 DO0 a nivell alt (24V) - Sensor #1
   - Activar NI-9472 DO1 a nivell alt (24V) - Sensor #2
   - Esperar 100 ms per estabilització dels sensors

3. **Crear fitxer de dades**
   - Crear el fitxer Excel indicat
   - Escriure capçalera: `time_seconds`, `voltage_sensor1`, `voltage_sensor2`
   - Deixar el fitxer obert per escriptura contínua

4. **Iniciar tasca DAQmx**
   - Configurar canals analògics ai0 i ai1 (±10V, RSE)
   - Configurar timing: 1000 Hz continuous per ambdós canals
   - Iniciar tasca

5. **Començar bucle d'adquisició**
   - Utilitzar QTimer o QThread per no bloquejar GUI
   - Cada període indicat:
     - Llegir mostres disponibles del buffer (ambdós canals simultàniament)
     - Calcular la mitjana de les mostres per cada canal
     - Afegir punt (temps, voltatge_sensor1, voltatge_sensor2) al fitxer
     - Actualitzar gràfica amb els nous punts (ambdues línies)
   - Mantenir temps relatiu des de l'inici (t=0)

6. **Actualitzar estat UI**
   - Deshabilitar botó Start
   - Habilitar botó Stop
   - Deshabilitar camps d'entrada
   - Actualitzar etiqueta d'estat: "Adquirint dades..."

### 6.3 En prémer Stop

Seqüència d'operacions:

1. **Aturar bucle d'adquisició**
   - Cancelar QTimer o senyalitzar QThread per aturar-se

2. **Aturar i netejar tasca DAQmx**
   - Cridar task.stop()
   - Cridar task.close()

3. **Tancar fitxer**
   - Assegurar que totes les dades s'han escrit
   - Tancar el fitxer Excel correctament

4. **Apagar sortides digitals**
   - Desactivar NI-9472 DO0 (0V) - Sensor #1
   - Desactivar NI-9472 DO1 (0V) - Sensor #2

5. **Deixar gràfica congelada**
   - No netejar les dades visualitzades
   - Permetre que l'usuari vegi el resultat final

6. **Actualitzar estat UI**
   - Habilitar botó Start
   - Deshabilitar botó Stop
   - Habilitar camps d'entrada
   - Actualitzar etiqueta d'estat: "Aturat"

### 6.4 En prémer Carregar mesura

1. **Obrir diàleg de selecció**
   - Utilitzar QFileDialog.getOpenFileName()
   - Filtre: "*.xlsx"
   - Directori inicial: Directori de treball actual

2. **Llegir fitxer**
   - Utilitzar pandas o openpyxl per llegir el fitxer
   - Validar que té les columnes `time_seconds`, `voltage_sensor1` i `voltage_sensor2`
   - Gestionar errors si el format no és correcte

3. **Visualitzar dades**
   - Netejar gràfica actual
   - Dibuixar tots els punts del fitxer carregat (ambdues línies amb colors diferents)
   - Ajustar eixos per visualitzar totes les dades

4. **Gestió d'errors**
   - Si el fitxer no existeix o és invàlid: Mostrar QMessageBox amb error
   - No modificar l'estat de l'aplicació (seguir en mode "Aturat")

### 6.5 En tancar l'aplicació

1. **Si hi ha adquisició activa**:
   - Executar automàticament la seqüència "En prémer Stop"
   - Mostrar diàleg confirmant que es tancarà l'adquisició
   - Esperar que tot estigui tancat correctament

2. **Alliberar recursos**:
   - Tancar totes les tasques DAQmx
   - Tancar fitxers oberts
   - Apagar sortides digitals

## 7. Format del fitxer

- **Extensió**: `.xlsx` (Excel)
- **Format**: Taula amb capçalera
- **Columnes**:
  - `time_seconds` (float): Temps en segons des de l'inici de la mesura
  - `voltage_sensor1` (float): Voltatge mesurat pel sensor #1 en V
  - `voltage_sensor2` (float): Voltatge mesurat pel sensor #2 en V

**Exemple**:
```
time_seconds | voltage_sensor1 | voltage_sensor2
0.000        | 2.345          | 3.456
0.100        | 2.347          | 3.458
0.200        | 2.350          | 3.460
...
```

## 8. Requisits no funcionals

### 8.1 Rendiment
- **L'adquisició no ha de bloquejar la GUI**: Utilitzar threading (QThread) o QTimer per separar la lògica d'adquisició de la GUI
- **La gràfica ha de ser fluida**: Utilitzar pyqtgraph amb downsampling automàtic si hi ha molts punts (>10000)
- **Actualització de gràfica**: Màxim cada 50-100 ms per evitar sobrecàrrega visual

### 8.2 Fiabilitat
- **Guardar dades de forma segura**: 
  - Utilitzar context managers (`with open()`) per garantir tancament de fitxers
  - Gestionar excepcions durant l'escriptura
  - Fer flush periòdic del buffer del fitxer

- **Gestió d'errors**:
  - Si el sensor es desconnecta: Mostrar error i aturar adquisició
  - Si el fitxer no es pot crear: Mostrar error i no iniciar adquisició
  - Si DAQmx falla: Capturar excepció i mostrar missatge descriptiu
  - Utilitzar try-except en operacions crítiques

### 8.3 Usabilitat
- **El programa ha de ser estable**: 
  - No pot crastejar mai, fins i tot amb inputs incorrectes
  - Sempre ha de permetre tancar correctament
  
- **Reutilitzable**:
  - El codi ha de ser modular (separar lògica DAQ, GUI i fitxers)
  - Comentaris en parts clau del codi
  - Noms de variables descriptius

### 8.4 Validacions

- **Període de mostreig**:
  - Mínim: 0.001 s (1 ms) - Encara que el hardware mostregi a 1 kHz
  - Màxim: 10.0 s
  - Missatge d'error si està fora de rang

- **Nom de fitxer**:
  - Ha de tenir extensió .xlsx
  - No pot estar buit
  - Si existeix, confirmar sobreescriptura

- **Configuració hardware**:
  - Comprovar que el dispositiu cDAQ està connectat abans de començar
  - Missatge d'error clar si no es troba el hardware

## 9. Arquitectura del codi (recomanació)

```
main.py                 # Punt d'entrada de l'aplicació
├── gui/
│   ├── main_window.py  # Classe MainWindow (PyQt5)
│   └── widgets.py      # Widgets personalitzats si cal
├── daq/
│   ├── acquisition.py  # Classe per gestionar DAQmx
│   └── sensor.py       # Classe específica per AWP-24-3
├── data/
│   ├── file_handler.py # Lectura/escriptura de fitxers Excel
│   └── processor.py    # Processament de dades (mitjanes, etc.)
└── utils/
    ├── config.py       # Configuració (noms de dispositius, etc.)
    └── validators.py   # Validació d'inputs
```

## 10. Exemple de noms de dispositius

Els noms reals dels dispositius DAQmx dependran de la configuració de NI MAX. Exemples típics:

- Xassís: `cDAQ1`
- Mòdul NI-9201: `cDAQ1Mod1`
- Canals analògics: `cDAQ1Mod1/ai0:1` (llegir ai0 i ai1 simultàniament)
- Mòdul NI-9472: `cDAQ1Mod2`
- Sortides digitals: 
  - `cDAQ1Mod2/port0/line0` (DO0 - Sensor #1)
  - `cDAQ1Mod2/port0/line1` (DO1 - Sensor #2)

**IMPORTANT**: Aquests noms s'han de verificar amb NI MAX abans d'executar el programa. Idealment, el programa hauria de permetre configurar aquests noms o detectar-los automàticament.

## 11. Consideracions addicionals

### 11.1 Millores opcionals (no obligatòries)

- Mostrar valor actual del voltatge en text gran
- Guardar configuració (període, últim fitxer) en un fitxer .ini
- Permetre exportar la gràfica com a imatge (PNG, SVG)
- Estadístiques en temps real (mitjana, min, max, desviació estàndard)
- Zoom i pan a la gràfica
- Marcadors temporals (anotacions) a la gràfica

### 11.2 Documentació

El programa ha d'incloure:
- Docstrings a totes les classes i funcions principals
- README.md amb:
  - Instal·lació de dependències
  - Configuració del hardware (NI MAX)
  - Instruccions d'ús
  - Troubleshooting bàsic

### 11.3 Testing

Recomanat però no obligatori:
- Comprovar que funciona sense hardware (mode simulació)
- Test unitaris per validadors
- Test d'integració per lectura/escriptura de fitxers
