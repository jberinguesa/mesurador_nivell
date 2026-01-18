# 📊 Sistema d'Adquisició de Nivell d'Aigua

**Universitat de Girona - Departament de Física**

Sistema d'adquisició de dades en temps real per mesurar nivells d'aigua utilitzant sensors analògics i hardware National Instruments cDAQ.

---

## 🚀 Instal·lació Ràpida

### Primera instal·lació (ordinador nou)

**Pas 1 - Instal·lar uv (gestor de paquets Python):**

```powershell
winget install astral-sh.uv
```

**Pas 2 - Clonar el projecte des de GitHub:**

```powershell
cd C:\Users\$env:USERNAME\Documents
git clone https://github.com/jberinguesa/mesurador_nivell.git
cd mesurador_nivell
```

O descarrega el ZIP des de: https://github.com/jberinguesa/mesurador_nivell

**Pas 3 - Instal·lar dependències:**

```powershell
uv sync
```

Això instal·larà automàticament:
- Python 3.11+ (si no el tens)
- Totes les llibreries necessàries (PySide6, pyqtgraph, openpyxl, nidaqmx, etc.)

**Pas 4 - Instal·lar NI-DAQmx Runtime (només per hardware real):**

Descarrega i instal·la de: [ni.com](https://www.ni.com/es/support/downloads/drivers/download.ni-daq-mx.html)

**Pas 5 - Crear drecera (opcional):**

Segueix les instruccions de "Crear drecera a l'escriptori" més avall.

---

### Crear drecera a l'escriptori (recomanat)

**Mètode manual - 10 segons:**

1. Obre l'Explorador de Windows
2. Navega a la carpeta `mesurador_nivell/`
3. **Clic dret** sobre `Executar_Aplicacio.bat`
4. Selecciona **"Enviar a" → "Escriptori (crear accés directe)"**
5. **LLEST!** 🎉

Ara pots executar l'aplicació amb doble clic des de l'escriptori.

**Opcional - Canviar icona:**
- Clic dret a la drecera → **"Propietats"**
- Clic **"Canviar icona..."**
- Escriu: `C:\Windows\System32\shell32.dll`
- Tria la icona de gràfic (núm. 23) 📊

---

### Executar directament (sense drecera)

1. Navega a `mesurador_nivell/`
2. **Doble clic** a `Executar_Aplicacio.bat`

---

### Des de PowerShell (per desenvolupadors)

```powershell
cd mesurador_nivell
uv run python main.py
```

### Mode Simulació (sense hardware)

```powershell
uv run python main_simulation.py
```

O crea un fitxer `Executar_Simulacio.bat` amb:
```batch
@echo off
uv run python main_simulation.py
pause
```

---

## 📋 Requisits

### Software

- **Python 3.11+** (gestionat automàticament per uv)
- **uv** - Gestor de paquets Python
  ```powershell
  winget install astral-sh.uv
  ```
- **NI-DAQmx Runtime** (només per hardware real)
  - Descarregar de: [ni.com](https://www.ni.com/es/support/downloads/drivers/download.ni-daq-mx.html)

### Hardware

- **National Instruments cDAQ-9178** (chassis)
- **NI-9201** - Mòdul d'entrada analògica (Slot 2)
- **NI-9472** - Mòdul de sortida digital (Slot 1)
- **2× Sensors de nivell d'aigua AWP-24-3** (sortida 4-20mA)
  - **IMPORTANT:** Els sensors AWP-24-3 requereixen calibració prèvia
  - Consulta el manual del sensor per instruccions detallades
  - El sensor disposa d'un botó per a la calibració

---

## ✨ Característiques

### 🎯 Adquisició de Dades
- ✅ Mostreig continu a taxa configurable (0.001 - 10 s)
- ✅ Dos canals d'entrada analògica simultanis
- ✅ Activació automàtica de sensors via sortides digitals
- ✅ Buffer de 100,000 mostres per evitar pèrdua de dades

### 📏 Sistema de Calibratge
- ✅ Conversió automàtica voltatge → alçada (cm)
- ✅ Calibratge independent per cada sensor
- ✅ Interpolació lineal de 2 punts
- ✅ Persistència automàtica en JSON
- ✅ Valors per defecte: -2V = 0cm, +2V = 5cm

### 📊 Visualització
- ✅ Gràfica en temps real amb pyqtgraph
- ✅ Displays de voltatge i alçada actualitzats cada 500ms
- ✅ Llegenda dinàmica segons calibratge
- ✅ Interfície moderna amb PySide6

### 💾 Exportació de Dades
- ✅ Format Excel (.xlsx) amb openpyxl
- ✅ Columnes: temps, voltatge_sensor1, voltatge_sensor2, alçada_sensor1, alçada_sensor2
- ✅ Flush automàtic cada 10 mostres
- ✅ Noms de fitxer amb timestamp

### 🎭 Mode Simulació
- ✅ Proves sense hardware real
- ✅ Dades sintètiques realistes
- ✅ Perfecte per desenvolupament i demos

---

## 📁 Estructura del Projecte

```
mesurador_nivell/
├── main.py                          # Punt d'entrada (hardware real)
├── main_simulation.py               # Punt d'entrada (simulació)
├── Executar_Aplicacio.bat          # Executar amb doble clic
├── pyproject.toml                   # Configuració del projecte
├── sensor_calibration.json         # Calibracions guardades
│
├── Mesures/                        # Fitxers Excel de mesures (creat automàticament)
│   ├── mesura_20260118_120000.xlsx
│   ├── mesura_20260118_130000.xlsx
│   └── ...
│
├── daq/                            # Adquisició de dades
│   ├── acquisition.py              # Gestió DAQmx
│   └── sensor.py                   # Processament de senyals
│
├── gui/                            # Interfície gràfica
│   ├── main_window.py              # Finestra principal
│   └── calibration_dialog.py      # Diàleg de calibratge
│
├── data/                           # Gestió de dades
│   └── file_handler.py             # Escriptura/lectura Excel
│
├── utils/                          # Utilitats
│   ├── config.py                   # Configuració hardware
│   ├── calibration.py              # Sistema de calibratge
│   └── validators.py               # Validacions
│
├── simulation/                     # Mode simulació
│   └── mock_daq.py                 # Mock de DAQmx
│
└── docs/                           # Documentació
    ├── GUIA_CALIBRATGE.md
    ├── CREAR_DRECERA_MANUAL.md
    ├── INSTALACIO_ORDINADOR_NOU.md
    └── manual_sensor/
        └── AWP-24-3_Users_Guide.pdf
```

---

## 🔧 Configuració Hardware

### Verificació amb NI MAX

1. Obre **NI MAX** (National Instruments Measurement & Automation Explorer)
2. Comprova que `cDAQ1` és visible a **"Devices and Interfaces"**
3. Verifica la configuració:
   - **Slot 1:** NI-9472 (Digital Output) → `cDAQ1Mod1`
   - **Slot 2:** NI-9201 (Analog Input) → `cDAQ1Mod2`

### Connexions

```
Sensor #1 → cDAQ1Mod2/ai0
Sensor #2 → cDAQ1Mod2/ai1

Alimentació Sensor #1 → cDAQ1Mod1/port0/line0
Alimentació Sensor #2 → cDAQ1Mod1/port0/line1
```

### Personalització

Edita `utils/config.py` per canviar:
- Noms de dispositius
- Rangs de voltatge
- Taxa de mostreig
- Mida del buffer

---

## 📖 Ús de l'Aplicació

### 0️⃣ Preparació (Primera vegada)

**Abans de començar, assegura't que:**

1. ✅ Els sensors AWP-24-3 estan **configurats** (procediment amb botó SET/CLEAR)
   - LED vermell parpelleja 1s ON, 9s OFF = configurat correctament
2. ✅ El cDAQ està connectat i encès
3. ✅ Els sensors estan connectats als canals correctes:
   - Sensor #1 → cDAQ1Mod2/ai0
   - Sensor #2 → cDAQ1Mod2/ai1
4. ✅ Has executat `uv sync` per instal·lar dependències

**Verificar hardware:**
- Obre NI MAX
- Comprova que `cDAQ1` és visible
- Verifica que Mod1 (DO) i Mod2 (AI) estan correctament identificats

---

### 1️⃣ Configuració del Sensor (Primera vegada o si canvia el rang)

**Configurar el sensor AWP-24-3 per al rang de mesura:**

1. Obre la caixa del sensor AWP-24-3
2. Submergeix la sonda a la **profunditat màxima** que vols mesurar
3. Amb el LED vermell **ON continu**, prem **SET/CLEAR** una vegada
4. LED vermell parpelleja (1s ON, 1s OFF) → **No moguis la sonda!**
5. Quan acaba: LED parpelleja 1s ON, 9s OFF → **Configurat!**

Aquesta configuració només cal fer-la una vegada (o si canvies el rang de mesura).

---

### 2️⃣ Calibratge Software (Primera vegada o si canvia el muntatge)

1. Clic a **"⚙️ Calibratge"**
2. Per cada sensor:
   - Col·loca a alçada coneguda (ex: 0 cm)
   - Clic **"Llegir"** → Introdueix alçada
   - Repeteix amb altra alçada (ex: 10 cm)
3. Clic **"Desa i Tanca"**
4. Les calibracions es guarden automàticament

### 3️⃣ Adquisició de Dades

1. Configura **període de mostreig** (ex: 0.1 s)
2. Introdueix **nom del fitxer** (ex: mesura_01.xlsx)
3. Clic **"Start"**
4. Les dades es mostren en temps real
5. Clic **"Stop"** per aturar
6. El fitxer Excel es guarda automàticament al directori **`Mesures/`**

**Nota:** El directori `Mesures/` es crea automàticament si no existeix.

### 4️⃣ Visualització

- **Displays:** Mostren voltatge + alçada en temps real
- **Gràfica:** 
  - Si NO calibrat → mostra voltatge (V)
  - Si calibrat → mostra alçada (cm)
- **Llegenda:** Indica unitat actual

### 5️⃣ Carregar Dades Antigues

1. Clic **"Carregar mesura"**
2. Selecciona fitxer `.xlsx` (el diàleg s'obre automàticament a `Mesures/`)
3. Les dades es mostren a la gràfica

---

## 🎓 Calibratge del Sistema

### Valors per Defecte

Si no calibres manualment, s'apliquen aquests valors:

| Punt | Voltatge | Alçada |
|------|----------|--------|
| Punt 1 | -2.0 V | 0.0 cm |
| Punt 2 | +2.0 V | 5.0 cm |

**Fórmula:** `Alçada (cm) = 1.25 × Voltatge + 2.5`

### Calibratge Personalitzat

Per màxima precisió:
- Usa dos punts molt separats (ex: 0cm i 50cm)
- Assegura't que el sensor està estable
- Repeteix la mesura si cal

Les calibracions es guarden a `sensor_calibration.json` i es carreguen automàticament.

---

## 🐛 Solució de Problemes

### Error: "Physical channel does not exist"
**Causa:** Configuració incorrecta dels mòduls
**Solució:** Verifica amb NI MAX que:
- Mod1 = NI-9472 (DO)
- Mod2 = NI-9201 (AI)

### Error: "Buffer overflow" (-200279)
**Causa:** El buffer s'omple massa ràpid
**Solució:** Ja està arreglat amb `BUFFER_SIZE = 100000`

### Error: "Resource requested by this task has already been reserved"
**Causa:** Tasques DAQmx no tancades correctament
**Solució:** 
1. Tanca l'aplicació
2. Obre NI MAX
3. Clic dret a `cDAQ1` → **Reset Device**

### L'aplicació no mostra valors
**Causa:** Sensors no activats
**Solució:** El sistema activa automàticament els sensors via DO

### Warnings de pandas
**Causa:** Concatenació de DataFrames buits
**Solució:** Ja està arreglat a `file_handler.py`

---

## 🔬 Especificacions Tècniques

### Sensor AWP-24-3 (Akamina Technologies)

**⚠️ CONFIGURACIÓ OBLIGATÒRIA DEL SENSOR:**

El sensor AWP-24-3 s'ha de configurar abans d'usar-lo. Aquest procediment ajusta automàticament el rang de mesura segons la profunditat màxima que vols mesurar.

**Procediment de configuració (una sola vegada):**

1. **Preparació:**
   - Connecta l'alimentació (8-24 VDC)
   - LED verd (PWR) s'encén
   - LED vermell ha d'estar **ON contínuament**
   - Si no ho està, manté premut **SET/CLEAR** 3 segons

2. **Configurar el rang:**
   - Submergeix la sonda a la **profunditat màxima** que vols mesurar
   - Prem el botó **SET/CLEAR** una vegada
   - LED vermell parpelleja a 0.5 Hz (1s ON, 1s OFF)
   - **No moguis la sonda** fins que acabi el parpelleig
   - Quan acaba: LED vermell parpelleja 1s ON, 9s OFF (funcionament normal)

3. **Si hi ha error:**
   - LED parpelleja a 5 Hz → prem **RESET** i torna a començar

**Característiques:**
- **Tipus:** Sensor capacitiu digital d'alta precisió
- **Sortida:** -4.5V a +4.5V (analògica, proporcional a l'alçada)
- **Alimentació:** 8-24 VDC, ~16 mA
- **Connector:** BNC (cap del sensor) + 6 pins (alimentació/sortida)
- **Rang de mesura:** Configurable segons profunditat màxima
- **Marges d'immersió:** 1.5 cm mínim des del cap i final del fil sensor

**Després de configurar el sensor:**
1. Connecta'l al sistema cDAQ (NI-9201)
2. Obre l'aplicació
3. Usa el botó "⚙️ Calibratge" del software
4. Calibra la conversió voltatge → alçada (cm) amb almenys 3 punts

**Notes importants:**
- La configuració es guarda a la memòria del sensor
- No cal repetir-la cada cop que l'encens
- Per esborrar configuració: manté **SET/CLEAR** 3 segons
- El fil sensor no s'ha de tocar amb objectes afilats

### Altres Sensors Compatibles
- Qualsevol sensor analògic de 0-10V
- Sensors amb sortida proporcional a l'alçada
- Sensors amb sortida 4-20mA (amb conversió adequada)

### Resolució
- **Hardware:** 16-bit (NI-9201)
- **Rang:** ±10V
- **Precisió:** ~0.3mV

### Taxa de Mostreig
- **Hardware:** 1000 Hz per canal
- **Software:** Configurable 0.001 - 10 s
- **Buffer:** 100,000 mostres

---

## 📊 Format de Dades Excel

```
| time_seconds | voltage_sensor1 | voltage_sensor2 | height_sensor1 | height_sensor2 |
|--------------|-----------------|-----------------|----------------|----------------|
| 0.0          | -1.234          | -2.456          | 1.23           | 0.00           |
| 0.1          | -1.235          | -2.457          | 1.24           | 0.01           |
| ...          | ...             | ...             | ...            | ...            |
```

---

## 👥 Autors

**Departament de Física**  
Universitat de Girona

**Repositori:** https://github.com/jberinguesa/mesurador_nivell

---

## 📄 Llicència

Ús intern acadèmic - Universitat de Girona

---

## 🆘 Suport

Per problemes o preguntes:
- Revisa la documentació a `docs/`
- Executa en mode simulació per debugging
- Verifica configuració hardware amb NI MAX

---

## 🎯 Roadmap

- [x] Sistema bàsic d'adquisició
- [x] Calibratge voltatge → alçada
- [x] Exportació Excel
- [x] Mode simulació
- [x] Interfície gràfica moderna
- [ ] Anàlisi estadístic integrat
- [ ] Export a CSV/JSON
- [ ] Configuració multi-dispositiu

---

**Última actualització:** Gener 2026  
**Versió:** 2.0
