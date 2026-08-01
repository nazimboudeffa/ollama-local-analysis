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
| `04_signal_price_action.ipynb` | Analyse Price Action pure — 4 timeframes, Smart Money, rapport Markdown enregistré dans `rapports_ia/` |

## Installation

```bash
pip install -r requirements.txt
```

Installe et lance [Ollama](https://ollama.ai/), puis tire le modèle :

```bash
ollama pull gemma4
ollama serve
```

## Structure du projet

```
├── 01_scan_rapide.ipynb         # Scan multi-paires
├── 02_signal_paire.ipynb        # Analyse d'une paire
├── 03_exemple_multi_tf.ipynb    # Exemple fixe EURUSD
├── 04_signal_price_action.ipynb # Analyse Price Action pure + rapport IA
├── lib/
│   ├── config.py                # Paires, timeframes, noms
│   ├── data.py                  # Fetch OpenBB + cache pickle
│   ├── analysis.py              # S/R, structure, patterns, signal
│   └── ai.py                    # Analyse IA via Ollama
├── doc/
│   ├── README.md                # Index de la documentation (ordre de lecture)
│   ├── signal_generation.md     # Pipeline complet
│   ├── signal_parameters.md     # Paramètres du signal IA
│   ├── indicateurs_techniques.md# Math des indicateurs
│   ├── support_resistance.md    # Algorithme S/R
│   ├── candlestick_patterns.md  # Patterns de chandeliers
│   ├── analyse_avancee.md       # Notebook 04 (Price Action)
│   └── prompt_ia.md             # Prompt Price Action (Markdown)
├── rapports_ia/                 # Rapports IA (date_modèle_paire.md)
├── data_cache/                  # Cache des données (60 min TTL)
├── _archive/                    # Anciens notebooks obsolètes
├── requirements.txt
└── README.md
```

## Pipeline

1. **Données** — `lib/data.py` : fetch via `obb.currency.price.historical()`, cache pickle 60 min
2. **Analyse** — `lib/analysis.py` : S/R adaptatif (ATR + pivot clustering), structure de marché, patterns bougies
3. **Signal** — Signal combiné multi-timeframe envoyé à Ollama
4. **IA** — `lib/ai.py` : `gemma4` (réponse JSON pour 01/02/03), ou prompt Price Action Markdown dans `04_signal_price_action.ipynb`

## Configuration

Éditer `lib/config.py` pour changer les paires ou les timeframes.

Le modèle Ollama se change dans `lib/ai.py` :
```python
MODEL = "gemma4"  # → gemma3:12b, llama3:8b, etc.
```

## AVERTISSEMENT IMPORTANT

> [!WARNING]
> **PROJET STRICTEMENT EDUCATIF ET EXPERIMENTAL**
>
> Ce projet est fourni exclusivement a des fins d'apprentissage, de demonstration technique et d'experimentation. Il ne constitue **en aucun cas** un conseil en investissement, une recommandation financiere, une incitation a acheter ou vendre un actif, ni une promesse de performance.
>
> Tout algorithme de trading, aussi convaincant, sophistique ou automatise soit-il, peut produire des signaux faux, tardifs, incoherents ou desastreux dans des conditions de marche reelles. Les marches financiers sont volatils, imprevisibles et peuvent reagir brutalement a des evenements que le modele ne comprend pas, n'anticipe pas ou interprete mal.
>
> **Vous pouvez perdre une partie importante de votre capital, voire la totalite de l'argent engage.** Cela inclut les pertes liees aux faux signaux, aux erreurs de parametrage, aux biais de donnees, aux problemes techniques, a la latence, aux conditions de liquidite, au spread, au slippage, a l'effet de levier et a toute defaillance logicielle ou humaine.
>
> N'utilisez jamais cet outil avec de l'argent que vous ne pouvez pas vous permettre de perdre integralement. Si vous choisissez de vous en servir dans un contexte reel, vous le faites **a vos seuls risques**, sous votre **entiere responsabilite**.
>
> En resume : **ce projet peut vous aider a explorer des idees, pas a securiser votre argent.** Si vous cherchez une garantie, il n'y en a aucune.
