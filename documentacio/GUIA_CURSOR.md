# 🚀 GUIA RÀPIDA PER UTILITZAR EL CODI A CURSOR

## 📦 Contingut del Paquet

Has rebut el programa complet del **Sistema d'Adquisició de Nivell d'Aigua** per la Universitat de Girona.

El paquet inclou:
- ✅ Codi Python complet i funcional
- ✅ Estructura modular organitzada
- ✅ Documentació completa (README.md)
- ✅ Script de test per verificar configuració
- ✅ Tots els fitxers de configuració necessaris

## 🔧 COM UTILITZAR-HO A CURSOR

### Opció 1: Descomprimir i obrir (MÉS RÀPID)

1. **Descarrega el ZIP:**
   - Baixa `mesurador_nivell.zip` des d'aquí

2. **Descomprimeix:**
   - Fes clic dret → Extreure tot
   - Tria una ubicació (per exemple: `C:\Projects\`)

3. **Obre a Cursor:**
   - Obre Cursor
   - File → Open Folder
   - Selecciona la carpeta `mesurador_nivell`

4. **Instal·la dependències:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Comprova la configuració:**
   ```bash
   python test_setup.py
   ```

6. **Executa l'aplicació:**
   ```bash
   python main.py
   ```

### Opció 2: Copiar fitxers individualment

Si prefereixes copiar fitxer per fitxer a Cursor:

1. Obre Cursor i crea un projecte nou
2. Crea l'estructura de carpetes:
   ```
   mesurador_nivell/
   ├── gui/
   ├── daq/
   ├── data/
   └── utils/
   ```
3. Copia cada fitxer a la seva carpeta corresponent
4. Segueix els passos 4-6 de l'Opció 1

## ⚙️ CONFIGURACIÓ NECESSÀRIA

### Abans d'executar el programa:

1. **Instal·lar NI-DAQmx Runtime**
   - Descarrega de: https://www.ni.com/
   - Cerca "NI-DAQmx Runtime"
   - Instal·la i reinicia l'ordinador

2. **Configurar hardware amb NI MAX**
   - Obre NI Measurement & Automation Explorer
   - Verifica que el cDAQ apareix com a `cDAQ1`
   - Comprova els mòduls:
     - Slot 1: NI-9201
     - Slot 2: NI-9472

3. **Ajustar noms de dispositius (si cal)**
   - Obre `utils/config.py`
   - Modifica els noms si el teu hardware és diferent:
     ```python
     DEVICE_NAME = "cDAQ1"  # Canvia si és necessari
     ```

## 🧪 VERIFICAR QUE TOT FUNCIONA

Executa el script de test:

```bash
python test_setup.py
```

Aquest script comprova:
- ✓ Totes les llibreries estan instal·lades
- ✓ El hardware DAQmx està connectat
- ✓ La configuració és correcta
- ✓ El dispositiu configurat existeix

Si tots els tests passen → Tot està preparat! 🎉

## 📂 ESTRUCTURA DEL PROJECTE

```
mesurador_nivell/
│
├── main.py                    # ⭐ Executa aquest fitxer
├── test_setup.py              # Script de verificació
├── requirements.txt           # Dependències Python
├── README.md                  # Documentació completa
├── .gitignore                 # Control de versions
│
├── gui/                       # Interfície gràfica
│   ├── __init__.py
│   └── main_window.py         # Finestra principal PyQt5
│
├── daq/                       # Adquisició de dades
│   ├── __init__.py
│   ├── acquisition.py         # Tasques DAQmx
│   └── sensor.py              # Lògica sensors AWP-24-3
│
├── data/                      # Gestió de dades
│   ├── __init__.py
│   ├── file_handler.py        # Excel
│   └── processor.py           # Processament
│
└── utils/                     # Utilitats
    ├── __init__.py
    ├── config.py              # ⚙️ Configuració del sistema
    └── validators.py          # Validacions
```

## 🎯 PAS A PAS PER EXECUTAR

1. Obre el terminal a Cursor (Terminal → New Terminal)

2. Comprova que estàs al directori correcte:
   ```bash
   cd mesurador_nivell
   ```

3. Instal·la dependències:
   ```bash
   pip install -r requirements.txt
   ```

4. Verifica configuració:
   ```bash
   python test_setup.py
   ```

5. Executa l'aplicació:
   ```bash
   python main.py
   ```

## 🐛 TROUBLESHOOTING COMÚ

**Error: "No module named nidaqmx"**
→ Instal·la NI-DAQmx Runtime primer, després `pip install nidaqmx`

**Error: "Dispositiu no trobat"**
→ Comprova amb NI MAX que el cDAQ està connectat i encès

**Error: "No s'han pogut configurar tasques"**
→ Tanca qualsevol altra aplicació que utilitzi el hardware

**La gràfica no es veu bé**
→ Normal, només apareix quan comences l'adquisició amb "Start"

## 💡 CONSELLS PER CURSOR

- **IntelliSense:** Cursor detectarà automàticament les dependències
- **Debugging:** Pots afegir breakpoints a qualsevol línia
- **Format del codi:** Usa Format Document per mantenir l'estil
- **Git:** El .gitignore ja està configurat per Python

## 📞 SUPORT

Si tens problemes:
1. Revisa el README.md complet (secció Troubleshooting)
2. Executa `python test_setup.py` per diagnosticar
3. Comprova que el hardware està configurat a NI MAX

## ✅ CHECKLIST FINAL

Abans de començar, assegura't que:
- [ ] NI-DAQmx Runtime està instal·lat
- [ ] El cDAQ està connectat i visible a NI MAX
- [ ] Els sensors estan connectats correctament
- [ ] Python 3.8+ està instal·lat
- [ ] Has executat `pip install -r requirements.txt`
- [ ] `python test_setup.py` passa tots els tests

Si tots els punts estan marcats → Estàs llest per començar! 🚀

---

**Desenvolupat per:** JCM Technologies, SAU  
**Client:** Universitat de Girona - Departament de Física  
**Data:** Gener 2026
