# Analyse Forex Multi-Timeframe avec IA Locale

Analyse technique multi-timeframe (daily/1h/5m) de paires forex majeures avec signaux IA via Ollama. Utilise OpenBB (provider yfinance) comme source de données.

## Paires supportées

EURUSD, USDJPY, GBPUSD — configurables dans `lib/config.py`.

## Notebooks (ordre d'exécution)

| Fichier | Rôle |
|---|---|
| `01_scan_rapide.ipynb` | Scanne toutes les paires, affiche un tableau récapitulatif avec les signaux IA |
| `02_signal_paire.ipynb` | Analyse détaillée d'une paire au choix (configurable en 1ʳᵉ cellule) |
| `03_exemple_multi_tf.ipynb` | Exemple fixe EURUSD (référence) |

## Installation

```bash
pip install -r requirements.txt
```

Installe et lance [Ollama](https://ollama.ai/), puis tire le modèle :

```bash
ollama pull qwen3:4b
ollama serve
```

## Structure du projet

```
├── 01_scan_rapide.ipynb         # Scan multi-paires
├── 02_signal_paire.ipynb        # Analyse d'une paire
├── 03_exemple_multi_tf.ipynb    # Exemple fixe EURUSD
├── lib/
│   ├── config.py                # Paires, timeframes, noms
│   ├── data.py                  # Fetch OpenBB + cache pickle
│   ├── analysis.py              # S/R, structure, patterns, signal
│   └── ai.py                    # Analyse IA via Ollama
├── doc/
│   ├── support_resistance.md    # Algorithme S/R
│   ├── signal_generation.md     # Pipeline complet
│   └── signal_parameters.md     # Paramètres du signal IA
├── data_cache/                  # Cache des données (60 min TTL)
├── _archive/                    # Anciens notebooks obsolètes
├── requirements.txt
└── README.md
```

## Pipeline

1. **Données** — `lib/data.py` : fetch via `obb.currency.price.historical()`, cache pickle 60 min
2. **Analyse** — `lib/analysis.py` : S/R adaptatif (ATR + pivot clustering), structure de marché, patterns bougies
3. **Signal** — Signal combiné multi-timeframe envoyé à Ollama
4. **IA** — `lib/ai.py` : Qwen 3:4B, réponse JSON avec signal (BUY/SELL/HOLD), entrée, SL, TP

## Configuration

Éditer `lib/config.py` pour changer les paires ou les timeframes.

Le modèle Ollama se change dans `lib/ai.py` :
```python
MODEL = "qwen3:4b"  # → qwen3:7b, llama3:8b, etc.
```

## Avertissement

Outil éducatif uniquement. Les signaux générés ne sont pas des conseils financiers.
