# Analyse avancée multi-timeframe (`04_signal_avance.ipynb`)

Analyse approfondie d'**une seule paire** sur 4 timeframes (M15, H1, Daily, Weekly) produisant un **signal YAML enrichi** envoyé à un LLM local (Ollama) qui répond en **Markdown**.

Contrairement aux notebooks `01`/`02`/`03` (prompt JSON + parsing), `04` construit un signal beaucoup plus riche : tendance avec score, EMA, Smart Money (Order Blocks, FVG, liquidité), chandeliers avec index de bougie, probabilités bull/bear, zones d'entrée et gestion du risque ATR.

---

## 1. Architecture du notebook (11 cellules)

| Cellule | Contenu |
|---|---|
| 0 | Configuration : `SYMBOL`, `FULL_NAME`, timeframes `TFS` |
| 1 | Imports (pandas, numpy, `ta`, `yaml`, `requests`, `lib.*`) |
| 2 | Téléchargement des données (cache 60 min) pour les 4 timeframes |
| 3 | Indicateurs par timeframe + définition `PIP_SIZE` / `pips()` |
| 4 | Structure, tendance (score), EMA, volume, volatilité |
| 5 | Détection de patterns candlestick enrichie (index de bougie) |
| 6 | Smart Money : Order Blocks, FVG, liquidité |
| 7 | Supports / résistances les plus proches (distance en pips) |
| 8 | Scoring probabiliste, synthèse, zones d'entrée, risque |
| 9 | Construction du signal YAML enrichi + affichage |
| 10 | Envoi à l'IA (prompt analyste, réponse Markdown brute) |

---

## 2. Configuration

```python
SYMBOL = "EURUSD"      # USDJPY, GBPUSD, USDCHF, AUDUSD, USDCAD, NZDUSD...
FULL_NAME = "EUR/USD"

TFS = {
    "M15":    {"interval": "15m", "period": "5d"},
    "H1":     {"interval": "1h",  "period": "1mo"},
    "Daily":  {"interval": "1d",  "period": "1y"},
    "Weekly": {"interval": "1W",  "period": "2y"},
}
```

> **Note** : yfinance ne supporte pas l'intervalle `4h`. Le timeframe hebdomadaire (`1W`, 2 ans) est utilisé à la place.

### Taille d'un pip

```python
PIP_SIZE = 0.01 if "JPY" in SYMBOL else 0.0001
```

Les paires JPY ont 2 décimales (USDJPY = 157.39), les autres 4 (EURUSD = 1.1527).

---

## 3. Indicateurs calculés par timeframe (`compute_indicators`)

Calculés avec la bibliothèque `ta` sur chaque timeframe :

| Indicateur | Paramètres | Signification |
|---|---|---|
| **ATR** | ATR 14 | Volatilité moyenne |
| **ADX** | ADX 14 | Force de la tendance (≥ 25 = tendance) |
| **DI+ / DI-** | ADX 14 | Direction de la force (mouvement) |
| **RSI** | RSI 14 | Momentum (surachat > 70, survente < 30) |
| **MACD** | 12/26/9 | Croisement + signal |
| **Momentum** | ROC 12 | Variation en % sur 12 barres |
| **EMA** | 20, 50, 100, 200 | Moyennes mobiles exponentielles |

---

## 4. Tendance (direction + force + score)

```python
score = 0.0
if macd_bull: score += 1.0   else: score -= 1.0
if rsi > 55:  score += 1.0
elif rsi < 45: score -= 1.0
if close > ema20: score += 1.0  else: score -= 1.0
if di_pos > di_neg: score += 0.5  else: score -= 0.5
```

| Résultat | Valeur |
|---|---|
| `direction` | `Bullish` si score ≥ 1.5, `Bearish` si ≤ -1.5, sinon `Neutral` |
| `strength` | `Strong` si ADX ≥ 30, `Moderate` si ≥ 20, sinon `Weak` |
| `score` | arrondi à 0.1 |

La **structure de marché** (`analyze_market_structure`) donne par ailleurs :
`Uptrend (Higher Highs)` / `Downtrend (Lower Lows)` / `Consolidation (Ranging)`.

---

## 5. Analyse EMA

Calculée sur Daily et H1 uniquement :

```python
alignement Bullish : EMA20 > EMA50 > EMA100 > EMA200
alignement Bearish : EMA20 < EMA50 < EMA100 < EMA200
sinon               : Mixed
```

`price_position` = nombre d'EMA sous le prix courant :

| Compteur (EMA sous le prix) | Position |
|---|---|
| 4 | `Above EMA20` |
| 3 | `Between EMA20 and EMA50` |
| 2 | `Between EMA50 and EMA100` |
| 1 | `Between EMA100 and EMA200` |
| 0 | `Below EMA200` |

