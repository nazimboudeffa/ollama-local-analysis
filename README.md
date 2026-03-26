# 📊 Forex Trading Analysis with Local AI

An automated forex trading analysis system that uses local AI models (via Ollama) to analyze EUR/USD market data and provide trading signals. The system combines technical indicators (RSI, MACD) with AI-powered decision making, running completely offline on your local machine.

## ✨ Features

### Two Analysis Approaches:

#### 1️⃣ **Technical Indicators Analysis** (`trading-analysis.ipynb`)
- RSI (Relative Strength Index) with oversold/overbought detection
- MACD (Moving Average Convergence Divergence)
- 20-period Moving Average for trend detection
- Focuses on mathematical indicators and momentum

#### 2️⃣ **Price Action Analysis** (`price-action-analysis.ipynb`) 🆕
- Candlestick pattern detection (Doji, Hammer, Engulfing, Shooting Star)
- Support and Resistance level identification
- Market structure analysis (Higher Highs, Lower Lows)
- Pure price movement focus without indicators
- Entry/Stop-Loss/Take-Profit suggestions

### Common Features:
- **Local AI Analysis**: Uses Ollama with Qwen 3:4B model for trading signal generation
- **Smart Caching**: Caches market data for 5 minutes to avoid redundant API calls
- **Session-Aware**: Considers forex trading sessions (London, New York, Asian)
- **Visual Analytics**: Beautiful matplotlib charts with key levels
- **Human-Readable Output**: Color-coded signals with confidence levels and recommendations

## 🔧 Requirements

### System Requirements
- Python 3.8 or higher
- 4GB+ RAM (for running Ollama models)
- Windows/Linux/macOS

