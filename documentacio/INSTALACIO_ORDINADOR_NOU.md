# 💻 INSTAL·LACIÓ EN ORDINADOR NOU

Guia completa per instal·lar el sistema en un ordinador sense res configurat.

---

## ✅ CHECKLIST INICIAL

Abans de començar, necessites:

- [ ] Windows 10 o 11
- [ ] Connexió a Internet
- [ ] Permisos d'administrador
- [ ] El projecte MesuradorNivell (descarregat o clonat)
- [ ] Hardware NI cDAQ connectat (opcional per proves)

---

## 📦 PAS 1: INSTAL·LAR UV

**uv** és el gestor de paquets Python que instal·la automàticament Python i totes les dependències.

### Opció A - Amb winget (recomanat):

```powershell
winget install astral-sh.uv
```

### Opció B - Amb PowerShell (manual):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### Verificar instal·lació:

```powershell
uv --version
```

Hauries de veure algo com: `uv 0.x.x`

---

## 📂 PAS 2: DESCARREGAR EL PROJECTE

### Opció A - Clonar des de Git:

```powershell
cd C:\Users\$env:USERNAME\Documents
git clone <URL_del_repositori>
cd MesuradorNivell
```

### Opció B - Descarregar ZIP:

1. Descarrega el ZIP del projecte
2. Descomprimeix a `C:\Users\<usuari>\Documents\MesuradorNivell\`
3. Navega a la carpeta:

```powershell
cd C:\Users\$env:USERNAME\Documents\MesuradorNivell
```

---

## 🔧 PAS 3: INSTAL·LAR DEPENDÈNCIES

Dins del directori del projecte, executa:

```powershell
uv sync
```

### Què fa `uv sync`?

1. ✅ Instal·la Python 3.11+ (si no el tens)
2. ✅ Crea un entorn virtual (`.venv/`)
3. ✅ Instal·la totes les llibreries del `pyproject.toml`:
   - PySide6 (interfície gràfica)
   - pyqtgraph (gràfiques)
   - openpyxl (fitxers Excel)
   - nidaqmx (comunicació amb hardware)
   - pandas (gestió de dades)
   - numpy (càlculs numèrics)

### Temps estimat:

- Primera vegada: ~2-5 minuts
- Depèn de la velocitat d'Internet

### Possible error:

Si veus: `uv: command not found`
- Tanca i torna a obrir PowerShell
- O afegeix uv al PATH manualment

---

## 🔌 PAS 4: INSTAL·LAR NI-DAQmx RUNTIME

**Només necessari si treballes amb hardware real.**

### Descarregar:

1. Ves a: https://www.ni.com/es/support/downloads/drivers/download.ni-daq-mx.html
2. Descarrega **NI-DAQmx Runtime** (no el complet, només Runtime)
3. Instal·la seguint l'assistent

### Versió recomanada:

- NI-DAQmx 2023 Q4 o posterior

### Verificar instal·lació:

1. Obre **NI MAX** (s'instal·la amb NI-DAQmx)
2. Comprova que veus el cDAQ a "Devices and Interfaces"
3. Verifica que detecta els mòduls:
   - Slot 1: NI-9472 (DO)
   - Slot 2: NI-9201 (AI)

### Si no tens hardware:

Pots saltar aquest pas i usar el **mode simulació** (`main_simulation.py`)

---

## 🎯 PAS 5: CREAR DRECERA (OPCIONAL)

Per executar fàcilment des de l'escriptori:

1. Navega a la carpeta del projecte
2. Clic dret sobre `Executar_Aplicacio.bat`
3. "Enviar a" → "Escriptori (crear accés directe)"
4. Ja tens la drecera! 🎉

---

## ✅ PAS 6: VERIFICAR INSTAL·LACIÓ

### Prova en mode simulació:

```powershell
uv run python main_simulation.py
```

Hauria d'obrir-se l'aplicació amb dades simulades.

### Prova amb hardware real:

```powershell
uv run python main.py
```

Si tot està bé, veuràs valors reals dels sensors.

---

## 🔧 CONFIGURACIÓ ADDICIONAL

### Calibració dels sensors AWP-24-3:

**⚠️ MOLT IMPORTANT**: Els sensors s'han de calibrar físicament abans d'usar-los.

Consulta `docs/manual_sensor/AWP-24-3_manual.pdf` per:
1. Ajustar potenciòmetres ZERO i SPAN
2. Verificar sortida 4-20mA
3. Connectar resistència de conversió (250Ω)

### Configuració del hardware:

Si tens una configuració diferent, edita `utils/config.py`:

```python
DEVICE_NAME = "cDAQ1"        # Nom del teu dispositiu
AI_CHANNELS = "cDAQ1Mod2/ai0:1"  # Canals analògics
DO_CHANNELS = ["cDAQ1Mod1/port0/line0", "cDAQ1Mod1/port0/line1"]  # Digitals
```

---

## 🚀 COMENÇAR A USAR

### Workflow complet:

1. **Calibrar sensors físics** (una sola vegada)
   - Ajustar potenciòmetres ZERO i SPAN
   - Verificar 4-20mA

2. **Calibrar en software** (primera vegada o si canvies muntatge)
   - Obrir aplicació
   - Clic "⚙️ Calibratge"
   - Seguir instruccions

3. **Mesurar**
   - Configurar període de mostreig
   - Introduir nom de fitxer
   - Clic "Start"

---

## 🆘 SOLUCIÓ DE PROBLEMES

### Error: "uv: command not found"

**Causa:** uv no està al PATH  
**Solució:**
1. Tanca i torna a obrir PowerShell
2. O executa: `$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")`

