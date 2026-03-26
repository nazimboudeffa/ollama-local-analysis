# 📊 Forex Trading Analysis with Local AI

An automated forex trading analysis system that uses local AI models (via Ollama) to analyze EUR/USD market data and provide trading signals. The system combines technical indicators (RSI, MACD) with AI-powered decision making, running completely offline on your local machine.

## ✨ Features

- **Local AI Analysis**: Uses Ollama with Qwen 3:4B model for trading signal generation
- **Technical Indicators**: 
  - RSI (Relative Strength Index) with oversold/overbought detection
  - MACD (Moving Average Convergence Divergence)
  - 20-period Moving Average for trend detection
- **Smart Caching**: Caches market data for 5 minutes to avoid redundant API calls
- **Session-Aware**: Considers forex trading sessions (London, New York, Asian)
- **Visual Analytics**: Beautiful matplotlib charts with technical indicators
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
CACHE_DURATION_MINUTES = 5  # Adjust cache duration (in minutes)
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

2. **Open the notebook**:
   ```bash
   jupyter notebook trading-analysis.ipynb
   ```

3. **Run all cells** (Cell → Run All) or run them sequentially:
   - Cell 1-6: Setup and function definitions
   - Cell 7: Execute analysis and display results
   - Cell 8: Display charts (optional)

### What You'll See

The analysis output includes:

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

## 📁 Project Structure

```
ollama-local-analysis/
├── trading-analysis.ipynb   # Main analysis notebook
├── data_cache/              # Cached market data (auto-created)
│   └── EURUSD_X_5m_1d.pkl  # Cached EUR/USD data
├── README.md                # This file
└── .gitignore              # Git ignore rules
```

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

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📝 License

This project is for educational purposes. Use at your own risk. Not financial advice.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. The trading signals generated are not financial advice. Always do your own research and consult with financial professionals before making trading decisions.