### Software Requirements
- [Ollama](https://ollama.ai/) - Local AI model runtime
- Jupyter Notebook or JupyterLab

## 📦 Installation

### 1. Install Ollama

**Windows:**
```bash
# Download and install from: https://ollama.ai/download
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Pull the AI Model

```bash
ollama pull qwen3:4b
```

### 3. Start Ollama Server

```bash
ollama serve
```

The server should now be running at `http://localhost:11434`

### 4. Install Python Dependencies

```bash
pip install yfinance pandas ta requests matplotlib pickle-mixin
```

Or using the requirements file (if available):
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Model Configuration

Edit the configuration in the notebook (Cell 2):

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:4b"  # Change to your preferred Ollama model

# Cache settings
CACHE_DIR = Path("data_cache")
CACHE_DURATION_MINUTES = 60  # Adjust cache duration (in minutes)
```

### Available Ollama Models

You can use other models by pulling them first:
```bash
# Smaller, faster models
ollama pull qwen3:1.8b
ollama pull phi3:mini

# Larger, more accurate models
ollama pull qwen3:7b
ollama pull llama3:8b
```

Then update the `MODEL` variable in Cell 2 of the notebook.

## 🚀 Usage

### Basic Usage

1. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

2. **Open a notebook**:
   
   For technical indicators analysis:
   ```bash
   jupyter notebook trading-analysis.ipynb
   ```
   
   For price action analysis:
   ```bash
   jupyter notebook price-action-analysis.ipynb
   ```

3. **Run all cells** (Cell → Run All) or run them sequentially

### Example Output - Technical Indicators

```
============================================================
📊 FOREX TRADING ANALYSIS - EUR/USD
============================================================

📈 MARKET DATA:
   Price:        1.15514
   Session:      London
   Volatility:   LOW

📉 TECHNICAL INDICATORS:
   RSI:          31.34 (OVERSOLD 🔴)
   MACD:         BEARISH 🔴
   Trend:        DOWNTREND 📉

🤖 AI ANALYSIS:
   Signal:       HOLD 🟡
   Confidence:   65% (MEDIUM)
   Reason:       Downtrend with oversold RSI, wait for reversal

============================================================
💡 RECOMMENDATION: HOLD position - Wait for better setup
============================================================
```

Plus visual charts showing price action, RSI, and MACD.

### Example Output - Price Action

```
======================================================================
📊 PRICE ACTION ANALYSIS - EUR/USD
======================================================================

🏗️  MARKET STRUCTURE:
   Structure:       Downtrend (Lower Lows)
   Bias:            Bearish 📉
   Price Range:     0.45%

💰 CURRENT PRICE:
   Price:           1.15514
   Session:         London

🎯 KEY LEVELS:
   Resistance:      1.15680 (Strong)
   Distance:        +0.14% 🔴
   Support:         1.15320 (Medium)
   Distance:        -0.17% 🟢

🕯️  RECENT CANDLESTICK PATTERNS:
   • Doji (Indecision)
   • Bearish Engulfing (Bearish Reversal)

🤖 AI PRICE ACTION ANALYSIS:
   Signal:          SELL 🔴
   Confidence:      72% (HIGH)
   Reason:          Bearish engulfing at resistance level
   Entry:           1.15500
   Stop Loss:       1.15700
   Take Profit:     1.15300
======================================================================
```

Plus candlestick chart with support/resistance levels highlighted.

## 📁 Project Structure

```
ollama-local-analysis/
├── trading-analysis.ipynb      # Technical indicators analysis (RSI, MACD)
├── price-action-analysis.ipynb # Price action analysis (patterns, S/R levels) 🆕
├── data_cache/                 # Cached market data (auto-created)
│   └── EURUSD_X_5m_1d.pkl     # Cached EUR/USD data
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .gitignore                 # Git ignore rules
```

## 🎯 Which Notebook to Use?

### Use `trading-analysis.ipynb` when:
- ✓ You prefer indicator-based trading
- ✓ You want momentum confirmation (RSI, MACD)
- ✓ You're looking for overbought/oversold conditions
- ✓ You prefer systematic, rules-based analysis

### Use `price-action-analysis.ipynb` when:
- ✓ You prefer pure price movement analysis
- ✓ You want to identify key support/resistance levels
- ✓ You trade based on candlestick patterns
- ✓ You need precise entry/stop-loss/take-profit levels
- ✓ You want to understand market structure

### Use both for:
- ✓ **Confirmation**: When both approaches agree, signals are stronger
- ✓ **Complete picture**: Technical + Price Action = comprehensive analysis

## 🔄 Caching System

The system caches yfinance data to improve performance:

- **Cache Location**: `data_cache/` directory
- **Cache Duration**: 5 minutes (configurable)
- **Auto-Refresh**: Automatically downloads fresh data when cache expires
- **Visual Feedback**: Shows cache status on each run

Example output:
```
✓ Using cached data (age: 2m 15s)  # Using cache
⬇ Downloading fresh data for EURUSD=X...  # Fresh download
```

To clear the cache manually:
```bash
# Windows
rmdir /s data_cache

# Linux/macOS
rm -rf data_cache
```

## 🎨 Customization

### Change Currency Pair

Modify the `fetch_data()` function (Cell 4):

```python
df = get_cached_data("GBPUSD=X", interval="5m", period="1d")  # GBP/USD
df = get_cached_data("USDJPY=X", interval="5m", period="1d")  # USD/JPY
```

### Adjust Technical Indicators

Modify parameters in `fetch_data()` (Cell 4):

```python
# Change RSI window
df["rsi"] = ta.momentum.RSIIndicator(close=df["Close"], window=21).rsi()

# Adjust MACD parameters
macd = ta.trend.MACD(close=df["Close"], window_slow=26, window_fast=12, window_sign=9)
```

### Modify AI Prompt

Edit the prompt in `analyze_signal()` function (Cell 6) to change AI behavior:

```python
prompt = f"""You are an aggressive forex day trader looking for opportunities.
Analyze this data and provide a trading signal...
"""
```

## 🐛 Troubleshooting

### Ollama Connection Error

**Error**: `Cannot connect to Ollama at http://localhost:11434`

**Solution**:
```bash
# Check if Ollama is running
curl http://localhost:11434

# If not running, start it
ollama serve
```

### Model Not Found

**Error**: `model 'qwen3:4b' not found`

**Solution**:
```bash
ollama pull qwen3:4b
```

### Empty Response from LLM

**Solution**:
1. Increase token limit in Cell 6:
   ```python
   "num_predict": 500  # Increase to 1000
   ```
2. Try a different model
3. Simplify the prompt

### yfinance Download Issues

**Solution**:
1. Check your internet connection
2. Clear cache: `rm -rf data_cache`
3. Try a different period: `period="5d"` instead of `period="1d"`

## 📊 Technical Indicators Explained

### RSI (Relative Strength Index)
- **< 30**: Oversold (potential buy signal)
- **> 70**: Overbought (potential sell signal)
- **30-70**: Neutral zone

### MACD
- **Bullish**: MACD line above signal line (upward momentum)
- **Bearish**: MACD line below signal line (downward momentum)

### Trend Detection
- **Uptrend**: Price above 20-period moving average
- **Downtrend**: Price below 20-period moving average

## 🕯️ Price Action Concepts Explained

### Candlestick Patterns

#### Reversal Patterns
- **Doji**: Small body, equal length wicks - indicates indecision
- **Hammer**: Small body at top, long lower wick - bullish reversal signal
- **Shooting Star**: Small body at bottom, long upper wick - bearish reversal signal
- **Bullish Engulfing**: Large green candle that engulfs previous red candle - strong bullish signal
- **Bearish Engulfing**: Large red candle that engulfs previous green candle - strong bearish signal

### Support & Resistance
- **Support**: Price level where buying pressure prevents further decline
- **Resistance**: Price level where selling pressure prevents further rise
- **Strength**: Determined by number of times price touched the level (more touches = stronger)

### Market Structure
- **Uptrend**: Series of higher highs and higher lows
- **Downtrend**: Series of lower highs and lower lows
- **Consolidation**: Price moving sideways in a range

### Trade Management
- **Entry**: Optimal price to enter the trade
- **Stop Loss**: Price level to exit if trade goes against you (risk management)
- **Take Profit**: Target price to secure profits

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📝 License

This project is for educational purposes. Use at your own risk. Not financial advice.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. The trading signals generated are not financial advice. Always do your own research and consult with financial professionals before making trading decisions.