### Error: "No module named 'nidaqmx'"

**Causa:** Dependències no instal·lades  
**Solució:**
```powershell
uv sync
```

### Error: "Physical channel does not exist"

**Causa:** Configuració hardware incorrecta  
**Solució:**
1. Obre NI MAX
2. Verifica mòduls:
   - Mod1 = NI-9472 (DO)
   - Mod2 = NI-9201 (AI)
3. Edita `utils/config.py` si és necessari

### L'aplicació no s'obre

**Causa:** Python o dependències no instal·lades  
**Solució:**
```powershell
# Reinstal·lar tot
uv sync --reinstall
```

### Vull provar sense hardware

**Solució:**
```powershell
uv run python main_simulation.py
```

---

## 📋 RESUM RÀPID

Per a un ordinador nou amb **ZERO configuració**:

```powershell
# 1. Instal·lar uv
winget install astral-sh.uv

# 2. Navegar al projecte
cd C:\Users\$env:USERNAME\Documents\MesuradorNivell

# 3. Instal·lar tot
uv sync

# 4. Provar
uv run python main_simulation.py

# 5. Crear drecera (manual)
# Clic dret a Executar_Aplicacio.bat → Enviar a escriptori
```

**Temps total: ~10 minuts** ⏱️

---

## 🎓 NOTES FINALS

### Per a estudiants/investigadors nous:

1. Llegeix primer el `README.md`
2. Consulta `GUIA_CALIBRATGE.md`
3. Revisa els manuals dels sensors a `docs/manual_sensor/`

### Per a desenvolupadors:

1. El codi està organitzat en mòduls (`daq/`, `gui/`, `utils/`)
2. Usa `main_simulation.py` per desenvolupar sense hardware
3. Els tests automàtics són a `test_simulation.py`

### Per a administradors IT:

1. No calen permisos d'admin després de la instal·lació inicial
2. uv gestiona tot automàticament (Python + paquets)
3. Les dades es guarden a la carpeta del projecte

---

## ✅ VERIFICACIÓ FINAL

Si tot ha anat bé, hauràs de poder:

- [ ] Executar `uv run python main.py` sense errors
- [ ] Veure l'aplicació oberta amb la interfície gràfica
- [ ] Veure valors dels sensors (reals o simulats)
- [ ] Fer clic a "⚙️ Calibratge" i veure el diàleg
- [ ] Prémer "Start" i veure la gràfica moure's

**Si tots els punts funcionen, ENHORABONA! 🎉**

Ja tens el sistema completament instal·lat i funcional.

---

**Última actualització:** Gener 2026
