# 🧪 GUIA DE TEST I SIMULACIÓ

## 🎯 Què és el Mode Simulació?

El mode simulació permet **executar tot el programa sense necessitat de hardware real** (cDAQ, sensors, etc.). 

### Utilitats:
- ✅ **Testejar** la interfície gràfica
- ✅ **Verificar** que tot funciona abans de connectar hardware
- ✅ **Desenvolupar** sense dependre del hardware
- ✅ **Demostrar** el sistema sense muntatge físic
- ✅ **Formar** usuaris abans d'usar l'equip real

---

## 🚀 COM UTILITZAR EL MODE SIMULACIÓ

### Opció 1: Executar l'Aplicació Simulada

```bash
# Amb uv (recomanat)
uv run python main_simulation.py

# O amb Python directament
python main_simulation.py
```

Això obre la **interfície gràfica completa** amb dades sintètiques:
- Dos sensors virtuals generant dades realistes
- Voltatges base al voltant de 2.5V i 3.5V
- Oscil·lacions simulant variacions del nivell d'aigua
- Soroll gaussià per realisme
- Deriva lenta en el temps

**Tot funciona igual que amb hardware real!**

### Opció 2: Executar Tests Automàtics

```bash
# Amb uv
uv run python test_simulation.py

# O amb Python directament
python test_simulation.py
```

Això executa **tests automàtics** que verifiquen:
- ✓ Validadors d'inputs
- ✓ Processador de dades
- ✓ Sistema DAQmx simulat
- ✓ Gestor de sensors
- ✓ Gestor de fitxers Excel
- ✓ Cicle complet d'adquisició

---

## 📊 QUÈ TESTEJA CADA SCRIPT

### test_simulation.py - Tests Automàtics

```
TEST 1: Validadors
├─ Períodes de mostreig (vàlids i invàlids)
├─ Noms de fitxer (vàlids i invàlids)
└─ Validacions generals

TEST 2: Processador de Dades
├─ Càlcul de mitjanes
└─ Estadístiques (mean, min, max, std)

TEST 3: Sistema DAQmx Simulat
├─ Mode simulació activat
├─ Configurar tasques
├─ Activar sensors
├─ Iniciar adquisició
├─ Llegir mostres
├─ Forma de dades correcta
├─ Valors dins del rang
├─ Aturar adquisició
└─ Neteja de tasques

TEST 4: Gestor de Sensors
├─ Processar dades multicanal
├─ Voltatges dins del rang
└─ Validar lectures

TEST 5: Gestor de Fitxers
├─ Crear fitxer Excel
├─ Afegir dades
├─ Guardar dades
├─ Tancar fitxer
├─ Carregar dades
├─ Columnes correctes
└─ Neteja correcta

TEST 6: Cicle Complet d'Adquisició
├─ Configurar DAQ
├─ Activar sensors
├─ Crear fitxer
├─ Iniciar adquisició
├─ 5 lectures completes
├─ Tancar correctament
└─ Fitxer final vàlid
```

### main_simulation.py - Aplicació Interactiva

Obre la GUI completa on pots:
- ✅ Prémer Start → Veure dades en temps real
- ✅ Ajustar període de mostreig
- ✅ Guardar dades en Excel
- ✅ Prémer Stop → Aturar adquisició
- ✅ Carregar mesures guardades
- ✅ Veure la gràfica amb dos sensors

---

## 🔄 WORKFLOW DE DESENVOLUPAMENT

### 1. Primera vegada - Verificar Instal·lació

```bash
# Executar tests automàtics
python test_simulation.py
```

Si tots passen → Tot està instal·lat correctament ✅

### 2. Desenvolupament - Provar Canvis

```bash
# Executar aplicació simulada
python main_simulation.py
```

Pots:
- Testejar la GUI
- Verificar funcionalitats
- Guardar dades de prova
- No necessites hardware

### 3. Producció - Usar Hardware Real

```bash
# Executar amb hardware real
python main.py
```

Ara sí que necessites:
- cDAQ connectat
- Sensors connectats
- NI-DAQmx instal·lat

---

## 🎨 DADES SINTÈTIQUES GENERADES

El simulador genera dades realistes amb:

### Sensor #1 (ai0)
- **Voltatge base:** ~2.5 V
- **Oscil·lació:** ±0.2 V (freqüència 0.1 Hz)
- **Soroll:** ±0.05 V (gaussià)
- **Deriva:** +0.001 V/s

### Sensor #2 (ai1)
- **Voltatge base:** ~3.5 V
- **Oscil·lació:** ±0.2 V (freqüència 0.1 Hz, desfasada)
- **Soroll:** ±0.05 V (gaussià)
- **Deriva:** +0.001 V/s