---

## 6. Volume et volatilité

- **Volume** : le forex n'a pas de volume réel (données yfinance ≈ 0). Le signal expose donc `available: false`, `tick_volume: null`, `trend: Unknown`. Le code supporte quand même le cas où un volume existe.
- **Volatilité** : comparaison de l'ATR daily courant à la moyenne mobile 14 de l'ATR :

```python
ATR_last > mean * 1.2  → "High"
ATR_last < mean * 0.8  → "Low"
sinon                   → "Medium"
```

---

## 7. Patterns candlestick enrichis (M15)

`detect_patterns_avances()` — fenêtre de 10 bougies, chaque pattern porte l'**index de bougie** (négatif : -1 = dernière bougie) :

| Pattern | Condition (sur le corps/ombres) | Signal |
|---|---|---|
| Doji | corps / range < 0.1 | Indecision |
| Hammer | ombre basse > 2×corps, ombre haute < corps | Bullish Reversal |
| Shooting Star | ombre haute > 2×corps, ombre basse < corps | Bearish Reversal |
| Pin Bar | ombres haute ET basse > 2×corps | Reversal |
| Bullish Engulfing | barre verte engloutit la barre rouge précédente | Bullish Reversal |
| Bearish Engulfing | barre rouge engloutit la verte précédente | Bearish Reversal |
| Inside Bar | H ≤ H_prev et L ≥ L_prev | Compression |
| Outside Bar | H ≥ H_prev et L ≤ L_prev | Expansion |
| Morning Star | bougie étoile + 3ᵉ barre > milieu de la 1ʳᵉ | Bullish Reversal |

---

## 8. Smart Money Concepts

### Order Blocks (sur H1)

```python
move = close[i+1] - close[i]
if  move > +1.5 * ATR and bougie[i] baissière  → Order Block HAUSSIER  (high[i])
elif move < -1.5 * ATR and bougie[i] haussière  → Order Block BAISSIER  (low[i])
```

Un mouvement fort (+1.5 ATR) après une bougie d'absorption signale la zone de départ du mouvement.

- Déduplication (arrondi à 5 décimales)
- Niveaux présents **dans les deux** listes → `role_change_levels` (servent de support **et** de résistance)

### Fair Value Gaps (FVG) (sur H1)

Déséquilibre entre 3 bougies (fenêtre 40) :

```python
l2 > h1  → FVG haussier, zone (h1, l2)
h2 < l1  → FVG baissier, zone (h2, l1)
```

### Liquidité (sur M15)

```python
tol = 0.5 × ATR
equal_highs = plus grand nombre de highs à moins de tol l'un de l'autre
equal_lows  = idem pour les lows
liquidity_above = equal_highs >= 2
liquidity_below = equal_lows >= 2
sweep_above     = dernier high > max(highs précédents)   # chasse au-dessus
sweep_below     = dernier low  < min(lows précédents)    # chasse en dessous
```

---

## 9. Supports / Résistances proches

Depuis les niveaux M15 (`find_support_resistance`) :

- support le plus proche **sous** le prix, résistance la plus proche **au-dessus**
- distance convertie en **pips** avec `pips()`

---

## 10. Scoring probabiliste, décision et risque

### Facteurs directionnels (6)

| Facteur | Bull si | Bear si |
|---|---|---|
| EMA Daily alignment | Bullish | Bearish |
| Position du prix Daily | Above EMA20 / Between EMA20-50 | Between EMA100-200 / Below EMA200 |
| MACD Daily | bullish | bearish |
| RSI Daily | > 50 | < 50 |
| Tendance H1 | Bullish | Bearish |
| Tendance M15 | Bullish | Bearish |

### Probabilités et confiance

```python
bull_pct   = 100 × bull_score / total
bear_pct   = 100 - bull_pct
confidence = 100 × max(bull_score, bear_score) / total
# bonus tendance :
#   Strong  → +10   (plafond 95)
#   Moderate → +5   (plafond 95)
```

### Décision

```python
if abs(bull_score - bear_score) <= 1 → HOLD
else → BUY si bull > bear, sinon SELL
```

### Force du signal

```python
strength = None si HOLD
         = "Weak" si confidence < 65
         = "Moderate" si < 80
         = "Strong" sinon
```

### Zones d'entrée

```python
buy_zone  = Order Blocks haussiers < prix  + support le plus proche   (top 2, tri décroissant)
sell_zone = Order Blocks baissiers > prix + résistance la plus proche (top 2, tri croissant)
```

### Gestion du risque (basée sur ATR M15)

