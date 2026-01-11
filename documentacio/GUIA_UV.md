# 🚀 GUIA D'INSTAL·LACIÓ AMB UV

## ✨ Per què UV?

- ⚡ **10-100x més ràpid** que pip
- 🔒 **Lockfile automàtic** (uv.lock)
- 🛠️ **Tot-en-un**: gestiona Python, venvs i paquets
- 📦 **Compatible** amb requirements.txt i pyproject.toml

---

## 📦 INSTAL·LAR UV

### Windows (PowerShell)
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Linux/Mac
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Reinicia el terminal després d'instal·lar.

---

## 🎯 CONFIGURAR EL PROJECTE AMB UV

### Opció 1: Utilitzant pyproject.toml (RECOMANAT) ⭐

```bash
# 1. Navegar al directori del projecte
cd mesurador_nivell

# 2. Sincronitzar (crea venv + instal·la tot automàticament)
uv sync

# 3. Executar el test de configuració
uv run python test_setup.py

# 4. Executar l'aplicació
uv run python main.py
```

**Això és tot!** 🎉 `uv sync` ho fa TOT:
- Crea l'entorn virtual
- Instal·la Python si cal
- Instal·la totes les dependències
- Genera el lockfile (uv.lock)

### Opció 2: Utilitzant requirements.txt (Compatible)

```bash
# 1. Crear entorn virtual
cd mesurador_nivell
uv venv

# 2. Activar entorn virtual
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 3. Instal·lar dependències
uv pip install -r requirements.txt

# 4. Executar
python test_setup.py
python main.py
```

---

## 🔧 COMANDES UV ÚTILS

### Gestió de dependències

```bash
# Afegir una nova dependència
uv add <paquet>

# Exemple: afegir matplotlib
uv add matplotlib

# Eliminar una dependència
uv remove <paquet>

# Actualitzar totes les dependències
uv sync --upgrade
```

### Executar codi

```bash
# Executar Python dins l'entorn
uv run python script.py

# Executar comandes directament
uv run test_setup.py
```

### Gestió de l'entorn

```bash
# Crear entorn virtual
uv venv

# Recrear entorn des de zero
uv venv --force

# Veure informació de l'entorn
uv venv --python 3.11  # Crear amb Python específic
```

---

## 📂 ESTRUCTURA DE FITXERS AMB UV

Després d'executar `uv sync`, tindràs:

```
mesurador_nivell/
├── .venv/                  # Entorn virtual (creat per uv)
├── uv.lock                 # Lockfile (versions exactes)
├── pyproject.toml          # Configuració del projecte
├── requirements.txt        # (opcional, per compatibilitat)
├── main.py
├── test_setup.py
└── ...
```

**IMPORTANT:**
- `.venv/` i `uv.lock` **NO** es pugen a Git (ja està al .gitignore)
- `pyproject.toml` **SÍ** es puja a Git
- Quan algú clona el repo, només cal fer `uv sync`

---

## 🔄 WORKFLOW DIARI AMB UV

### Primera vegada (configurar projecte)
```bash
cd mesurador_nivell
uv sync
```

### Cada dia (executar aplicació)
```bash
# Només cal executar directament
uv run python main.py
```

### Afegir nova dependència
```bash
# Exemple: vull afegir matplotlib
uv add matplotlib

# Això actualitza pyproject.toml i uv.lock automàticament
```

### Actualitzar dependències
```bash
# Actualitzar tot
uv sync --upgrade

# O actualitzar només un paquet
uv add --upgrade numpy
```

---

## 👥 TREBALLAR EN EQUIP AMB UV

### Tu (desenvolupador)

1. Fas canvis i afegeixes dependències:
   ```bash
   uv add nova-llibreria
   ```

2. Puges a Git:
   ```bash
   git add pyproject.toml uv.lock
   git commit -m "Afegida nova dependència"
   git push
   ```

### Company (rep els canvis)

1. Baixa els canvis:
   ```bash
   git pull
   ```

2. Sincronitza l'entorn:
   ```bash
   uv sync
   ```

**Això garanteix que tots tenen EXACTAMENT les mateixes versions!** 🔒

---

## 🆚 UV vs PIP: Comparació

| Característica | UV | PIP |
|----------------|----|----- |
| Velocitat | ⚡⚡⚡ (10-100x) | 🐌 |
| Lockfile | ✅ Automàtic | ❌ Manual |
| Gestió Python | ✅ Integrada | ❌ Cal pyenv |
| Resolució deps | ✅ Intelligent | ⚠️ Bàsica |
| Compatibilitat | ✅ 100% pip | ✅ Natiu |

---

## 🐛 TROUBLESHOOTING

### Error: "uv: command not found"
→ Reinicia el terminal després d'instal·lar uv

### Error: "No s'ha trobat Python"
→ uv pot instal·lar Python automàticament:
```bash
uv python install 3.11
```

### Error: "Lockfile desincronitzat"
→ Regenera el lockfile:
```bash
uv lock --upgrade
uv sync
```

### Vull començar de zero
```bash
# Esborrar entorn i recrear
rm -rf .venv uv.lock
uv sync
```

---

## 💡 CONSELLS PRO

### 1. Alias útils (afegir a .bashrc o .zshrc)
```bash
alias uvs="uv sync"
alias uvr="uv run python"
alias uva="uv add"
```

### 2. Scripts al pyproject.toml
Pots afegir scripts personalitzats:

```toml
[project.scripts]
test = "test_setup:main"
start = "main:main"
```

Després executar:
```bash
uv run test   # Executa test_setup.py
uv run start  # Executa main.py
```

### 3. Desenvolupament amb uv
```bash
# Instal·lar dependències de desenvolupament
uv sync --group dev

# Això instal·la pytest, black, ruff, etc.
```

---

## ✅ CHECKLIST RÀPIDA

Workflow complet amb UV:

```bash
# [ ] 1. Instal·lar uv (una sola vegada)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# [ ] 2. Clonar/descomprimir projecte
cd mesurador_nivell

# [ ] 3. Sincronitzar entorn (crea tot automàticament)
uv sync

# [ ] 4. Verificar configuració
uv run python test_setup.py

# [ ] 5. Executar aplicació
uv run python main.py
```

**Això és tot!** Molt més simple que amb pip/venv tradicional. 🎉

---

## 🔗 Recursos

- **Documentació UV:** https://docs.astral.sh/uv/
- **GitHub UV:** https://github.com/astral-sh/uv
- **Guia pyproject.toml:** https://packaging.python.org/en/latest/guides/writing-pyproject-toml/

---

**Desenvolupat per:** JCM Technologies, SAU  
**Client:** Universitat de Girona - Departament de Física  
**Actualitzat:** Gener 2026