Aquestes dades són **prou realistes** per:
- Semblar lectures reals de sensors
- Testejar el processament de dades
- Verificar que les gràfiques es veuen bé
- Comprovar que els fitxers es guarden correctament

---

## 📁 FITXERS GENERATS EN SIMULACIÓ

Els fitxers Excel generats en mode simulació són **completament vàlids** i tenen el mateix format que els reals:

```
time_seconds | voltage_sensor1 | voltage_sensor2
0.000        | 2.523          | 3.487
0.100        | 2.531          | 3.495
0.200        | 2.547          | 3.501
...
```

Pots:
- ✅ Obrir-los amb Excel
- ✅ Carregar-los amb "Carregar mesura"
- ✅ Analitzar-los amb Python/Pandas
- ✅ Utilitzar-los per demos

---

## 🆚 MODE SIMULACIÓ vs MODE REAL

| Característica | Simulació | Real |
|----------------|-----------|------|
| Hardware necessari | ❌ No | ✅ Sí |
| NI-DAQmx necessari | ❌ No | ✅ Sí |
| Dades | Sintètiques | Reals |
| GUI | ✅ Completa | ✅ Completa |
| Guardar fitxers | ✅ Sí | ✅ Sí |
| Carregar fitxers | ✅ Sí | ✅ Sí |
| Velocitat | ⚡ Ràpid | 🐌 Real |
| Cost | 💰 Gratis | 💰💰 Equip car |

---

## 🐛 TROUBLESHOOTING

### Error: "ModuleNotFoundError: No module named 'simulation'"

→ Assegura't que estàs al directori del projecte:
```bash
cd mesurador_nivell
python main_simulation.py
```

### La simulació no genera dades

→ Verifica que el mode simulació s'activa correctament:
```python
from simulation import enable_simulation, is_simulation_enabled
enable_simulation()
print(is_simulation_enabled())  # Ha de retornar True
```

### Els tests fallen

→ Revisa quin test falla exactament i el missatge d'error:
```bash
python test_simulation.py
```

Cada test mostra el motiu del fallo.

### Vull tornar a usar hardware real

Simplement executa:
```bash
python main.py  # NO main_simulation.py
```

---

## 💡 CONSELLS

### Per desenvolupadors:

1. **Sempre testeja primer en simulació** abans de connectar hardware
2. **Usa els tests automàtics** per verificar canvis
3. **Genera fitxers d'exemple** amb simulació per documentació
4. **Ensenya el sistema** a altres sense necessitat de hardware

### Per usuaris finals:

1. **Practica amb simulació** abans d'usar l'equip real
2. **Aprèn la interfície** sense risc de malmetre res
3. **Entén el funcionament** abans de fer mesures reals

---

## 🎓 EXEMPLES D'ÚS

### Exemple 1: Verificar que tot funciona

```bash
# 1. Executar tests
python test_simulation.py

# Si tots passen:
# 2. Executar aplicació simulada
python main_simulation.py

# 3. Prémer Start, deixar córrer 30 segons, Stop
# 4. Comprovar que el fitxer s'ha creat correctament
```

### Exemple 2: Crear dades d'exemple per documentació

```bash
# 1. Executar simulació
python main_simulation.py

# 2. Configurar:
#    - Període: 0.1 s
#    - Fitxer: exemple_mesura.xlsx

# 3. Prémer Start
# 4. Deixar córrer 60 segons
# 5. Prémer Stop

# Ara tens un fitxer d'exemple amb 600 punts!
```

### Exemple 3: Demostració a un client

```bash
# Executar mode simulació
python main_simulation.py

# Mostrar:
# - Com s'inicia la mesura (Start)
# - Com es visualitzen les dades en temps real
# - Com es guarden automàticament
# - Com s'atura (Stop)
# - Com es carreguen mesures anteriors
```

---

## ✅ CHECKLIST DE VERIFICACIÓ

Abans d'usar el hardware real, comprova:

- [ ] `python test_simulation.py` passa tots els tests
- [ ] `python main_simulation.py` s'obre correctament
- [ ] Pots fer Start i veure dades a la gràfica
- [ ] Les dades es guarden en fitxers Excel
- [ ] Pots carregar fitxers guardats
- [ ] La gràfica mostra dos senyals diferents
- [ ] El botó Stop funciona correctament

Si tot està marcat → **Estàs llest per hardware real!** 🚀

---

**Desenvolupat per:** JCM Technologies, SAU  
**Client:** Universitat de Girona - Departament de Física  
**Data:** Gener 2026