```python
SL = 1.5 × ATR(M15)
TP = 2.5 × ATR(M15)
RR = TP / SL = 1.67

BUY  → entry = prix, SL = prix - 1.5×ATR, TP = prix + 2.5×ATR
SELL → entry = prix, SL = prix + 1.5×ATR, TP = prix - 2.5×ATR
HOLD → entry = SL = TP = null
```

---

## 11. Structure du YAML généré

```
pair
├── price          current, spread
├── session        name
├── timeframes     analyzed, interval, period
├── structure      M15/H1/Daily/Weekly
├── trend          direction, strength, score (par TF)
├── volatility     daily_atr_vs_14d_mean
├── atr            M15/H1/Daily/Weekly
├── indicators     RSI, MACD, ADX, DI+, DI-, Momentum (par TF) + Volume
├── ema            Daily/H1 : alignment, price_position, EMA20/50/100/200
├── support        nearest : exists, price, strength, distance_pips, reason
├── resistance     nearest : idem
├── smart_money    order_blocks (bullish/bearish/role_change_levels),
│                  liquidity (equal_highs/lows, liquidity_above/below, sweeps),
│                  fvg (bullish/bearish : exists, zone)
├── candlestick    patterns.recent (candle, pattern, signal), timeframe
├── probabilities  bull_score, bear_score, factors_total, scale, confidence
├── signals        confluence, confidence
├── analysis       direction, strength, confidence, reasons
├── entry          buy_zone, sell_zone
├── risk           atr_reference, atr_pips, direction, entry,
│                  stop_loss, take_profit, rr, note
└── news           high_impact_today (à remplir manuellement : NFP, CPI...)
```

### Exemple réel (EURUSD, juillet 2026)

```yaml
pair: EURUSD (EUR/USD)
price:
  current: 1.15274
  spread: 0.8
session:
  name: New York
trend:
  M15: {direction: Bearish, strength: Moderate, score: -1.5}
  H1: {direction: Bullish, strength: Moderate, score: 3.5}
  Daily: {direction: Bullish, strength: Moderate, score: 3.5}
  Weekly: {direction: Bearish, strength: Weak, score: -2.5}
atr: {M15: 0.000643, H1: 0.001494, Daily: 0.006143, Weekly: 0.013744}
indicators:
  RSI: {M15: 51.2, H1: 56.4, Daily: 61.2, Weekly: 48.0}
  MACD: {M15: Bearish, H1: Bullish, Daily: Bullish, Weekly: Bearish}
ema:
  Daily: {alignment: Bearish, price_position: Between EMA50 and EMA100}
  H1: {alignment: Bullish, price_position: Above EMA20}
support:
  nearest: {exists: true, price: 1.15088, strength: Strong, distance_pips: 18.6}
resistance:
  nearest: {exists: false, price: null, reason: No resistance identified above current price}
smart_money:
  order_blocks:
    bullish: [1.15062]
    bearish: [1.15088]
    role_change_levels: [1.14863]
  liquidity:
    equal_highs: 10
    equal_lows: 12
    liquidity_above: true
    liquidity_below: true
  fvg:
    bullish: {exists: true, zone: {low: 1.15221, high: 1.15287}}
    bearish: {exists: true, zone: {low: 1.15274, high: 1.153}}
probabilities: {bull_score: 60, bear_score: 40, factors_total: 5, confidence: 65}
analysis:
  direction: HOLD
  confidence: 65
  reasons: [MACD bullish (Daily), RSI > 50 (Daily), H1 trend Bullish, Score too close (3 vs 2)]
entry:
  buy_zone: [1.15088, 1.15062]
  sell_zone: []
risk: {atr_pips: 6.4, stop_loss: null, take_profit: null, rr: 1.67}
```

---

## 12. Passage à l'IA

Le YAML est sérialisé (`yaml.dump`) et injecté dans le prompt (cf. [prompt_ia.md](prompt_ia.md)). La réponse du modèle est **Markdown brut** affiché tel quel :

```python
ai_result = ask_ai(yaml.dump(signal_yaml, sort_keys=False, allow_unicode=True))
```

Paramètres de l'appel :

| Paramètre | Valeur |
|---|---|
| `model` | `gemma4` (configurable dans `lib/ai.py`) |
| `stream` | `false` |
| `format` | **non défini** (réponse texte libre, pas de JSON forcé) |
| `temperature` | 0.2 |
| `num_predict` | 2500 (réponse longue en Markdown) |
| `timeout` | 120 s |

---

## Fichiers impliqués

| Fichier | Rôle |
|---|---|
| `04_signal_avance.ipynb` | Notebook d'analyse avancée |
| `lib/data.py` | Fetch OpenBB + cache |
| `lib/analysis.py` | Structure de marché, S/R |
| `lib/ai.py` | `MODEL`, `OLLAMA_URL` |
| `doc/prompt_ia.md` | Prompt analyste (sortie Markdown) |
