import pandas as pd


def detect_candlestick_patterns(df):
    patterns = []

    for i in range(1, len(df)):
        open_price = df['Open'].iloc[i]
        close_price = df['Close'].iloc[i]
        high = df['High'].iloc[i]
        low = df['Low'].iloc[i]
        prev_close = df['Close'].iloc[i-1]

        body = abs(close_price - open_price)
        range_size = high - low

        if range_size == 0:
            continue

        if body / range_size < 0.1:
            patterns.append({
                'index': i,
                'pattern': 'Doji',
                'signal': 'Indecision',
                'strength': 'Medium'
            })

        upper_wick = high - max(open_price, close_price)
        lower_wick = min(open_price, close_price) - low

        if lower_wick > 2 * body and upper_wick < body:
            patterns.append({
                'index': i,
                'pattern': 'Hammer',
                'signal': 'Bullish Reversal',
                'strength': 'Strong'
            })

        if upper_wick > 2 * body and lower_wick < body:
            patterns.append({
                'index': i,
                'pattern': 'Shooting Star',
                'signal': 'Bearish Reversal',
                'strength': 'Strong'
            })

        if i >= 1:
            prev_open = df['Open'].iloc[i-1]
            prev_close = df['Close'].iloc[i-1]

            if (prev_close < prev_open and
                close_price > open_price and
                open_price < prev_close and
                close_price > prev_open):
                patterns.append({
                    'index': i,
                    'pattern': 'Bullish Engulfing',
                    'signal': 'Bullish Reversal',
                    'strength': 'Very Strong'
                })

            if (prev_close > prev_open and
                close_price < open_price and
                open_price > prev_close and
                close_price < prev_open):
                patterns.append({
                    'index': i,
                    'pattern': 'Bearish Engulfing',
                    'signal': 'Bearish Reversal',
                    'strength': 'Very Strong'
                })

    return patterns


def find_support_resistance(df, window=10, threshold=0.0002):
    levels = []

    for i in range(window, len(df) - window):
        if df['High'].iloc[i] == df['High'].iloc[i-window:i+window+1].max():
            level = df['High'].iloc[i]
            if not any(abs(level - l['level']) / level < threshold for l in levels):
                touches = sum(abs(df['High'] - level) / level < threshold)
                levels.append({
                    'level': level,
                    'type': 'Resistance',
                    'touches': touches,
                    'strength': 'Strong' if touches >= 3 else 'Medium' if touches >= 2 else 'Weak'
                })

        if df['Low'].iloc[i] == df['Low'].iloc[i-window:i+window+1].min():
            level = df['Low'].iloc[i]
            if not any(abs(level - l['level']) / level < threshold for l in levels):
                touches = sum(abs(df['Low'] - level) / level < threshold)
                levels.append({
                    'level': level,
                    'type': 'Support',
                    'touches': touches,
                    'strength': 'Strong' if touches >= 3 else 'Medium' if touches >= 2 else 'Weak'
                })

    levels.sort(key=lambda x: x['touches'], reverse=True)
    return levels[:5]


def analyze_market_structure(df):
    recent = df.tail(20)

    highs = recent['High'].values
    lows = recent['Low'].values

    higher_highs = sum(1 for i in range(1, len(highs)) if highs[i] > highs[i-1])
    lower_lows = sum(1 for i in range(1, len(lows)) if lows[i] < lows[i-1])

    if higher_highs > lower_lows * 1.5:
        structure = "Uptrend (Higher Highs)"
        bias = "Bullish"
    elif lower_lows > higher_highs * 1.5:
        structure = "Downtrend (Lower Lows)"
        bias = "Bearish"
    else:
        structure = "Consolidation (Ranging)"
        bias = "Neutral"

    price_range = (recent['High'].max() - recent['Low'].min()) / recent['Close'].iloc[-1]

    return {
        'structure': structure,
        'bias': bias,
        'higher_highs': higher_highs,
        'lower_lows': lower_lows,
        'price_range_pct': price_range * 100
    }


def build_price_action_signal(df, patterns, levels, structure):
    from .data import get_session

    last = df.iloc[-1]
    current_price = float(last['Close'])

    recent_patterns = [p for p in patterns if p['index'] >= len(df) - 5]

    nearest_support = None
    nearest_resistance = None

    for level in levels:
        if level['type'] == 'Support' and level['level'] < current_price:
            if nearest_support is None or level['level'] > nearest_support['level']:
                nearest_support = level
        elif level['type'] == 'Resistance' and level['level'] > current_price:
            if nearest_resistance is None or level['level'] < nearest_resistance['level']:
                nearest_resistance = level

    dist_to_support = ((current_price - nearest_support['level']) / current_price * 100) if nearest_support else None
    dist_to_resistance = ((nearest_resistance['level'] - current_price) / current_price * 100) if nearest_resistance else None

    return {
        'pair': 'EUR/USD',
        'price': current_price,
        'session': get_session(),
        'market_structure': structure['structure'],
        'bias': structure['bias'],
        'price_range_pct': round(structure['price_range_pct'], 2),
        'recent_patterns': [f"{p['pattern']} ({p['signal']})" for p in recent_patterns],
        'nearest_support': round(nearest_support['level'], 5) if nearest_support else None,
        'support_strength': nearest_support['strength'] if nearest_support else None,
        'dist_to_support_pct': round(dist_to_support, 2) if dist_to_support else None,
        'nearest_resistance': round(nearest_resistance['level'], 5) if nearest_resistance else None,
        'resistance_strength': nearest_resistance['strength'] if nearest_resistance else None,
        'dist_to_resistance_pct': round(dist_to_resistance, 2) if dist_to_resistance else None
    }
