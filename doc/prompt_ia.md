# Prompt d'analyse IA (`04_signal_avance.ipynb` — cellule 10)

Le prompt utilisé dans `04_signal_avance.ipynb` transforme le modèle local en **analyste professionnel Forex / Price Action / Smart Money Concepts (SMC)**. Contrairement à l'ancien prompt (`lib/ai.py`, sortie JSON), celui-ci impose une **réponse en Markdown structurée** et une méthode d'analyse complète en 8 étapes.

---

## 1. Règles importantes

- Analyser **uniquement** les données fournies, n'inventer **jamais** une donnée absente.
- Information absente ou `null` → indiquer « indisponible ».
- Indicateurs contradictoires → privilégier la **prudence** et **réduire la confiance**.
- Les timeframes supérieurs ont toujours plus de poids : **Weekly > Daily > H1 > M15**.
- Décision finale justifiée par une **confluence de facteurs**, pas un seul indicateur.
- **Consolidation → HOLD**, sauf cassure ou confluence exceptionnelle.
- **RR < 1.5 → HOLD**.
- Ne jamais forcer un BUY ou un SELL.

---

## 2. Méthode d'analyse (8 étapes imposées)

1. **Contexte général** — tendance dominante, structure de marché, alignement des timeframes.
2. **Momentum** — RSI, MACD, ADX, DI+, DI-, Momentum → haussier / baissier / neutre / perte de momentum.
3. **Volatilité** — ATR, volatilité → objectifs réalistes ou non.
4. **EMA** — alignement, position du prix, tendance.
5. **Smart Money** — Order Blocks, Liquidité, Equal Highs/Lows, Liquidity Sweeps, FVG → chasse à la liquidité probable ?
6. **Supports / Résistances** — proximité, qualité, risque de rebond / de cassure.
7. **Chandeliers** — patterns récents, plus de poids aux plus récents.
8. **Confluence** — liste des facteurs `+` / `-` puis confiance 0–100.

Exemple de confluence fourni au modèle :

```
+ MACD Daily Bullish
+ RSI H1 > 50
+ EMA H1 Bullish
+ Support Daily Strong
- Weekly Bearish
- Momentum M15 négatif
```

---

## 3. Décision

Une seule décision possible : **BUY / SELL / HOLD**.

| Décision | Conditions |
|---|---|
| **BUY** | plusieurs timeframes haussiers + momentum favorable + confluence élevée + RR ≥ 1.5 |
| **SELL** | plusieurs timeframes baissiers + momentum baissier + confluence élevée + RR ≥ 1.5 |
| **HOLD** | sinon |

### Si BUY ou SELL

Calculer : Entrée, Stop Loss, **Take Profit 1 / 2 / 3**, Risk Reward.

- **SL cohérent avec** : ATR, Support/Résistance, Smart Money, Structure.
- **TP cohérents avec** : ATR, Supports, Résistances, FVG, Liquidité.

---

## 4. Format de réponse (Markdown)

```markdown
# Résumé
- Décision :
- Confiance :
- Tendance dominante :
- Structure :

# Analyse
## Tendances
...
## Momentum
...
## Smart Money
...
## Supports / Résistances
...
## Confluence
...

# Signal
Action : BUY / SELL / HOLD
Entrée :
Stop Loss :
Take Profit 1 :
Take Profit 2 :
Take Profit 3 :
Risk Reward :

# Justification
```

Contraintes finales :
- Ne jamais inventer une valeur.
- Ne jamais utiliser d'informations extérieures au YAML.
- Toujours expliquer les **contradictions** entre indicateurs.

---

## 5. Intégration dans le notebook

Le YAML du signal est sérialisé puis injecté à la fin du prompt :

```python
prompt = f"""{...méthode et règles ci-dessus...}
==========================
Données (YAML)
==========================
{yaml_text}"""
```

Appel Ollama :

```python
requests.post(OLLAMA_URL, json={
    "model": MODEL,               # gemma4 (lib/ai.py)
    "prompt": prompt,
    "stream": False,
    "options": {"temperature": 0.2, "num_predict": 2500},
}, timeout=120)
```

La réponse (Markdown) est affichée brute.

---

## 6. Différences avec l'ancien prompt (`lib/ai.py`)

| Aspect | Ancien (`lib/ai.py`, 01/02/03) | Nouveau (`04_signal_avance.ipynb`) |
|---|---|---|
| Rôle du modèle | Générateur de signal | Analyste professionnel (SMC) |
| Format de sortie | JSON forcé (`format: json`) | **Markdown** structuré |
| Analyse | Simple (prix + règles SL/TP) | 8 étapes complètes |
| Confluence | Absente | Liste de facteurs + confiance 0–100 |
| TP multiples | Un seul TP | **TP1 / TP2 / TP3** |
| Règles de décision | Implicites | Explicites (RR ≥ 1.5, consolidation → HOLD…) |
| `num_predict` | 500 | 2500 |
| `temperature` | 0.1 | 0.2 |

> `01_scan_rapide.ipynb`, `02_signal_paire.ipynb` et `03_exemple_multi_tf.ipynb` continuent d'utiliser l'ancien prompt JSON via `lib/ai.py`.
