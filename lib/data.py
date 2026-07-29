import pandas as pd
import pickle
from pathlib import Path
from datetime import datetime, timezone, timedelta
from openbb import obb

CACHE_DIR = Path("data_cache")
CACHE_DURATION_MINUTES = 60
CACHE_DIR.mkdir(exist_ok=True)

PERIOD_MAP = {
    "1d": timedelta(days=1),
    "5d": timedelta(days=5),
    "1mo": timedelta(days=30),
    "3mo": timedelta(days=90),
    "6mo": timedelta(days=180),
    "1y": timedelta(days=365),
    "2y": timedelta(days=730),
    "5y": timedelta(days=1825),
}


def get_cached_data(symbol, interval, period):
    cache_key = f"{symbol}_{interval}_{period}".replace("=", "_").replace("/", "_")
    cache_file = CACHE_DIR / f"{cache_key}.pkl"

    if cache_file.exists():
        cache_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if cache_age < timedelta(minutes=CACHE_DURATION_MINUTES):
            print(f"✓ Using cached data (age: {cache_age.seconds//60}m {cache_age.seconds%60}s)")
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        else:
            print(f"✗ Cache expired (age: {cache_age.seconds//60}m)")

    print(f"⬇ Downloading fresh data for {symbol}...")

    end_date = datetime.now()
    start_date = end_date - PERIOD_MAP.get(period, timedelta(days=1))

    data = obb.currency.price.historical(
        symbol=symbol.replace("=X", ""),
        interval=interval,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        provider="yfinance",
    )

    df = data.to_dataframe()

    if 'date' in df.columns:
        df = df.set_index(pd.to_datetime(df['date']))
        df.drop(columns=['date'], inplace=True)

    df.columns = [col.capitalize() for col in df.columns]

    with open(cache_file, 'wb') as f:
        pickle.dump(df, f)

    return df


def get_session():
    hour = datetime.now(timezone.utc).hour

    if 7 <= hour < 16:
        return "London"
    elif 13 <= hour < 22:
        return "New York"
    else:
        return "Asian"
